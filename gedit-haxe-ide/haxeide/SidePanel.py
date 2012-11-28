import os
from gi.repository import GObject, Gedit, Gtk, Gdk

filename20b = os.path.join(".icons", 'haxe20b.png')
filename24b = os.path.join(".icons", 'haxe24b.png')

class SidePanel(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "SidePanelBar"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self, plugin):
        GObject.Object.__init__(self)
        self.plugin = plugin
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.geditWindow = plugin.window
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" +"SidePanel.glade")
        self.builder.connect_signals(self)
        
        self.vbox = self.builder.get_object('vbox')
        self.hxmlTextView = self.builder.get_object('hxmlTextView')
        self.hxmlTextView.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(red=65535, green=65535, blue=65535))
        self.hxmlTextView.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(red=11776, green=13312, blue=13824))

        self.geditSidePanel = self.geditWindow.get_side_panel()
        self.geditSidePanel.add_item(self.vbox, "haxe_side_panel", "haXe", Gtk.Image.new_from_file(filename20b)) #Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU))
        self.geditSidePanel.activate_item(self.vbox)
        
    def onNewProjectButtonClick(self, button):
        dialog = Gtk.FileChooserDialog("Choose a destination folder", self.window, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,"Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print "Select clicked"
            print "Folder selected: " + dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print "Cancel clicked"
        dialog.destroy()
        
    def remove(self):
        self.geditSidePanel.remove_item(self.vbox)
        
    def setHxml(self, hxmlPath, hxmlName, hxmlText):
        self.builder.get_object('hxmlLabel').set_tooltip_text(hxmlPath)
        self.builder.get_object('hxmlInput').set_text(hxmlName)
        self.builder.get_object('hxmlTextView').get_buffer().set_text(hxmlText)
    
