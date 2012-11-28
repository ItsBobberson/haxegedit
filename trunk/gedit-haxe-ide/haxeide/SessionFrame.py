from gi.repository import GObject, Gtk, Gdk, Gedit
import string
import os
import Configuration

class SessionFrame(Gtk.Frame):
    __gtype_name__ = "SessionFrame"
    
    def __init__(self, plugin, win):
        Gtk.Frame.__init__(self)
        self.plugin = plugin
        self.win = win
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.hxmlFile=""
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "SessionBox.glade")
        self.builder.connect_signals(self)
        self.builder.get_object("openProjectBtn").set_sensitive(False)
        self.vbox = self.builder.get_object("vbox")
        self.add(self.vbox)
        
        uri = Configuration.getProjectsLocation()
        if uri !=None and uri!="":
            self.builder.get_object("filechooser").set_current_folder_uri(uri)
            
        filter = Gtk.FileFilter()
        filter.set_name("*.hxml")
        filter.add_pattern("*.hxml")
        self.builder.get_object("filechooser").add_filter(filter)
        
        self.builder.get_object("locationInput").set_size_request(300,20)
        
        self.show_all()

    def onOpenProjectBtnClick(self, button):
        #fileName = os.path.basename(self.hxmlFile)
        #folderPath =  os.path.dirname(self.hxmlFile)
        if self.builder.get_object("closeTabsCheckBox").get_active():
            self.plugin.window.close_all_tabs()
        #self.plugin.openFile(folderPath, fileName, True)
        self.plugin.openProject(self.hxmlFile)
        self.win.destroy()
        
    def onFileSelect(self,fileChooser):
        fn = fileChooser.get_filename()
        if fn != None:
            if fn.endswith(".hxml"):
                self.hxmlFile = fn
                self.builder.get_object("locationInput").set_text(fn)
                self.builder.get_object("openProjectBtn").set_sensitive(True)
            else:
                self.hxmlFile = ""
                self.builder.get_object("locationInput").set_text("")
                self.builder.get_object("openProjectBtn").set_sensitive(False)
            
