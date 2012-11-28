from gi.repository import GObject, Gtk, Gdk, Gedit
import string
import Configuration

class ProjectFrame(Gtk.Frame):
    __gtype_name__ = "ProjectFrame"
    
    def __init__(self, plugin, win):
        Gtk.Frame.__init__(self)
        self.plugin = plugin
        self.win = win
        self.dataDir = plugin.plugin_info.get_data_dir()
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "ProjectBox.glade")
        self.builder.connect_signals(self)
        
        self.vbox = self.builder.get_object("vbox")
        self.add(self.vbox)
        
        uri = Configuration.getProjectDefaultLocation()
        if uri !=None and uri!="":
            self.builder.get_object("filechooser").set_current_folder_uri(uri)
            
        package = Configuration.getProjectDefaultPackage()
        if package ==None or package =="None":
            package=""
        self.builder.get_object("packageInput").set_text(package)
            
        main = Configuration.getProjectDefaultMain()
        if main ==None or main =="None":
            main = ""
        if package!="":
            self.builder.get_object("mainInput").set_text(package+"."+main)
        else:
            self.builder.get_object("mainInput").set_text(main)
            
        self.show_all()
        
    def onCreateProjectButtonClick(self, button):
        destinationFolder = self.builder.get_object("locationInput").get_text()
        projectFolder = self.builder.get_object("nameInput").get_text()
        mainFile = self.builder.get_object("mainInput").get_text()
        #package = self.builder.get_object("packageInput").get_text()
        if destinationFolder != "" and projectFolder != "" and mainFile !="":
            target = "flash"
            if self.builder.get_object("jsCheckBtn").get_active():
                target = "js"
            elif self.builder.get_object("phpCheckBtn").get_active():
                target = "php"
            elif self.builder.get_object("nekoCheckBtn").get_active():
                target = "neko"
            elif self.builder.get_object("cppCheckBtn").get_active():
                target = "cpp"
                
            self.handleCloseAllDocuments()
            self.plugin.createProject(target, destinationFolder, projectFolder, mainFile, self.builder.get_object("useHxmlCheckBox").get_active(), self.builder.get_object("setRootCheckBox").get_active())
            self.win.destroy()
        else:
            pass
    
    def onFolderSelect(self,fileChooser):
        fn = fileChooser.get_filename()
        if fn != None:
            self.builder.get_object("locationInput").set_text(fn)

    def handleCloseAllDocuments(self):
        if self.builder.get_object("closeTabsCheckBox").get_active():
            self.plugin.window.close_all_tabs()
