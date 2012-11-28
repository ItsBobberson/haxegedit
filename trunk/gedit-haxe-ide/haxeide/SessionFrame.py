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
        
        uri = Configuration.getProjectsLocation()
        if uri !=None and uri!="":
            self.builder.get_object("filechooser").set_current_folder_uri(uri)
            
        filter = Gtk.FileFilter()
        filter.set_name("*.hxml")
        filter.add_pattern("*.hxml")
        filter.add_pattern("*.nmml")
        self.builder.get_object("filechooser").add_filter(filter)
        
        treeView = self.builder.get_object("treeView").append_column(Gtk.TreeViewColumn("Sessions", Gtk.CellRendererText(), text=0))

        self.getSessions()
        
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
        #self.sessionsHash.pop(self.hxmlSessionPath)
        del self.sessionsHash[self.hxml]
        Configuration.saveSessions(self.sessionsHash)
        
        self.getSessions()
             
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
        self.hxml = model[iter][0]
        if self.hxml.endswith ('.hxml'):
            self.builder.get_object("locationInput").set_text(self.hxml)
            self.builder.get_object("deleteSessionBtn").set_sensitive(True)
            self.builder.get_object("openProjectBtn").set_sensitive(True)
            self.builder.get_object("openSessionBtn").set_sensitive(True)
            
        else:
            self.resetButtons()
            
    def resetButtons(self):
        self.builder.get_object("locationInput").set_text("")
        self.builder.get_object("deleteSessionBtn").set_sensitive(False)
        self.builder.get_object("openSessionBtn").set_sensitive(False)
        self.builder.get_object("openProjectBtn").set_sensitive(False)
        
    def getSessions(self): 
        listStore = Gtk.ListStore(str) #, list) #Gio.Icon, str, GObject.Object, Gio.FileType)
        self.sessionsHash = Configuration.getSessions()
        for key in self.sessionsHash:
            listStore.append([key])
        self.builder.get_object("treeView").set_model(listStore)
   
    def handleCloseAllDocuments(self):
        if self.builder.get_object("closeTabsCheckBox").get_active():
            self.plugin.window.close_all_tabs()
