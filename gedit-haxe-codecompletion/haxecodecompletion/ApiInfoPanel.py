import os
from gi.repository import GObject, Gtk, Gdk, Gedit, Gio, GLib
import string

class ApiInfoPanel(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ApiInfoPanel"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self, plugin):
        GObject.Object.__init__(self)
        self.plugin = plugin
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.geditWindow = plugin.window
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "ApiInfoWindow.glade")
        self.builder.connect_signals(self)
        
        self.scrolledWindow = self.builder.get_object("scrolledWindow")
        
        self.textView = self.builder.get_object("textView")
        self.textView.set_editable (False)
        self.textView.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(red=65535, green=65535, blue=65535))
        self.textView.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(red=11776, green=13312, blue=13824))
        self.textView.modify_bg(Gtk.StateType.SELECTED, Gdk.Color(red=51776, green=0, blue=0))
        #self.textView.connect("button-press-event", self.onTextViewClick)

        self.geditBottomPanel = self.geditWindow.get_bottom_panel()
        self.geditBottomPanel.add_item(self.scrolledWindow, "haxe_api_info_panel", "api info", Gtk.Image.new_from_file(self.dataDir + "/" + "icons" + "/" + "haxe_logo_16.png"))# Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU))
        self.geditBottomPanel.activate_item(self.scrolledWindow)
        
    def activate(self):
        self.geditBottomPanel.activate_item(self.scrolledWindow)
        
    def remove(self):
        self.geditBottomPanel.remove_item(self.scrolledWindow)
    
    def setText(self, txt):
        textBuffer = self.textView.get_buffer()
        textBuffer.set_text(txt)
        
    def appendText(self, txt):
        textBuffer = self.textView.get_buffer()
        textBuffer.insert(textBuffer.get_end_iter(), txt)
        self.textView.scroll_mark_onscreen(textBuffer.get_insert())
        #self.textView.scroll_to_mark(textBuffer.get_insert(), 0)    
        
    def onTextViewClick(self, textView, event):
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            hyperLink = self.parseHyperLinkLine()
            if hyperLink == None:
                return True
            
            return True
        
    def parseHyperLinkLine(self):
        doc = self.textView.get_buffer()
        iter = doc.get_iter_at_mark(doc.get_insert())
        lineStart = iter.copy()
        lineEnd = iter.copy()
        lineStart.set_offset (iter.get_offset () - iter.get_line_offset ())
        
        #get the complete line
        lineEnd.forward_to_line_end()
        currentLine = unicode (doc.get_text (lineStart, lineEnd, include_hidden_chars=True))
        if len(currentLine)==0:
            return None
        #print currentLine;
        return None
