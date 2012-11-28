from gi.repository import GObject, Gtk, Gdk, Gedit
import string
import os
import Configuration

class SessionFrame(Gtk.Frame):
    __gtype_name__ = "SessionFrame"
    
    def __init__(self, plugin, win):
        Gtk.Frame.__init__(self)
        self.plugin = plugin
        self.win = win
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.hxml=""

        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "SessionBox.glade")
        self.builder.connect_signals(self)

        self.vbox = self.builder.get_object("hbox")
        self.add(self.vbox)
        
        uri = Configuration.getProjectDefaultLocation()
        if uri !=None and uri!="":
            self.builder.get_object("filechooser").set_current_folder_uri(uri)
            
        filter = Gtk.FileFilter()
        filter.set_name("*.hxml")
        filter.add_pattern("*.hxml")
        filter.add_pattern("*.nmml")
        self.builder.get_object("filechooser").add_filter(filter)
        self.builder.get_object("treeView").append_column(Gtk.TreeViewColumn("Sessions", Gtk.CellRendererText(), text=0))
        
        self.sessionsToolBar = self.builder.get_object("sessionsToolBar")

        self.lessButton = Gtk.ToolButton(stock_id=Gtk.STOCK_GO_BACK)
        self.lessButton.connect("clicked", self.onLessButtonClick)
        self.lessButton.set_tooltip_text('Show more.')

        self.moreButton = Gtk.ToolButton(stock_id=Gtk.STOCK_GO_FORWARD)
        self.moreButton.connect("clicked", self.onMoreButtonClick)
        self.moreButton.set_tooltip_text('Show less.')

        self.deleteSessionBtn = Gtk.ToolButton(stock_id=Gtk.STOCK_DELETE)
        self.deleteSessionBtn.connect("clicked", self.onDeleteSessionBtnClick)
        self.deleteSessionBtn.set_tooltip_text('Delete session from history.')
        
        self.toggleHxmlBtn = Gtk.ToggleToolButton(stock_id=Gtk.STOCK_PROPERTIES)
        #self.toggleHxmlBtn.set_is_important(True)
        #self.toggleHxmlBtn.set_label("show hxml")
        self.toggleHxmlBtn.connect("clicked", self.onToggleHxmlBtnClick)
        self.toggleHxmlBtn.set_tooltip_text('Show hxml file in path.')
        
        self.sessionsToolBar.insert(pos = len(self.sessionsToolBar.get_children()), item = self.deleteSessionBtn)
        self.sessionsToolBar.insert(pos = len(self.sessionsToolBar.get_children()), item = Gtk.SeparatorToolItem())
        
        self.sessionsToolBar.insert(pos = len(self.sessionsToolBar.get_children()), item = self.lessButton)
        self.sessionsToolBar.insert(pos = len(self.sessionsToolBar.get_children()), item = self.moreButton)
        self.sessionsToolBar.insert(pos = len(self.sessionsToolBar.get_children()), item = Gtk.SeparatorToolItem())
        self.sessionsToolBar.insert(pos = len(self.sessionsToolBar.get_children()), item = self.toggleHxmlBtn)
        
        self.sessionsToolBar.show_all()
        
        Configuration.settings().connect("changed::sessions", self.getSessions)
        Configuration.settings().connect("changed::session-path-offset", self.getSessions)
        Configuration.settings().connect("changed::session-path-show-hxml", self.getSessions)

        self.getSessions(None, None)
        self.show_all()

    def onOpenProjectBtnClick(self, button):
        self.handleCloseAllDocuments()
        self.plugin.openProject(self.hxml, self.builder.get_object("useHxmlCheckBox").get_active(), self.builder.get_object("setRootCheckBox").get_active())
        self.win.destroy()
        
    def onOpenSessionBtnClick(self, button):
        self.handleCloseAllDocuments()
        self.plugin.openSession(self.hxml, self.builder.get_object("useHxmlCheckBox").get_active(), self.builder.get_object("setRootCheckBox").get_active())
        self.win.destroy()
     
    def onDeleteSessionBtnClick(self, button):
        del self.sessionsHash[self.hxml]
        Configuration.saveSessions(self.sessionsHash)
    
    def onLessButtonClick(self, button):
        Configuration.decrementSessionPathOffset()
        
    def onMoreButtonClick(self, button):
        Configuration.incrementSessionPathOffset()
        
    def onToggleHxmlBtnClick(self, button):
        Configuration.setSessionPathShowHxml(button.get_active())
        
    def onDeleteSessionFileBtnClick(self, button):
        pass        
        
    def onFileSelect(self,fileChooser):
        fn = fileChooser.get_filename()
        if fn != None and fn.endswith(".hxml"):
            self.hxml = fn
            self.builder.get_object("locationInput").set_text(fn)
            self.builder.get_object("openProjectBtn").set_sensitive(True)
            self.builder.get_object("openSessionBtn").set_sensitive(self.hxml in self.sessionsHash)
        else:
            self.resetButtons()
                
    def onTreeViewSelectionChanged(self,selection):
        model, rows = selection.get_selected_rows()
        if len(rows)==0:
            self.resetButtons()
            return
        iter = model.get_iter(rows[0])
        self.hxml = model[iter][1]
        if self.hxml.endswith ('.hxml'):
            self.builder.get_object("locationInput").set_text(self.hxml)
            self.builder.get_object("openProjectBtn").set_sensitive(True)
            self.builder.get_object("openSessionBtn").set_sensitive(True)
            self.deleteSessionBtn.set_sensitive(True)
        else:
            self.resetButtons()
            
    def resetButtons(self):
        self.builder.get_object("locationInput").set_text("")
        self.builder.get_object("openSessionBtn").set_sensitive(False)
        self.builder.get_object("openProjectBtn").set_sensitive(False)
        self.deleteSessionBtn.set_sensitive(False)
        
    def getSessions(self, settings, key):
        self.sessionsHash = Configuration.getSessions()
        showHxml = Configuration.getSessionPathShowHxml()
        self.toggleHxmlBtn.set_active(showHxml)
        offset = Configuration.getSessionPathOffset()
        listStore = Gtk.ListStore(str, str)
        for key in self.sessionsHash:
            parts = key.split("/")
            available = len(parts)-1
            label = ""
            if offset < available:
                label = "/".join(parts[offset:-1])
            if showHxml:
                label = label + "/" + parts[-1]
            listStore.append([label, key])
        self.builder.get_object("treeView").set_model(listStore)
   
    def handleCloseAllDocuments(self):
        if self.builder.get_object("closeTabsCheckBox").get_active():
            self.plugin.window.close_all_tabs()
