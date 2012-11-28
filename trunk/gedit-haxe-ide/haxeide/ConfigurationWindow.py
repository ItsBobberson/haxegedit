from gi.repository import GObject, Gtk, Gdk, Gedit
import string
from SettingsFrame import SettingsFrame
from ProjectFrame import ProjectFrame

class ConfigurationWindow(Gtk.Window):

    def __init__(self, plugin):
        Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL);
        self.plugin = plugin
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.set_title("Haxe Configuration Window")
        self.set_size_request(1000,600)

        self.notebook = Gtk.Notebook()

        self.notebook.append_page(ProjectFrame(plugin, self), Gtk.Label("Create new project"))
        self.notebook.append_page(Gtk.Label("projects and sessions (TODO)"), Gtk.Label("Sessions and Projects"))
        self.notebook.append_page(SettingsFrame(plugin), Gtk.Label("Settings"))
        
        self.notebook.set_margin_left(20)
        self.notebook.set_margin_top(20)
        self.notebook.set_margin_right(20)
        self.notebook.set_margin_bottom(20)

        self.add(self.notebook)
        self.show_all()
