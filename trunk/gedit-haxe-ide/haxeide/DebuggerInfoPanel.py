import Configuration
import os
from gi.repository import GObject, Gtk, Gdk, Gedit, Gio, GLib
import string

class DebuggerInfoPanel(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "DebuggerInfoPanel"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self, plugin):
        GObject.Object.__init__(self)
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.geditWindow = plugin.window
        self.debugger = plugin.debuggerPanel
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "DebuggerInfoBox.glade")
        self.builder.connect_signals(self)
        
        self.scrolledWindow = self.builder.get_object("scrolledWindow")
           
        self.toolbar = self.builder.get_object("toolbar")
        self.refreshButton = Gtk.ToolButton(stock_id=Gtk.STOCK_REFRESH)
        self.refreshButton.connect("clicked", self.onRefreshButtonClick)
        self.refreshButton.set_tooltip_text('Refresh all')
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.refreshButton)
        self.toolbar.show_all()
        
        self.geditSidePanel = self.geditWindow.get_side_panel()
        self.geditSidePanel.add_item(self.scrolledWindow, "haxe_debugger_info_panel", "Debugger info", Gtk.Image.new_from_file(self.dataDir + "/" + "icons" + "/" + "haxe_logo_16.png")) #Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU))
        self.geditSidePanel.activate_item(self.scrolledWindow)
        
    def activate(self):
        self.geditSidePanel.activate_item(self.scrolledWindow)
            
    def remove(self):
        self.geditSidePanel.remove_item(self.scrolledWindow)
 
    def onRefreshButtonClick(self, button):
        self.setBreakPoints()
        self.setStack(False)
        self.setLocals()
        self.setArgs()
        self.setThis()
        self.setFiles()
        self.setVariables()
        #self.setFunctions()
        #self.setScopeChain()
        
    def setStack(self, jumpTo):
        stackTreeView = self.builder.get_object("stackTreeView")
        stackTreeView.set_headers_visible(False)
        stackTreeView.get_selection().connect("changed", self.onStackSelectionChange, stackTreeView)
        if len(stackTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("info stack", Gtk.CellRendererText(), text=0)
            col.set_resizable (True) 
            stackTreeView.append_column(col)
        result = self.debugger.sendDebugInfoCommand("info stack")
        lines = result.split("\n")
        ls = Gtk.ListStore(str, str)
        for line in lines:
            if line != '(fdb)' and line != '(gdb)' and line != ' (gdb)':
                parts = line.split(" at ")
                ls.append([parts[-1], line])
        stackTreeView.set_model(ls)
        if jumpTo and len(ls)!=0:
            info = self.parseStackLineInfo(ls[0][1])
            self.jumpToSourceLine(info)
        
    def onStackSelectionChange (self, selection, tree):
        model, rows = selection.get_selected_rows()
        if len(rows)==0:
            return
        iter = model.get_iter(rows[0])
        info = self.parseStackLineInfo(model[iter][1])
        self.jumpToSourceLine(info)
    
    def jumpToSourceLine(self, info):
        path = info["file"]
        lineNr = int(info["lineNr"])
        if info["file"]=="":
            return
        gio_file = Gio.file_new_for_path(path)
        tab = self.geditWindow.get_tab_from_location(gio_file)
        if tab == None:
            tab = self.geditWindow.create_tab_from_location(gio_file, None, lineNr, 0, False, True )
        else:
            self.geditWindow.set_active_tab(tab)
            view = self.geditWindow.get_active_view()
            buf = view.get_buffer() 
            i = buf.get_iter_at_line_offset(lineNr - 1, 0)
            buf.place_cursor(i)
            view.scroll_to_cursor()

    def parseStackLineInfo(self, line):
        #line = " #0   this = [Object 3039793441, class='be.haxer::Main'].Main() at Main.hx:9"
        #line = "1  0x0808b2e1 in main (argc=1, argv=0xbffff704) at ./src/__main__.cpp:12"
        parts0 = line.split(" at ")
        fileNameLineNr = parts0[-1] #Main.hx:9 or ./src/__main__.cpp:12
        parts1 = fileNameLineNr.split(":")
        fileName = parts1[0] #./src/__main__.cpp
        lineNr = parts1[-1] # 12
        
        if fileName.startswith("/"):
            return {"file":os.path.normpath(fileName), "lineNr":lineNr}
        
        stdDir = "".join(os.environ['HAXE_LIBRARY_PATH'].split(":.")) # "/home/jan/Programs/Motion-Twin/haxe/std"
        libDir = os.environ['HAXEPATH'] + "/lib" #"/home/jan/Programs/Motion-Twin/haxe/lib"
        hxml = Configuration.getHxml()
        hxmlDir = os.path.dirname(hxml)
        searchLocations = [hxmlDir]    
        if fileName.endswith(".hx"):
            searchLocations.append(stdDir + "/flash9")
            classInfo0 = parts0[0] # #0   this = [Object 3039793441, class='be.haxer::Main'].Main()
            parts2 = classInfo0.split("'].")
            classInfo1 = parts2[0] # #0   this = [Object 3039793441, class='be.haxer::Main
            parts3 = classInfo1.split(", class='")
            classInfo2 = parts3[1] # be.haxer::Main
            parts4 = classInfo2.split("::")
            packagePath = ""
            if len(parts4) != 1:
                package = parts4[0]  # be.haxer
                packagePath = "/".join(package.split("."))
                cls = parts4[-1] # Main
            if packagePath == "":
                path = fileName
            else:
                path = packagePath + "/" + fileName
        elif fileName.endswith(".cpp") or fileName.endswith(".h"):
            searchLocations.append(stdDir + "/cpp")
            searchLocations.append(hxmlDir + "/bin")
            searchLocations.append(libDir + "/hxcpp")
            path = fileName
        else:
            return {"file":"", "lineNr":-1}
            
        f = open(hxml)
        lines = f.readlines()
        f.close()
        for line in lines:
           if line.startswith("-cp"):
               searchLocations.append(os.path.normpath(hxmlDir + "/" + line[4:-1]))
           elif line.startswith("-lib"):
               f = open(libDir+"/" + line[5:-1]+"/.current")
               version = f.readline()#[:-1]
               libPath = libDir+"/"+line[5:-1]+"/"+ ",".join(version.split("."))
               searchLocations.append(libPath)

        targetFile = ""
        
        for loc in searchLocations:
            file = os.path.normpath(loc + "/" + path)
            if file.endswith(".cpp") or file.endswith(".h"):
                if os.path.isfile(file):
                    targetFile = file
                    info = self.findHxCounterPart(searchLocations,targetFile,lineNr)
                    if info["file"] != "":
                        targetFile = info["file"]
                        lineNr = info["lineNr"]
                    break
            elif path.endswith(".hx"):
                if os.path.isfile(file):
                    targetFile = file
                    break
        
        return {"file":targetFile, "lineNr":lineNr}
        
    def findHxCounterPart(self, searchLocations, targetFile, lineNr):
        info = {"file":"", "lineNr":-1}
        f = open(targetFile)
        lines = f.readlines()
        f.close()
        debugLine = lines[int(lineNr)-1]
        if debugLine.find('HX_SOURCE_POS("') != -1 or debugLine.find('HX_SOURCE_PUSH("') != -1:
            self.debugger.sendDebugCommand("next")
            return
            
        hxSourcePos = lines[int(lineNr)-2]
        if hxSourcePos.find('HX_SOURCE_POS("') != -1:
            hxpathFileNr = hxSourcePos.split('HX_SOURCE_POS("')[-1].split('",') #[ src/Main.hx, 29) ]
            hxpath = hxpathFileNr[0]
            for loc in searchLocations:
                file = os.path.normpath(loc + "/" + hxpath)
                if os.path.isfile(file):
                    info["file"] = file
                    info["lineNr"] = int("".join(hxpathFileNr[1].split(')')))
                    break
        return info
        
    def setFiles(self):
        filesTreeView = self.builder.get_object("filesTreeView")
        filesTreeView.set_headers_visible(False)
        if len(filesTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("file", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            filesTreeView.append_column(col)
        result = self.debugger.sendDebugInfoCommand("info files")
        lines = result.split("\n")
        ls = Gtk.ListStore(str)
        for line in lines:
            if line != '(fdb)' and line != '(gdb)' and line != ' (gdb)':
                ls.append([line])       
        filesTreeView.set_model(ls)
        
    def setLocals(self):
        localsTreeView = self.builder.get_object("localsTreeView")
        localsTreeView.set_headers_visible(False)
        if len(localsTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("key", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            localsTreeView.append_column(col)
            col = Gtk.TreeViewColumn("value", Gtk.CellRendererText(), text=1)
            col.set_resizable(True)
            localsTreeView.append_column(col)  
        result = self.debugger.sendDebugInfoCommand("info locals")
        lines = result.split("\n")
        ls = Gtk.ListStore(str, str)
        for line in lines:
            if line != '(fdb)' and line != '(gdb)' and line != ' (gdb)':
                parts = line.split(" = ")
                if len(parts)==2:
                    ls.append([parts[0], parts[1]])      
        localsTreeView.set_model(ls)
        
    def setVariables(self):
        varsTreeView = self.builder.get_object("varsTreeView")
        varsTreeView.set_headers_visible(False)
        if len(varsTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("key", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            varsTreeView.append_column(col)
            col = Gtk.TreeViewColumn("value", Gtk.CellRendererText(), text=1)
            col.set_resizable(True)
            varsTreeView.append_column(col)
        result = self.debugger.sendDebugInfoCommand("info variables")
        lines = result.split("\n")
        ls = Gtk.ListStore(str, str)
        for line in lines:
            if line != '(fdb)' and line != '(gdb)' and line != ' (gdb)':
                parts = line.split(" = ")
                if len(parts)==2:
                    ls.append([parts[0], parts[1]])      
        varsTreeView.set_model(ls)
            
    def setArgs(self):
        argsTreeView = self.builder.get_object("argsTreeView")
        argsTreeView.set_headers_visible(False)
        if len(argsTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("key", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            argsTreeView.append_column(col)
            col = Gtk.TreeViewColumn("value", Gtk.CellRendererText(), text=1)
            col.set_resizable(True)
            argsTreeView.append_column(col)

        cmd = self.debugger.debugType == 'fdb' if "info arguments" else "info args"
        result = self.debugger.sendDebugInfoCommand("info args")
        lines = result.split("\n")
        ls = Gtk.ListStore(str, str)
        for line in lines:
            if line != '(fdb)' and line != '(gdb)' and line != ' (gdb)':
                parts = line.split(" = ")
                if len(parts)==2:
                    ls.append([parts[0], parts[1]])      
        argsTreeView.set_model(ls)
        

    def setBreakPoints(self):    
        breakPointsTreeView = self.builder.get_object("breakPointsTreeView")
        breakPointsTreeView.set_headers_visible(False)
        if len(breakPointsTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            breakPointsTreeView.append_column(col)
        result = self.debugger.sendDebugInfoCommand("info breakpoints")
        lines = result.split("\n")
        ls = Gtk.ListStore(str)
        for line in lines:
            if line != '(gdb)' and line != '(fdb)' and not line.startswith("  "):
                ls.append([line])
        breakPointsTreeView.set_model(ls)
        
    def setThis(self):
        thisTreeView = self.builder.get_object("thisTreeView")
        thisTreeView.set_headers_visible(False)
        if len(thisTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("key", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            thisTreeView.append_column(col)
            
            col = Gtk.TreeViewColumn("value", Gtk.CellRendererText(), text=1)
            col.set_resizable(True)
            thisTreeView.append_column(col)
        result = self.debugger.sendDebugInfoCommand("print this.")
        lines = result.split("\n")
        ls = Gtk.ListStore(str, str)
        for line in lines:
            if line != '(fdb)' and line != '(gdb)' and line != ' (gdb)':
                parts = line.split(" = ")
                if len(parts)==3:
                    self.builder.get_object("thisLabel").set_markup("<b>" + "["+ parts[-1].split(", ")[-1] + "</b>")
                if len(parts)==2:
                    ls.append([parts[0], parts[1]])      
        thisTreeView.set_model(ls)
