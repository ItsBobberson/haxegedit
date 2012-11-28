import os
from gi.repository import GObject, Gedit, Gtk
import Configuration

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
        
        
        """
        self.sessionButton = Gtk.ToolButton(stock_id=Gtk.STOCK_ADD)
        self.sessionButton.connect("clicked", self.saveSession)
        
        
        self.projectsComboBox = Gtk.ComboBox()
        self.projectsComboBox.connect("changed", self.onProjectsComboBoxChange)
        listStore = Gtk.ListStore(str,str)
        self.sessionsHash = Configuration.getSessions()
        for key in self.sessionsHash:
            projectDirName = os.path.basename(os.path.dirname(key))
            listStore.append([projectDirName,key])
            
        renderer_text = Gtk.CellRendererText()
        self.projectsComboBox.pack_start(renderer_text, True)
        self.projectsComboBox.add_attribute(renderer_text, "text", 0)
        self.projectsComboBox.set_entry_text_column(0)
        self.projectsComboBox.set_model(listStore)
        
        self.projectsComboBoxToolItem = Gtk.ToolItem()
        self.projectsComboBoxToolItem.add(self.projectsComboBox)
        """
        self.projectsButton = Gtk.MenuToolButton()
        self.menu = Gtk.Menu()
        item = Gtk.MenuItem("save session")
        item.connect("activate", self.saveSession)
        
        self.menu.add(item)
        self.menu.add(Gtk.SeparatorMenuItem())
        
        self.sessionsHash = Configuration.getSessions()
        for key in self.sessionsHash:
            projectDirName = os.path.basename(os.path.dirname(key))
            item = Gtk.MenuItem(projectDirName)
            item.connect("activate", self.onProjectsChange, key)
            self.menu.add(item)
        self.menu.show_all()
        self.projectsButton.set_menu(self.menu)
        
        self.haxeButton = Gtk.ToolButton(icon_widget=Gtk.Image.new_from_file(self.dataDir+"/"+"icons"+"/"+ "haxe_logo_24.png"))
        self.haxeButton.connect("clicked", self.onHaxeButtonClick)
        
        self.buildButton = Gtk.ToolButton(stock_id=Gtk.STOCK_EXECUTE) #Gtk.STOCK_MEDIA_PLAY
        self.buildButton.set_is_important(True)
        self.buildButton.connect("clicked", self.onBuildButtonClick)
        
        self.hxmlButton = Gtk.ToolButton(stock_id=Gtk.STOCK_PROPERTIES)
        self.hxmlButton.connect("clicked", self.onHxmlButtonClick)
        
        #self.debugButton = Gtk.ToolButton(stock_id=Gtk.STOCK_GOTO_LAST)
        #self.debugButton.connect("clicked", self.onDebugButtonClick)
        
        self.resetButtons()
        
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.separator1)
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.projectsButton)
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.haxeButton)
        
        #self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.sessionButton)
        #self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.debugButton)
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.hxmlButton)
        self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.buildButton)
        
        self.geditToolbar.show_all()
        
        #self.geditToolbar.insert(pos = len(self.geditToolbar.get_children()),item = self.projectsComboBoxToolItem)

        self.h0 = self.geditWindow.connect("active-tab-changed", self.onActiveTabChange)
        self.h1 = self.geditWindow.connect("active-tab-state-changed", self.onActiveTabStateChange)
        self.h2 = self.geditWindow.connect("tab-added", self.onTabAdded)    
        self.h3 = self.geditWindow.connect("tab-removed", self.onTabRemoved)
        
        self.onActiveTabStateChange(self.geditWindow)
        
    def resetButtons(self):
        #self.sessionButton.set_tooltip_text('Save session')
        #self.sessionButton.set_sensitive(False)
        
        #self.debugButton.set_tooltip_text('Debugger')
        #self.debugButton.set_sensitive(False)
        
        self.haxeButton.set_tooltip_text('Open haXe panel')
        self.projectsButton.set_sensitive(True)
        
        self.projectsButton.set_tooltip_text('Open session')
        self.projectsButton.set_sensitive(True)
        
        self.buildButton.set_tooltip_text('Build project')
        self.buildButton.set_is_important(True)
        self.buildButton.set_label("no hxml")
        self.buildButton.set_sensitive(False)
        
        #self.hxmlButton.set_stock_id(Gtk.STOCK_NO)
        self.hxmlButton.set_tooltip_text('Select active document as hxml')
        self.hxmlButton.set_sensitive(False)
        
    def remove(self):
        self.geditToolbar.remove(self.separator1)
        #self.geditToolbar.remove(self.debugButton)
        self.geditToolbar.remove(self.projectsButton)
        #self.geditToolbar.remove(self.sessionButton)
        self.geditToolbar.remove(self.buildButton)
        self.geditToolbar.remove(self.hxmlButton)
        self.geditToolbar.remove(self.haxeButton)

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
    
    def onProjectsChange(self, item, data):
        self.plugin.window.close_all_tabs()
        self.plugin.openSession(data, True, True)
    """    
    def onProjectsComboBoxChange(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            folder, hxml = model[tree_iter][:2]
            self.plugin.window.close_all_tabs()
            self.plugin.openSession(hxml, True, True)
        else:
            entry = combo.get_child()
            print "Entered: %s" % entry.get_text()
    """    
    def onHaxeButtonClick(self, button):
        self.plugin.showHaxeWindow()
    
    def onBuildButtonClick(self, button):
        self.plugin.saveAndBuild()
        
    def onHxmlButtonClick(self, button):
        self.plugin.setActiveDocAsHxml()
    """    
    def onDebugButtonClick(self, button):
        self.plugin.debug()
    """    
    def setHxml(self, hxml):
        if hxml=="" or hxml == None:
            self.resetButtons()
            return

        parts = hxml.split("/")
        l = len(parts)
        label = parts[l-2] + "/" + parts[l-1]
        
        self.buildButton.set_label(label)
        self.buildButton.set_sensitive(True)
        #self.debugButton.set_sensitive(True)
        self.hxmlButton.set_tooltip_text(hxml)
        #self.sessionButton.set_sensitive(True)
        
        
