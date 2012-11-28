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
        self.hxmlFile=""
        self.hxmlSessionPath=""
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "SessionBox.glade")
        self.builder.connect_signals(self)
        #self.builder.get_object("openProjectBtn").set_sensitive(False)
        #self.builder.get_object("openSessionBtn").set_sensitive(False)
        self.vbox = self.builder.get_object("vbox")
        self.add(self.vbox)
        
        uri = Configuration.getProjectsLocation()
        if uri !=None and uri!="":
            self.builder.get_object("filechooser").set_current_folder_uri(uri)
            
        filter = Gtk.FileFilter()
        filter.set_name("*.hxml")
        filter.add_pattern("*.hxml")
        filter.add_pattern("*.nmml")
        self.builder.get_object("filechooser").add_filter(filter)
        
        #self.builder.get_object("locationInput").set_size_request(300,20)
        self.getSessions()
        self.show_all()

    def onOpenProjectBtnClick(self, button):
        if self.builder.get_object("closeTabsCheckBox").get_active():
            self.plugin.window.close_all_tabs()
        self.plugin.openProject(self.hxmlFile)
        self.win.destroy()
        
    def onOpenSessionBtnClick(self, button):
        if self.builder.get_object("closeTabsCheckBox").get_active():
            self.plugin.window.close_all_tabs()
        self.plugin.openSession(self.hxmlSessionPath)
        self.win.destroy()
        
    def onDeleteSessionBtnClick(self, button):
        #self.sessionsHash.pop(self.hxmlSessionPath)
        del self.sessionsHash[self.hxmlSessionPath]
        Configuration.saveSessions(self.sessionsHash)
        
        self.getSessions()
        self.hxmlSessionPath = ""
        self.builder.get_object("openSessionBtn").set_sensitive(True)
        
    def onDeleteSessionFileBtnClick(self, button):
        pass        
        
    def onFileSelect(self,fileChooser):
        fn = fileChooser.get_filename()
        if fn != None:
            if fn.endswith(".hxml"):
                self.hxmlFile = fn
                self.builder.get_object("locationInput").set_text(fn)
                self.builder.get_object("openProjectBtn").set_sensitive(True)
            else:
                self.hxmlFile = ""
                self.builder.get_object("locationInput").set_text("")
                self.builder.get_object("openProjectBtn").set_sensitive(False)
                
    def getSessions(self): 
        listStore = Gtk.ListStore(str) #, list) #Gio.Icon, str, GObject.Object, Gio.FileType)
        self.sessionsHash = Configuration.getSessions()
        for key in self.sessionsHash:
            listStore.append([key])

        treeViewColumn = Gtk.TreeViewColumn("Session Identifier", Gtk.CellRendererText(), text=0)

        treeView = self.builder.get_object("treeView")
        #treeView.set_headers_visible(False)
        treeView.set_model(listStore)
        treeView.append_column(treeViewColumn)
        
        selection = treeView.get_selection()
        selection.connect('changed', self.onTreeViewSelectionChanged)
        selection.set_mode(Gtk.SelectionMode.MULTIPLE)

    def onTreeViewSelectionChanged(self,selection):
        model, rows = selection.get_selected_rows()
        if len(rows)==0:
            return
        iter = model.get_iter(rows[0])
        self.hxmlSessionPath = model[iter][0]
        if self.hxmlSessionPath.endswith ('.hxml'):
            self.builder.get_object("deleteSessionBtn").set_sensitive(True)
            self.builder.get_object("openSessionBtn").set_sensitive(True)
        """    
        print self.sessionsHash[self.hxmlSessionPath]
        for i in self.sessionsHash:
            if hxmlPath == self.sessionsHash[i][0]:
                c = 0
                while c < len(self.sessionsHash[i]):
                    if c==0:
                        print "session hxmlPath:"
                    elif c==1:
                        print "session rootDir:"
                    else:
                        print "session file:"
                    print self.sessionsHash[i][c]
                    c = c+1
        """
