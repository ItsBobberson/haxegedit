from gi.repository import Gdk, Gedit, Gio, GObject, Gtk, PeasGtk
from OutputPanel import OutputPanel
from DebuggerPanel import DebuggerPanel
from DebuggerInfoPanel import DebuggerInfoPanel
from ConfigurationWindow import ConfigurationWindow
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
        self.outputPanel = OutputPanel(self)
        self.debuggerPanel = DebuggerPanel(self)
        self.debuggerInfoPanel = DebuggerInfoPanel(self)
        
        self.handlerId = self.window.connect("key-press-event", self.on_view_key_press_event)
        
    def showHaxeWindow(self):
        ConfigurationWindow(self)  
        
    def do_deactivate(self):
        self.toolBar.remove()
        self.debuggerInfoPanel.remove()
        self.outputPanel.remove()
        self.debuggerPanel.remove()
        Configuration.setHxml("")
        self.window.disconnect(self.handlerId)
        
    def do_create_configure_widget(self):
        return SettingsFrame(self)    
        
    def do_update_state(self):
        pass
       
    def createProject(self, target, destinationFolder, folderName, mainName, useHxml, setRoot):
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
            if setRoot:
                self.setFileBrowserRoot(root)
            if useHxml:
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
            #self.toolBar.setHxml(hxml)
        
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
            #self.toolBar.setHxml(hxml)
        sessionsHash = Configuration.getSessions()
        files = []
        if hxml in sessionsHash:
            files = sessionsHash[hxml]
        for i in files:
            self.openFile(i, False)
            
    def openFile(self, filePath, jumpTo):
        if not os.path.isfile(filePath):
            msg = "A file from this session could not be found:" + filePath
            Gedit.App.get_default().get_active_window().get_bottom_panel().set_property("visible", True)
            self.outputPanel.activate()
            self.outputPanel.setText(msg)
            return
        #gio_file = Gio.file_new_for_path(filePath)
        gio_file = Gio.file_new_for_uri("file://" + filePath)
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
            if Configuration.getPlayAfterBuild():
                self.runApplication(hxml)
        self.busy = False
        
    def runApplication(self, hxml):
        runFile = Configuration.getRunFile()
        if runFile=="" and not os.path.isfile(os.path.dirname(hxml)+"/" + runFile):
            bottom_panel = Gedit.App.get_default().get_active_window().get_bottom_panel()
            bottom_panel.set_property("visible", True)
            self.outputPanel.activate()
            self.outputPanel.appendText("No post compilation run file found: " + os.path.dirname(hxml) + "/" + runFile + "\n")
            return
        else:
            os.system("cd " +os.path.dirname(hxml)+";sh " + runFile +"&")
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
        
    
                
    def on_view_key_press_event(self, view, event):
        """
        doc = self.window.get_active_document()
        fullpath = doc.get_uri_for_display()
        if fullpath.endswith ('hx'):
            file = open (fullpath, "w")
            file.write (origdoc)
            file.close ()
        """
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
