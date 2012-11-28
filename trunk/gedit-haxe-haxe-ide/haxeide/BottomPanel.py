import os
from gi.repository import GObject, Gtk, Gdk, Gedit
import string


class BottomPanel(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "BottomPanel"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self, plugin):
        GObject.Object.__init__(self)
        self.plugin = plugin
        self.geditWindow = plugin.window
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("BottomPanel.glade")
        self.builder.connect_signals(self)
        self.scrolledWindow = self.builder.get_object("scrolledWindow")
        self.textView = self.builder.get_object("textView")
        self.textView.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(red=65535, green=65535, blue=65535))
        self.textView.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(red=11776, green=13312, blue=13824))
       
        self.geditBottomPanel = self.geditWindow.get_bottom_panel()
        self.geditBottomPanel.add_item(self.scrolledWindow, "haxe_bottom_panel", "haXe errors", Gtk.Image.new_from_file(os.path.join(".icons", 'haxe16.png')))# Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU))
        self.geditBottomPanel.activate_item(self.scrolledWindow)
    
    def remove(self):
        self.geditBottomPanel.remove_item(self.scrolledWindow)
    
    def setText(self, txt):
        textBuffer = self.textView.get_buffer()
        textBuffer.set_text(txt)
    
        
