from gi.repository import GObject, Gtk, Gdk, Gedit
import string


class ProjectWindow(Gtk.Window):

    def __init__(self, plugin):
        Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL);
        self.plugin = plugin
        self.set_title("Haxe Project Panel")
        self.set_size_request(1000,600)
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ProjectFrame.glade")
        self.builder.connect_signals(self)
 
        self.add(self.builder.get_object("frame"))
        
        self.show_all()
        
    def onCreateProjectButtonClick(self, button):
        destinationFolder = self.builder.get_object("locationInput").get_text()
        projectFolder = self.builder.get_object("nameInput").get_text()
        mainFile = self.builder.get_object("mainInput").get_text()
        if(destinationFolder != "" and projectFolder != "" and mainFile !=""):
            self.plugin.createProject(destinationFolder, projectFolder, mainFile)
        self.destroy()
    
    def onFolderSelect(self,fileChooser):
        fn = fileChooser.get_filename()
        if fn != None:
            self.builder.get_object("locationInput").set_text(fn)
  
    def onOpenProjectButtonClick(self, button):
        dialog = Gtk.FileChooserDialog("Choose a project folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,"Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        if dialog.run() == Gtk.ResponseType.OK:
            self.plugin.openProject(dialog.get_filename())
        dialog.destroy()

