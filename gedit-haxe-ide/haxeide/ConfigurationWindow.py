from gi.repository import GObject, Gtk, Gdk, Gedit
import string
from SettingsFrame import SettingsFrame
from ProjectFrame import ProjectFrame
from SessionFrame import SessionFrame

class ConfigurationWindow(Gtk.Window):

    def __init__(self, plugin):
        Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL);
        self.plugin = plugin
        
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.set_title("haXedit")
        self.set_icon_from_file(self.dataDir+"/"+"icons"+"/"+ "haxe_logo_24.png")
        self.set_size_request(1000,600)
        self.set_position(Gtk.WindowPosition.CENTER);

        self.notebook = Gtk.Notebook()
        self.notebook.set_margin_left(20)
        self.notebook.set_margin_top(20)
        self.notebook.set_margin_right(20)
        self.notebook.set_margin_bottom(20)
        
        self.notebook.append_page(ProjectFrame(plugin, self), Gtk.Label("Create new project"))
        self.notebook.append_page(SessionFrame(plugin, self), Gtk.Label("Sessions and Projects"))
        self.notebook.append_page(SettingsFrame(plugin), Gtk.Label("Settings"))

        self.add(self.notebook)
        
        self.show_all()
