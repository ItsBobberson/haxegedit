from gi.repository import Gdk, Gedit, Gio, GObject, Gtk, PeasGtk
from OutputPanel import OutputPanel
from DebuggerPanel import DebuggerPanel
from DebuggerInfoPanel import DebuggerInfoPanel
from ConfigurationWindow import ConfigurationWindow
#from SidePanel import SidePanel
from SettingsFrame import SettingsFrame
from ToolBar import ToolBar
import Configuration
import os
import sys
import subprocess

class haxeide(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    __gtype_name__ = "haxeide"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
        self.name = "haxeide"
        self.busy=False;

    def do_activate(self):
        self.dataDir = self.plugin_info.get_data_dir()
        self.toolBar = ToolBar(self)
        #self.sidePanel = SidePanel(self)
        
        self.outputPanel = OutputPanel(self)
        self.debuggerInfoPanel = DebuggerInfoPanel(self)
        self.debuggerPanel = DebuggerPanel(self)
        self.handlerId = self.window.connect("key-press-event", self.on_view_key_press_event)
        
    def showHaxeWindow(self):
        ConfigurationWindow(self)  
        
    def do_deactivate(self):
        self.toolBar.remove()
        #self.sidePanel.remove()
        self.debuggerInfoPanel.remove()
        self.outputPanel.remove()
        self.debuggerPanel.remove()
        Configuration.setHxml("")
        self.window.disconnect(self.handlerId)
        
    def do_create_configure_widget(self):
        return SettingsFrame(self)    
        
    def do_update_state(self):
        pass
       
    def createProject(self, target, destinationFolder, folderName, mainName, package):
        root = destinationFolder + "/" + folderName
        hxml = destinationFolder + "/" + folderName + "/" + "build.hxml"
        main = destinationFolder + "/" + folderName + "/" + "src" +"/" + mainName.replace(".", "/")+".hx"
    
        cwd = self.plugin_info.get_data_dir() + "/" + "scripts"
        command = ["./createproject.sh", target, destinationFolder, folderName, mainName]
        proc = subprocess.Popen (command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
        out = proc.communicate ()
        if proc.returncode == 0:
            self.openFile(hxml, True)
            self.openFile(main, True)
            self.setFileBrowserRoot(root)
            self.setHxml(hxml)
        else:
            Gedit.App.get_default().get_active_window().get_bottom_panel().set_property("visible", True)
            self.outputPanel.activate()
            self.outputPanel.setText(out[1])

    def openProject(self, hxml, useHxml, setRoot ):
        self.openFile(hxml, True)
        if setRoot:
            self.setFileBrowserRoot(os.path.dirname(hxml))
        if useHxml:
            Configuration.setHxml(hxml)
            self.toolBar.setHxml(hxml)
        
    def saveSession(self):
        hxml = self.sf(Configuration.getHxml())
        if hxml == None or hxml == "":
            return
        sessionsHash = Configuration.getSessions()
        sessionsHash[hxml] = [hxml]
        docs = self.window.get_documents()
        for d in docs:
            uri = self.sf(d.get_uri_for_display())
            if uri != hxml:
                sessionsHash[hxml].append(uri)
        Configuration.saveSessions(sessionsHash)
          
    def openSession(self, hxml, useHxml, setRoot ):
        self.openFile(hxml, False)
        if setRoot:
            self.setFileBrowserRoot(os.path.dirname(hxml))
        if useHxml:
            Configuration.setHxml(hxml)
            self.toolBar.setHxml(hxml)
            
        sessionsHash = Configuration.getSessions()
        files = []
        if hxml in sessionsHash:
            files = sessionsHash[hxml]
        for i in files:
            self.openFile(i, False)
            
    def openFile(self, filePath, jumpTo):
        #print filePath
        #print os.path.exists(filePath)
        #print os.path.isfile(filePath)
        if not os.path.isfile(filePath):
            msg = "haxeide.py : 119 : not os.path.isfile(filePath) : " + filePath
            Gedit.App.get_default().get_active_window().get_bottom_panel().set_property("visible", True)
            self.outputPanel.activate()
            self.outputPanel.setText(msg)
            print msg
            return
            
        uri = "file://" + filePath
        #Gio.file_new_for_path(os.path.expanduser('~')
        #gio_file = Gio.file_new_for_path(filePath)
        gio_file = Gio.file_new_for_uri(uri)
        tab = self.window.get_tab_from_location(gio_file)
        if tab == None:
            tab = self.window.create_tab_from_location( gio_file, None, 0, 0, False, False )
        if jumpTo:
            self.window.set_active_tab(tab)

    def setFileBrowserRoot(self, location):
        object_path = '/plugins/filebrowser'
        method = "set_root"
        arg1 = Gio.file_new_for_path(location)
        arg2 = None
        bus = self.window.get_message_bus()
        if bus.is_registered(object_path, method):
            msgType = bus.lookup(object_path, method)
            msg = GObject.new(msgType, object_path=object_path, method=method, location=arg1, virtual=arg2)
            bus.send_message(msg)
            #bus = Gedit.MessageBus.get_default()
            #bus.send(object_path, method, location=arg1, virtual=arg2)
            side_panel = Gedit.App.get_default().get_active_window().get_side_panel()
            side_panel.set_property("visible", True)
        else:
            Gedit.App.get_default().get_active_window().get_bottom_panel().set_property("visible", True)
            self.outputPanel.activate()
            self.outputPanel.setText("File browser plugin was not enabled or not installed.")
   
    def setActiveDocAsHxml(self):
        doc = self.window.get_active_document()
        hxml = doc.get_uri_for_display()
        self.setHxml(hxml)
        
    def setHxml(self, hxml):
        Configuration.setHxml(hxml)
        self.toolBar.setHxml(hxml)
        
    def saveAndBuild(self):
        self.outputPanel.activate()
        self.outputPanel.setText("")
        unsavedDocuments = self.window.get_unsaved_documents()
        total = len(unsavedDocuments)
        if(total==0):
            self.build()
        else:
            self.counter = 0
            self.handlers = {}
            for doc in unsavedDocuments:
                if doc.is_untouched() or doc.is_untitled():
                    continue
                self.handlers[doc.get_uri_for_display()] = doc.connect("saved", self.onSaved, total)
                Gedit.commands_save_document(self.window, doc)
            
    def onSaved(self, doc, error, total):
        doc.disconnect(self.handlers[doc.get_uri_for_display()])
        self.counter += 1
        if(self.counter == total):
            self.build()
            
    def build(self):
        if self.busy:
            return
        self.busy = True
        hxml = self.sf(Configuration.getHxml())

        command = ["haxe", hxml]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(hxml))
        out = proc.communicate()
        
        bottom_panel = Gedit.App.get_default().get_active_window().get_bottom_panel()
        
        if proc.returncode != 0:
            bottom_panel.set_property("visible", True)
            self.outputPanel.activate()
            self.outputPanel.setText(out[1])
            
        else:
            self.outputPanel.activate()
            self.outputPanel.setText("Building done.\n")
            
            if Configuration.getAutoHideConsole():
                bottom_panel.set_property("visible", False)
            
            self.runApplication(hxml)
            
        self.busy = False
        
    def runApplication(self, hxml):
        bottom_panel = Gedit.App.get_default().get_active_window().get_bottom_panel()
        if not os.path.isfile(os.path.dirname(hxml)+"/run.sh"):
            bottom_panel.set_property("visible", True)
            self.outputPanel.activate()
            self.outputPanel.appendText("Can't find " + os.path.dirname(hxml)+"/run.sh to test.\n")
            return 
        
        os.system("cd " +os.path.dirname(hxml)+";sh run.sh &")
        """
        p = os.popen("cd " +os.path.dirname(hxml)+";sh run.sh &","r")
        bottom_panel.set_property("visible", True)
        while 1:
            line = p.readline()
            if not line: break
            self.bottomPanel.appendText(line+"\n")
        """
        """
        command = [os.path.dirname(hxml)+"/run.sh"]
        command = ["gnome-terminal", "--command=run.sh"]# --command="+os.path.dirname(hxml)+"/run.sh"]
        proc = subprocess.Popen(command,cwd=os.path.dirname(hxml),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.communicate()
        if proc.returncode != 0:
        self.bottomPanel.set_property("visible", True)
        self.bottomPanel.appendText(out[0])
        self.bottomPanel.appendText(out[1])
                
        #r = os.system("bash /home/jan/MyDocuments/haxe-test/test3/run.sh")
        """ 
        
    def readUntilFDB(self, proc, output):
        result = ""
        seqPromt = ["(","f","d","b",")"]
        #seqQuit=["(","y", "o", "r", "n", ")"]
        counter = 0
        tempstr = ""
        while True:
            c = proc.stdout.read(1)
            result = result +c
            if output:
                self.debuggerPanel.appendText(c)
            if c == seqPromt[counter]:
                counter = counter + 1
                tempstr = tempstr + c
                if tempstr == "(fdb)":
                    counter = 0
                    tempstr = ""
                    break
            else:
                counter = 0
                tempstr = ""
        proc.stdout.flush()
        return result
        
        
    def sendDebugInfoCommand(self, cmd):
        try:
            self.proc
        except:
            self.debuggerPanel.appendText("no debugger running\n")
            return ""
        if self.proc == None:
            self.debuggerPanel.appendText("no debugger running\n")
            return ""
        self.proc.stdin.write(cmd+"\n")
        try:
            self.proc.stdin.flush()
        except:
            return ""
        return self.readUntilFDB(self.proc, False)
        
    def sendDebugCommand(self, cmd):
        try:
            self.proc
        except:
            self.debuggerPanel.appendText("no debugger running\n")
            return
        if self.proc == None:
            self.debuggerPanel.appendText("no debugger running\n")
            return
        self.debuggerPanel.appendText(">>>"+cmd+"\n")
        self.proc.stdin.write(cmd+"\n")
        try:
            self.proc.stdin.flush()
        except:
            return
        if cmd == "continue":
            self.readUntilFDB(self.proc, True)
        elif cmd=="kill":
            self.proc.stdin.write("y\n")
            self.proc.stdin.flush()
            self.debuggerPanel.appendText(">>>y\n")
            
        elif cmd == "quit" or cmd=="kill":
            self.proc.stdin.write("y\n")
            self.proc.stdin.flush()
            self.proc = None
            self.debuggerPanel.appendText(">>>y\n")
        else:
            self.readUntilFDB(self.proc, True)
    
    def debug(self, swf):
        bottom_panel = Gedit.App.get_default().get_active_window().get_bottom_panel()
        bottom_panel.set_property("visible", True)
        
        side_panel = Gedit.App.get_default().get_active_window().get_side_panel()
        side_panel.set_property("visible", True)
            
        self.debuggerPanel.activate()
        
        command = ["fdb"]
        #cwd=os.path.dirname(self.sf(Configuration.getHxml()))+"/bin"
        cwd=os.path.dirname(self.sf(Configuration.getHxml()))
        self.proc = subprocess.Popen(command, bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
        self.readUntilFDB(self.proc,True)

        #self.proc.stdin.write("run index.swf\n")
        self.proc.stdin.write("run "+swf+"\n")
        self.proc.stdin.flush()
        self.readUntilFDB(self.proc, True)
        
        #1
        #Adobe fdb (Flash Player Debugger) [build 23201]
        #Copyright (c) 2004-2007 Adobe, Inc. All rights reserved.
        #(fdb) 
        
        #2
        #Attempting to launch and connect to Player using URL
        #index.swf
        #Player connected; session starting.
        #Set breakpoints and then type 'continue' to resume the session.
        #[SWF] /home/jan/MyDocuments/haxe-test/debugger-test/bin/index.swf - 7,332 bytes after decompression
        #(fdb)
        
        """
        (fdb) Generic command for showing things about the program being debugged.
        List of info subcommands:
        info arguments (i a)    Argument variables of current stack frame
        info breakpoints (i b)  Status of user-settable breakpoints
        info display (i d)      Display list of auto-display expressions
        info files (i f)        Names of targets and files being debugged
        info functions (i fu)   All function names
        info handle (i h)       How to handle a fault
        info locals (i l)       Local variables of current stack frame
        info scopechain (i sc)  Scope chain of current stack frame
        info sources (i so)     Source files in the program
        info stack (i s)        Backtrace of the stack
        info swfs (i sw)        List of swfs in this session
        info targets(i t)       Application being debugged
        info variables (i v)    All global and static variable names
        Type 'help info' followed by info subcommand name for full documentation.
        """

    def on_view_key_press_event(self, view, event):
        """
        #build on key press (blocks)
        doc = self.window.get_active_document()
        try:
            if not doc.get_uri_for_display().endswith ('hx'):
                return
        except:
            return
        if doc.is_untouched():
            return
        Gedit.commands_save_document(self.window, doc)
        self.build()
        """
        #print "view event.keyval %s" % event.keyval
        if self.toolBar.buildButton.get_sensitive() :
            keybinding = Configuration.getKeybindingBuildTuple()
            ctrl_pressed = (event.state & Gdk.ModifierType.CONTROL_MASK) == Gdk.ModifierType.CONTROL_MASK
            alt_pressed = (event.state & Gdk.ModifierType.MOD1_MASK) == Gdk.ModifierType.MOD1_MASK
            shift_pressed = (event.state & Gdk.ModifierType.SHIFT_MASK) == Gdk.ModifierType.SHIFT_MASK
            keyval = Gdk.keyval_from_name(keybinding[Configuration.KEY])
            # It's only ok if a key is pressed and it's needed or if a key is not pressed if it isn't needed.
            ctrl_ok = not (keybinding[Configuration.MODIFIER_CTRL] ^ ctrl_pressed )
            alt_ok =  not (keybinding[Configuration.MODIFIER_ALT] ^ alt_pressed )
            shift_ok = not (keybinding[Configuration.MODIFIER_SHIFT] ^ shift_pressed )
            key_ok = (event.keyval == keyval)
        
            if ctrl_ok and alt_ok and shift_ok and key_ok:
                self.saveAndBuild()
                
    #sanitize file
    def sf(self, path):
        if path == None or path=="":
            return path
        if path[1]=="/":
            return path[1:]
        return path
        
            
                
        
        
    

        
