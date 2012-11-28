import Configuration
import os
from gi.repository import GObject, Gtk, Gdk, Gedit, Gio, GLib
import string

class DebuggerInfoPanel(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "DebuggerInfoPanel"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self, plugin):
        GObject.Object.__init__(self)
        self.plugin = plugin
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.geditWindow = plugin.window
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "DebuggerInfoBox.glade")
        self.builder.connect_signals(self)
        
        self.scrolledWindow = self.builder.get_object("scrolledWindow")
           
        self.toolbar = self.builder.get_object("toolbar")
        self.refreshButton = Gtk.ToolButton(stock_id=Gtk.STOCK_REFRESH)
        self.refreshButton.connect("clicked", self.onRefreshButtonClick)
        self.refreshButton.set_tooltip_text('Refresh all')
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.refreshButton)
        self.toolbar.show_all()
        
        self.geditSidePanel = self.geditWindow.get_side_panel()
        self.geditSidePanel.add_item(self.scrolledWindow, "haxe_debugger_info_panel", "Debugger info", Gtk.Image.new_from_file(self.dataDir + "/" + "icons" + "/" + "haxe_logo_16.png")) #Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU))
        self.geditSidePanel.activate_item(self.scrolledWindow)
        
    def activate(self):
        self.geditSidePanel.activate_item(self.scrolledWindow)
            
    def remove(self):
        self.geditSidePanel.remove_item(self.scrolledWindow)
 
    def onRefreshButtonClick(self, button):
        self.setStack()
        self.setLocals()
        self.setArgs()
        self.setThis()
        self.setBreakPoints()
        self.setFiles()
        self.setVariables()
        #self.setFunctions()
        #self.setScopeChain()
        
    def setFiles(self):
        filesTreeView = self.builder.get_object("filesTreeView")
        if len(filesTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("file", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            filesTreeView.append_column(col)
        result = self.plugin.sendDebugInfoCommand("info files")
        lines = result.split("\n")
        ls = Gtk.ListStore(str)
        for line in lines:
            if line != '(fdb)':
                ls.append([line])       
        filesTreeView.set_model(ls)
        
    def setLocals(self):
        localsTreeView = self.builder.get_object("localsTreeView")
        if len(localsTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("key", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            localsTreeView.append_column(col)
            col = Gtk.TreeViewColumn("value", Gtk.CellRendererText(), text=1)
            col.set_resizable(True)
            localsTreeView.append_column(col)  
        result = self.plugin.sendDebugInfoCommand("info locals")
        lines = result.split("\n")
        ls = Gtk.ListStore(str, str)
        for line in lines:
            if line != '(fdb)':
                parts = line.split(" = ")
                if len(parts)==2:
                    ls.append([parts[0], parts[1]])      
        localsTreeView.set_model(ls)
        
    def setVariables(self):
        varsTreeView = self.builder.get_object("varsTreeView")
        if len(varsTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("key", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            varsTreeView.append_column(col)
            col = Gtk.TreeViewColumn("value", Gtk.CellRendererText(), text=1)
            col.set_resizable(True)
            varsTreeView.append_column(col)
        result = self.plugin.sendDebugInfoCommand("info variables")
        lines = result.split("\n")
        ls = Gtk.ListStore(str, str)
        for line in lines:
            if line != '(fdb)':
                parts = line.split(" = ")
                if len(parts)==2:
                    ls.append([parts[0], parts[1]])      
        varsTreeView.set_model(ls)
            
    def setArgs(self):
        argsTreeView = self.builder.get_object("argsTreeView")
        if len(argsTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("key", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            argsTreeView.append_column(col)
            col = Gtk.TreeViewColumn("value", Gtk.CellRendererText(), text=1)
            col.set_resizable(True)
            argsTreeView.append_column(col)
        result = self.plugin.sendDebugInfoCommand("info arguments")
        lines = result.split("\n")
        ls = Gtk.ListStore(str, str)
        for line in lines:
            if line != '(fdb)':
                parts = line.split(" = ")
                if len(parts)==2:
                    ls.append([parts[0], parts[1]])      
        argsTreeView.set_model(ls)
        
    def setStack(self):
        stackTreeView = self.builder.get_object("stackTreeView")
        stackTreeView.set_headers_visible(False)
        if len(stackTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("info stack", Gtk.CellRendererText(), text=0)
            col.set_resizable (True) 
            stackTreeView.append_column(col)
        result = self.plugin.sendDebugInfoCommand("info stack")
        lines = result.split("\n")
        ls = Gtk.ListStore(str)
        for line in lines:
            if line != '(fdb)':
                parts = line.split(" at ")
                ls.append([parts[-1]])
        stackTreeView.set_model(ls)
        
    def setBreakPoints(self):    
        breakPointsTreeView = self.builder.get_object("breakPointsTreeView")
        if len(breakPointsTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            breakPointsTreeView.append_column(col)
        result = self.plugin.sendDebugInfoCommand("info breakpoints")
        lines = result.split("\n")
        ls = Gtk.ListStore(str)
        for line in lines:
            if line != '(fdb)' and not line.startswith("  "):
                ls.append([line])
        breakPointsTreeView.set_model(ls)
        
    def setThis(self):
        thisTreeView = self.builder.get_object("thisTreeView")
        if len(thisTreeView.get_columns()) == 0:
            col = Gtk.TreeViewColumn("key", Gtk.CellRendererText(), text=0)
            col.set_resizable(True)
            thisTreeView.append_column(col)
            
            col = Gtk.TreeViewColumn("value", Gtk.CellRendererText(), text=1)
            col.set_resizable(True)
            thisTreeView.append_column(col)
        result = self.plugin.sendDebugInfoCommand("print this.")
        lines = result.split("\n")
        ls = Gtk.ListStore(str, str)
        for line in lines:
            if line != '(fdb)':
                parts = line.split(" = ")
                if len(parts)==3:
                    self.builder.get_object("thisLabel").set_text("["+ parts[-1].split(", ")[-1])
                if len(parts)==2:
                    ls.append([parts[0], parts[1]])      
        thisTreeView.set_model(ls)
