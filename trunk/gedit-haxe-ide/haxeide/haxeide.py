from gi.repository import Gdk, Gedit, Gio, GObject, Gtk, PeasGtk
from BottomPanel import BottomPanel
from ConfigurationWindow import ConfigurationWindow
#from SidePanel import SidePanel
from SettingsFrame import SettingsFrame
from ToolBar import ToolBar
import Configuration
import os
import subprocess

class haxeide(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    __gtype_name__ = "haxeide"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self.name = "haxeide"
        
    def do_activate(self):
        self.toolBar = ToolBar(self)
        #self.sidePanel = SidePanel(self)
        self.bottomPanel = BottomPanel(self)
        self.handlerId = self.window.connect("key-press-event", self.on_view_key_press_event)
        
    def showProjectWindow(self):
        ConfigurationWindow(self)  
        
    def do_deactivate(self):
        self.toolBar.remove()
        #self.sidePanel.remove()
        self.bottomPanel.remove()
        self.window.disconnect(self.handlerId)
        
    def do_create_configure_widget(self):
        return SettingsFrame(self)    
        
    def do_update_state(self):
        pass
             
    def on_view_key_press_event(self, view, event):
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
                
    def createProject(self, destinationFolder, folderName, mainName, target):
        cwd = self.plugin_info.get_data_dir() + "/" + "scripts"
        command = ["./createproject.sh", target, destinationFolder, folderName]#, target]
        proc = subprocess.Popen (command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
        out = proc.communicate ()
        str0 = out[0]
        str1 = out[1]
        bottom_panel = Gedit.App.get_default().get_active_window().get_bottom_panel()
        if proc.returncode != 0:
            bottom_panel.set_property("visible", True)
            self.bottomPanel.setText(out[1])
        else:
            self.openFile(destinationFolder, folderName, "build.hxml", True)
            self.openFile(destinationFolder, folderName, "src/Main.hx", True)

    def openFile(self, destinationFolder, folderName, fileName, jumpTo):
        uri = "file://" + "/" + destinationFolder + "/" + folderName + "/" + fileName
        gio_file = Gio.file_new_for_uri(uri)
        tab = self.window.get_tab_from_location(gio_file)
        if tab == None:
            tab = self.window.create_tab_from_location( gio_file, None, 0, 0, False, False )
        if jumpTo:
            self.window.set_active_tab(tab)
            if fileName.endswith(".hxml"):
                self.setHxml()
        self.setFileBrowserRoot(destinationFolder+"/"+folderName)
                
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
            pass
            #print relies on the file browser plugin
            
    def openProject(self, folder ):
        print "folder %s" %folder

    def setHxml(self):
        doc = self.window.get_active_document()
        self.hxmlPath = doc.get_uri_for_display()
        hxmlName = doc.get_short_name_for_display()
        
        buf = self.window.get_active_view().get_buffer()
        hxmlText = unicode (buf.get_text (*buf.get_bounds (),include_hidden_chars=True), 'utf-8')

        Configuration.setHxml(self.hxmlPath)
        #self.sidePanel.setHxml(self.hxmlPath, hxmlName, hxmlText)
        self.toolBar.setHxml(self.hxmlPath)
        
    def saveAndBuild(self):
        self.bottomPanel.setText("")
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
        command = ["haxe", self.hxmlPath]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(self.hxmlPath))
        out = proc.communicate()
        bottom_panel = Gedit.App.get_default().get_active_window().get_bottom_panel()
        try:
            if proc.returncode != 0:
                bottom_panel.set_property("visible", True)
                self.bottomPanel.setText(out[1])
            else:
                bottom_panel.set_property("visible", False)
        except Exception, e:
            bottom_panel.set_property("visible", True)
            self.bottomPanel.setText(e)
            
    def saveSession(self):
        print "TODO saveSession()"
