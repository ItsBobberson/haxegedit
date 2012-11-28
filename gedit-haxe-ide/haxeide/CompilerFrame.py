from gi.repository import GObject, Gtk, Gdk, Gedit
import string
import Configuration

class CompilerFrame(Gtk.Frame):
    __gtype_name__ = "CompilerFrame"
    
    def __init__(self, plugin, win):
        Gtk.Frame.__init__(self)
        self.plugin = plugin
        self.win = win
        self.dataDir = plugin.plugin_info.get_data_dir()
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "CompilerBox.glade")
        self.builder.connect_signals(self)
        
        self.vbox = self.builder.get_object("vbox")
        self.add(self.vbox)
