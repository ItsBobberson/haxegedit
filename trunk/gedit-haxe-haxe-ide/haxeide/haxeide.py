import os
import subprocess

from gi.repository import Gdk, Gedit, Gio, GObject, Gtk
import Configuration
from BottomPanel import BottomPanel
from ProjectWindow import ProjectWindow
from SidePanel import SidePanel
from ToolBar import ToolBar


filename20b = os.path.join(".icons", 'haxe20b.png')
filename24b = os.path.join(".icons", 'haxe24b.png')

class haxeide(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "haxeide"
    window = GObject.property(type=Gedit.Window)
    
    def test(self):
        object_path = '/plugins/filebrowser'
        method = "set_root"
        arg1 = Gio.file_new_for_uri("file:///MyDocuments")
        arg2 = "MyDocuments"
        
        bus = self.window.get_message_bus()
        #print bus.is_registered(object_path, method) # True
        msgType = bus.lookup(object_path, method) # GType GeditFileBrowserMessageSetRoot
        msg = GObject.new(msgType, object_path=object_path, method=method, location=arg1, virtual=arg2)
        bus.send_message_sync(msg)

    def __init__(self):
        GObject.Object.__init__(self)
        self.current_hxml = ""
        self.current_full_path = ""
        
    def do_activate(self):
        self.toolBar = ToolBar(self)
        self.sidePanel = SidePanel(self)
        self.bottomPanel = BottomPanel(self)

    def do_update_state(self):
        pass
    
    def do_deactivate(self):
        self.toolBar.remove()
        self.sidePanel.remove()
        self.bottomPanel.remove()
  
    def createProject(self, destinationFolder, folderName, mainName):
        basedir = "/home/jan/.config/gedit/haxeide"
        command = ["./createproject.sh", "flash", destinationFolder, folderName]
        proc = subprocess.Popen (command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=basedir)
        out = proc.communicate ()
        str0 = out[0]
        str1 = out[1]
        #print "str0 %s" %str0
        #print "str1 %s" %str1
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
        
    def openProject(self, folder ):
        print "folder %s" %folder

    def setHxml(self):
        doc = self.window.get_active_document()
        self.hxmlPath = doc.get_uri_for_display()
        hxmlName = doc.get_short_name_for_display()
        
        buf = self.window.get_active_view().get_buffer()
        hxmlText = unicode (buf.get_text (*buf.get_bounds (),include_hidden_chars=True), 'utf-8')

        Configuration.setHxml(self.hxmlPath)
        self.sidePanel.setHxml(self.hxmlPath, hxmlName, hxmlText)
        self.toolBar.setHxml(self.hxmlPath)
   
    def showProjectWindow(self):
        projectWindow = ProjectWindow(self)
            
    def build(self):
        self.bottomPanel.setText("Started building")
        
        for doc in self.window.get_unsaved_documents():
            if doc.is_untouched():
                continue
            if doc.is_untitled():
                continue
            Gedit.commands_save_document(self.window, doc)

        if self.hxmlPath != "":
            command = ["haxe", self.hxmlPath]
            proc = subprocess.Popen (command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(self.hxmlPath))
            out = proc.communicate ()
            str0 = out[0]
            str1 = out[1]
            self.bottomPanel.setText(str1 + "\nDone.")
            """
            print "returncode %s" % proc.returncode
            try:
                if proc.returncode == 1:
                    self.textbuffer.set_text(str1)      
            except Exception, e:
                self.textbuffer.set_text(str1)
            """
        else:
            self.bottomPanel.setText("Nothing to build. Reason: no hxml file set")   
                        
        
    
        
   
