import os
from gi.repository import GObject, Gedit, Gtk

class ToolBar(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ToolBar"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self, plugin):
        GObject.Object.__init__(self)
        self.plugin = plugin
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.geditWindow = plugin.window
        self.setup()
        
  
    def setup(self):
        vbox = self.geditWindow.get_children()[0]
        self.geditToolbar = vbox.get_children()[1]

        self.separator1 = Gtk.SeparatorToolItem()
 
        self.sessionButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_RECORD)
        self.sessionButton.set_tooltip_text('Save session')
        self.sessionButton.connect("clicked", self.saveSession)
        #print self.dataDir+"/"+"icons"+"/"+ "haxe_logo_24.png"
        
        self.projectButton = Gtk.ToolButton(icon_widget=Gtk.Image.new_from_file(self.dataDir+"/"+"icons"+"/"+ "haxe_logo_24.png"))
        self.projectButton.set_tooltip_text('open haXe project panel')
        self.projectButton.connect("clicked", self.onProjectButtonClick)
        
        self.buildButton = Gtk.ToolButton(stock_id=Gtk.STOCK_EXECUTE) #Gtk.STOCK_MEDIA_PLAY
        self.buildButton.set_tooltip_text('Build')
        self.buildButton.set_is_important(True)
        self.buildButton.set_label("no hxml")
        self.buildButton.connect("clicked", self.onBuildButtonClick)
        self.buildButton.set_sensitive(False)
        
        self.hxmlButton = Gtk.ToolButton(stock_id=Gtk.STOCK_YES)
        self.hxmlButton.set_stock_id(Gtk.STOCK_NO)
        self.hxmlButton.set_tooltip_text('Select active document as hxml build file')
        self.hxmlButton.connect("clicked", self.onHxmlButtonClick)
        self.hxmlButton.set_sensitive(False)

        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.separator1)
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.projectButton )
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.sessionButton)
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.hxmlButton )
        
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.buildButton )
        
        self.geditToolbar.show_all()
        
        self.h0 = self.geditWindow.connect("active-tab-changed", self.onActiveTabChange)
        self.h1 = self.geditWindow.connect("active-tab-state-changed", self.onActiveTabStateChange)
        self.h2 = self.geditWindow.connect("tab-added", self.onTabAdded)    
        self.h3 = self.geditWindow.connect("tab-removed", self.onTabRemoved)
        
        self.onActiveTabStateChange(self.geditWindow)

    def remove(self):
        self.geditToolbar.remove(self.separator1)
        self.geditToolbar.remove(self.sessionButton)
        self.geditToolbar.remove(self.buildButton)
        self.geditToolbar.remove(self.hxmlButton)
        self.geditToolbar.remove(self.projectButton)

        self.geditWindow.disconnect(self.h0)
        self.geditWindow.disconnect(self.h1)
        self.geditWindow.disconnect(self.h2)
        self.geditWindow.disconnect(self.h3)
    
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
    
    def saveSession(self, button):
        self.plugin.saveSession()
    
    def onProjectButtonClick(self, button):
        self.plugin.showProjectWindow()
    
    def onBuildButtonClick(self, button):
        self.plugin.saveAndBuild()
        
    def onHxmlButtonClick(self, button):
        self.plugin.setHxml()
        
    def setHxml(self, hxmlPath):
        self.hxmlButton.set_tooltip_text(hxmlPath)
        self.hxmlButton.set_stock_id(Gtk.STOCK_YES)
        self.buildButton.set_sensitive(True)
        parts = hxmlPath.split("/")
        l = len(parts)
        label = parts[l-2] + "/" + parts[l-1]
        self.buildButton.set_label(label)
