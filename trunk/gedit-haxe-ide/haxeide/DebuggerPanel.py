import Configuration
import os
from gi.repository import GObject, Gtk, Gdk, Gedit, Gio, GLib
import string
import subprocess

class DebuggerPanel(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "DebuggerPanel"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self, plugin):
        GObject.Object.__init__(self)
        self.plugin = plugin
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.geditWindow = plugin.window
        self.debugType = "fdb"
        self.eom = "("+self.debugType+")"
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "DebuggerBox.glade")
        self.builder.connect_signals(self)
        
        self.box = self.builder.get_object("box")
        
        self.textView = self.builder.get_object("textView")
        self.textView.set_editable (False)
        self.textView.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(red=65535, green=65535, blue=65535))
        self.textView.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(red=11776, green=13312, blue=13824))
        self.textView.modify_bg(Gtk.StateType.SELECTED, Gdk.Color(red=51776, green=0, blue=0))

        self.geditBottomPanel = self.geditWindow.get_bottom_panel()
        self.geditBottomPanel.add_item(self.box, "haxe_debugger_panel", "debugger", Gtk.Image.new_from_file(self.dataDir + "/" + "icons" + "/" + "haxe_logo_16.png"))# Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU))
        self.geditBottomPanel.activate_item(self.box)
        
        self.builder.get_object("buttonBox").hide()
        
        self.toolbar = self.builder.get_object("toolbar")
        self.toolbar.set_icon_size(1)
        
        self.breakButton = Gtk.ToolButton(stock_id=Gtk.STOCK_ADD)
        self.breakButton.connect("clicked", self.onBreakButtonClick)
        self.breakButton.set_tooltip_text('Break on selected line')
        
        self.clearButton = Gtk.ToolButton(stock_id=Gtk.STOCK_DELETE)
        self.clearButton.connect("clicked", self.onClearButtonClick)
        self.clearButton.set_tooltip_text('Clear breakpoint from selected line')
        
        self.stepButton = Gtk.ToolButton(icon_widget=Gtk.Image.new_from_file(self.dataDir+"/"+"icons"+"/"+ "debug_step.png")) #Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_NEXT)
        self.stepButton.connect("clicked", self.onStepButtonClick)
        self.stepButton.set_tooltip_text('Step into line')
        
        self.nextButton = Gtk.ToolButton(icon_widget=Gtk.Image.new_from_file(self.dataDir+"/"+"icons"+"/"+ "debug_next.png")) #Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_NEXT)
        self.nextButton.connect("clicked", self.onNextButtonClick)
        self.nextButton.set_tooltip_text('Next source line')
        
        self.finishButton = Gtk.ToolButton(icon_widget=Gtk.Image.new_from_file(self.dataDir+"/"+"icons"+"/"+ "debug_finish.png")) #Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_FORWARD)
        self.finishButton.connect("clicked", self.onFinishButtonClick)
        self.finishButton.set_tooltip_text('Finish current function')
        
        self.pauseButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_PAUSE)
        self.pauseButton.connect("clicked", self.onPauseButtonClick)
        self.pauseButton.set_tooltip_text('Break at current execution address')
        
        self.continueButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_PLAY)
        self.continueButton.connect("clicked", self.onContinueButtonClick)
        self.continueButton.set_tooltip_text('Continue execution after stopping at breakpoint')
        
        self.killButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_STOP)
        self.killButton.connect("clicked", self.onKillButtonClick)
        self.killButton.set_tooltip_text('Kill execution of program being debugged')

        self.quitButton = Gtk.ToolButton(stock_id=Gtk.STOCK_QUIT)
        self.quitButton.connect("clicked", self.onQuitButtonClick)
        self.quitButton.set_tooltip_text('Quit fdb')
        
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.breakButton)
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.clearButton)
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = Gtk.SeparatorToolItem())
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.stepButton)
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.nextButton)
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.finishButton)
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = Gtk.SeparatorToolItem())
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.pauseButton)
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.continueButton)
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.killButton)
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = Gtk.SeparatorToolItem())
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.quitButton)

        self.toolbar.show_all()
        
    def activate(self):
        self.geditBottomPanel.activate_item(self.box)
            
    def remove(self):
        self.geditBottomPanel.remove_item(self.box)
    
    
    #    ToolBar Top File
    
    def onBinFileInputChange(self, entry):
        if entry.get_text().endswith(".swf"):
            self.debugType = "fdb"
            self.eom = "(fdb)"
            self.builder.get_object("urlLabel").set_text("swf:")
        else:
            self.debugType = "gdb"
            self.eom = "(gdb)"
            self.builder.get_object("urlLabel").set_text("cpp:")
            
        self.builder.get_object("consoleLabel").set_text(self.debugType + ":")
            
    def onStartDebugButtonClick(self, button):
        hxml = self.sf(Configuration.getHxml())
        hxmlDir = os.path.dirname(hxml)
        file = self.builder.get_object("urlInput").get_text()
        path = hxmlDir + "/" + file
        
        if not os.path.isfile(path):
            self.appendText("Could not find " + path)
        else:
            self.builder.get_object("urlBox").hide()
            self.builder.get_object("buttonBox").show()
            
        GObject.idle_add(self.runDebugger, file)
    
    
    #    ToolBar Top Debug        

    def onBreakButtonClick(self, button):
        fileLine = self.getFileLine()
        if fileLine != None:
            self.sendDebugCommand("break "+fileLine)        
            
    def onClearButtonClick(self, button):
        fileLine = self.getFileLine()
        if fileLine != None:
            self.sendDebugCommand("clear "+fileLine)
    
    def onStepButtonClick(self, button):
        self.sendDebugCommand("step")
        
    def onNextButtonClick(self, button):
        self.sendDebugCommand("next")
        
    def onFinishButtonClick(self, button):
        self.sendDebugCommand("finish")
        
    def onContinueButtonClick(self, button):
        if self.debugType=="gdb" and self.gdbFirstRun:
            self.gdbFirstRun=False
            self.sendDebugCommand("run")
        else:
            self.sendDebugCommand("continue")
        
    def onPauseButtonClick(self, button):    
        self.sendDebugCommand("break")
            
    def onKillButtonClick(self, button):    
        self.sendDebugCommand("kill")
        self.sendDebugCommand("y")
   
    def onQuitButtonClick(self, button):
        self.sendDebugCommand("quit")
        self.sendDebugCommand("y")
        self.proc = None
        self.builder.get_object("urlBox").show()
        self.builder.get_object("buttonBox").hide()
   
    
    #   TextView Console
        
    def setText(self, txt):
        textBuffer = self.textView.get_buffer()
        textBuffer.set_text(txt)
        
    def appendText(self, txt):
        textBuffer = self.textView.get_buffer()
        textBuffer.insert(textBuffer.get_end_iter(), txt)
        self.textView.scroll_mark_onscreen(textBuffer.get_insert())
        #self.textView.scroll_to_mark(textBuffer.get_insert(), 0)
    
    
    #   ToolBar Bottom
    
    def onClearConsoleButton(self, button):
        self.textView.get_buffer().set_text("")
        
    def onConsoleButtonClick(self, button):
        txt = self.builder.get_object("consoleInput").get_text()
        self.builder.get_object("consoleInput").set_text("")
        self.sendDebugCommand(txt)
        if txt=="kill" or txt=="quit":
            self.sendDebugCommand("y")

   
    #   Debugger
     
    def runDebugger(self, file):
        bottom_panel = Gedit.App.get_default().get_active_window().get_bottom_panel()
        bottom_panel.set_property("visible", True)
        side_panel = Gedit.App.get_default().get_active_window().get_side_panel()
        side_panel.set_property("visible", True)   
        self.activate()

        command = [self.debugType]
        hxmlDir = os.path.dirname(self.sf(Configuration.getHxml()))
        
        self.proc = subprocess.Popen(command, bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=hxmlDir)
        self.readUntilEOM(self.proc,True)

        if self.debugType == "fdb":
            self.sendDebugCommand("run " + file)
        else:
            self.gdbFirstRun = True
            self.sendDebugCommand("file " + file)
                
    def sendDebugCommand(self, cmd):
        #1 check
        try:
            if self.proc == None:
                self.appendText("no debugger running\n")
                return ""
        except:
            self.appendText("no debugger running\n")
            return ""  
        #2 write
        self.appendText(">>>"+cmd+"\n")
        self.proc.stdin.write(cmd+"\n")
        self.proc.stdin.flush()
        #3 avoid block
        if cmd=="kill" or cmd=="quit" or cmd=="y":
            return
        #4 read
        self.readUntilEOM(self.proc, True)
        #5 update
        if cmd=="step" or cmd == "next" or cmd=="finish" or cmd=="continue" or cmd=="run":
            self.plugin.debuggerInfoPanel.setStack(True)
            self.plugin.debuggerInfoPanel.setLocals()
            self.plugin.debuggerInfoPanel.setArgs()
            self.plugin.debuggerInfoPanel.setThis()
            self.plugin.debuggerInfoPanel.setVariables()
            self.plugin.debuggerInfoPanel.setBreakPoints()
        elif cmd[0:6]=="break ":
            self.plugin.debuggerInfoPanel.setBreakPoints()
                   
    def sendDebugInfoCommand(self, cmd):
        #1 check
        try:
            if self.proc == None:
                self.appendText("no debugger running\n")
                return ""
        except:
            self.appendText("no debugger running\n")
            return ""
        #2 write    
        self.proc.stdin.write(cmd+"\n")
        self.proc.stdin.flush()
        #3 read
        return self.readUntilEOM(self.proc, False)

    def readUntilEOM(self, proc, output):
        result = ""
        tempstr = ""
        while True:
            c = proc.stdout.read(1)
            result = result + c
            if output:
                self.appendText(c)
            if c == self.eom[len(tempstr)]:
                tempstr = tempstr + c
                if tempstr == self.eom:
                    tempstr = ""
                    break
            elif c == self.eom[0]:
                tempstr = c
            else:
                tempstr = ""
        proc.stdout.flush()
        return result

        
    #   Breakpoints helpers
    
    def getFileLine(self):
        doc = self.geditWindow.get_active_document()
        uri = doc.get_uri_for_display()
        if uri.endswith ('hx') or uri.endswith ('cpp'):
            lineOffset = doc.get_iter_at_mark(doc.get_insert()).get_line()+1
            fileName = os.path.basename(uri)
            if self.debugType=="gdb" and uri.endswith ('hx'):
                return self.mapHXtoCPP(uri, str(lineOffset))    
            return fileName+":"+str(lineOffset)
        else:
            self.appendText("You can only set breakpoints in .hx or .cpp files.\n")
            return None
        
    def mapHXtoCPP(self, uri, lineOffset):
        uriHx = self.sf(uri)
        hxmlDir = os.path.dirname(self.sf(Configuration.getHxml()))
        basePartHx = uriHx.split(hxmlDir+"/")[-1]
        basePartCpp = basePartHx[0:-3] + ".cpp"
        uriCpp = hxmlDir+"/bin/"+ basePartCpp
        """
        print uriHx
        print hxmlDir
        print basePartHx
        print basePartCpp
        """
        f = open(uriCpp)
        cppCode = f.read()
        f.close()
        mark = basePartHx+","+lineOffset
        
        parts = cppCode.split(basePartHx+'",'+lineOffset)
        if len(parts)==1:
            return None
        lines = parts[0].split("\n")
        """
        print uriCpp
        print mark
        print len(lines)+1
        """
        fileName = fileName = os.path.basename(uriCpp)
        lineOffset = len(lines)+1
        return fileName+':'+ str(lineOffset)
        

    # Sanitize file
    
    def sf(self, path):
        if path == None or path=="":
            return path
        if path[1]=="/":
            return path[1:]
        return path
