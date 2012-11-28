import os
from gi.repository import GObject, Gedit, Gtk

filename20b = os.path.join(".icons", 'haxe20b.png')
filename24b = os.path.join(".icons", 'haxe24b.png')

class ToolBar(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ToolBar"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self, plugin):#, geditWindow):
        GObject.Object.__init__(self)
        self.plugin = plugin
        self.geditWindow = plugin.window
        self.setup()
        self.geditWindow.connect("active-tab-changed", self.onActiveTabChange)
        self.geditWindow.connect("active-tab-state-changed", self.onActiveTabStateChange)
        self.geditWindow.connect("tab-added", self.onTabAdded)    
        self.geditWindow.connect("tab-removed", self.onTabRemoved) 
        
    def setup(self):
        vbox = self.geditWindow.get_children()[0]
        self.geditToolbar = vbox.get_children()[1]

        self.separator1 = Gtk.SeparatorToolItem()
 
        self.buildButton = Gtk.ToolButton(stock_id=Gtk.STOCK_EXECUTE) #Gtk.STOCK_MEDIA_PLAY
        self.buildButton.set_tooltip_text('Execute haXe')
        self.buildButton.connect("clicked", self.onBuildButtonClick)
        self.buildButton.set_sensitive(False)
        
        self.projectButton = Gtk.ToolButton(icon_widget=Gtk.Image.new_from_file(filename24b))
        self.projectButton.set_tooltip_text('toggle haXe workspace')
        self.projectButton.connect("clicked", self.onProjectButtonClick)

        self.hxmlButton = Gtk.ToolButton(stock_id=Gtk.STOCK_YES) 
        self.hxmlButton.set_tooltip_text('Set active document as build file')
        self.hxmlButton.connect("clicked", self.onHxmlButtonClick)
        self.hxmlButton.set_sensitive(False)
        
        self.testB = Gtk.ToolButton(stock_id=Gtk.STOCK_YES) 
        self.testB.set_tooltip_text('test')
        self.testB.connect("clicked", self.test)
        
        self.separator2 = Gtk.SeparatorToolItem()

        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.separator1)
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.projectButton )
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.buildButton )
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.hxmlButton )
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.separator2)
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.testB)
        
        self.geditToolbar.show_all()
        
    def test(self, button):
        self.plugin.test()
    
    def remove(self):
        self.geditToolbar.remove(self.separator1)
        self.geditToolbar.remove(self.buildButton)
        self.geditToolbar.remove(self.hxmlButton)
        self.geditToolbar.remove(self.projectButton)
        self.geditToolbar.remove(self.separator2)
    
    def onActiveTabStateChange(self, window):
        doc = window.get_active_document()
        if(doc != None):
            self.hxmlButton.set_sensitive(doc.get_uri_for_display().endswith(".hxml"))
        
    def onTabAdded(self, window, tab):
        doc = window.get_active_document()
        if(doc != None):
            self.hxmlButton.set_sensitive(doc.get_uri_for_display().endswith(".hxml"))
            
    def onTabRemoved(self, window, tab):
        doc = window.get_active_document()
        if(doc == None):
            self.hxmlButton.set_sensitive(False)
        else:
            self.hxmlButton.set_sensitive(doc.get_uri_for_display().endswith(".hxml"))
    
    def onActiveTabChange(self, window, tab):
        doc = window.get_active_document()
        self.hxmlButton.set_sensitive(doc.get_uri_for_display().endswith(".hxml"))
    
    def onProjectButtonClick(self, button):
        self.plugin.showProjectWindow()
    
    def onBuildButtonClick(self, button):
        self.plugin.build()
        
    def onHxmlButtonClick(self, button):
        self.plugin.setHxml()
        
    def setHxml(self, hxmlPath):
        self.hxmlButton.set_tooltip_text(hxmlPath)
        self.buildButton.set_sensitive(True)
