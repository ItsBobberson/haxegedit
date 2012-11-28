from gi.repository import GObject, Gtk, Gedit, PeasGtk# Gdk, Peas, 
from KeybindingInput import KeybindingInput
import Configuration

class SettingsFrame(Gtk.Frame):
    __gtype_name__ = "SettingsFrame"

    def __init__(self, plugin):
        Gtk.Frame.__init__(self)

        self.plugin = plugin
        self.dataDir = plugin.plugin_info.get_data_dir()
        
        self.completeChanges = []
        self.buildChanges = []
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "SettingsBox.glade")
        self.builder.connect_signals(self)
        
        self.builder.get_object("useDotCompleteCheckbutton").set_active(Configuration.getDotComplete())
        self.builder.get_object("autoHideConsoleCheckbutton").set_active(Configuration.getAutoHideConsole())
        self.builder.get_object("autoHideSidePanelCheckbutton").set_active(Configuration.getAutoHideSidePanel())
        uri = Configuration.getProjectsLocation()
        if uri !=None and uri!="":
            self.builder.get_object("filechooserbutton").set_current_folder_uri(uri)
        
        self.setKeybindingComplete(Configuration.getKeybindingComplete())
        self.setKeybindingBuild(Configuration.getKeybindingBuild())

        self.keybindingBuildInput = KeybindingInput()
        self.keybindingBuildInput.setKeybinding(self.keybindingBuild)
        self.keybindingBuildInput.connect("keybinding-changed", self.onKeybindingBuildInputChange)
        self.builder.get_object("buildKeybindingPlaceholder").add(self.keybindingBuildInput)
        
        self.keybindingCompleteInput = KeybindingInput()
        self.keybindingCompleteInput.setKeybinding(self.keybindingComplete)
        self.keybindingCompleteInput.connect("keybinding-changed", self.onKeybindingCompleteInputChange)
        self.builder.get_object("completeKeybindingPlaceholder").add(self.keybindingCompleteInput)

        self.add(self.builder.get_object("vbox"))
        
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.set_hexpand(False)
        self.set_vexpand(False)
        
        self.show_all()
    
    # Keybinding for Completion   
     
    def getKeybindingComplete(self):
        return self.keybindingComplete
   
    def setKeybindingComplete(self, keybinding):
        self.keybindingComplete = keybinding
 
    def onKeybindingCompleteInputChange(self, widget, keybinding):
        change1 = (Configuration.setKeybindingComplete, keybinding)
        change2 = (self.setKeybindingComplete, keybinding)
        self.completeChanges.append(change1)
        self.completeChanges.append(change2)
        self.updateKeybindingCompleteButtons(True)
        
    def clearKeybindingCompleteChanges(self, widget):
        self.completeChanges = []
        self.keybindingCompleteInput.setKeybinding(self.getKeybindingComplete())
        self.updateKeybindingCompleteButtons(False)
    
    def applyKeybindingCompleteChanges(self, widget):
        for change in self.completeChanges:
            change[0](change[1])
        self.updateKeybindingCompleteButtons(False)


    # Keybinding for Building
    
    def getKeybindingBuild(self):
        return self.keybindingBuild    
        
    def setKeybindingBuild(self, keybinding):
        self.keybindingBuild = keybinding
                    
    def onKeybindingBuildInputChange(self, widget, keybinding):
        change1 = (Configuration.setKeybindingBuild, keybinding)
        change2 = (self.setKeybindingBuild, keybinding)
        self.buildChanges.append(change1)
        self.buildChanges.append(change2)
        self.updateKeybindingBuildButtons(True)

    def clearKeybindingBuildChanges(self, widget):
        self.buildChanges = []
        self.keybindingBuildInput.setKeybinding(self.keybindingBuild)
        self.updateKeybindingBuildButtons(False)

    def applyKeybindingBuildChanges(self, widget):
        for change in self.buildChanges:
            change[0](change[1])
        self.updateKeybindingBuildButtons(False)
    
    
    #various flags

    def onUseDotCompleteToggle(self, button):
        Configuration.setDotComplete(button.get_active())
        
    def onAutoHideConsoleToggle(self, button):
        Configuration.setAutoHideConsole(button.get_active())
        
    def onAutoHideSidePanelToggle(self, button):
        Configuration.setAutoHideSidePanel(button.get_active())
        
    #Button state handling
    def updateKeybindingCompleteButtons(self, flag):
        self.builder.get_object("completeKeybindingBtnApply").set_sensitive(flag)
        self.builder.get_object("completeKeybindingBtnClear").set_sensitive(flag)
        
    def updateKeybindingBuildButtons(self, flag):
        self.builder.get_object("buildKeybindingBtnApply").set_sensitive(flag)
        self.builder.get_object("buildKeybindingBtnClear").set_sensitive(flag)

    #Default project folder location
    def onFolderSelect(self,fileChooser):
        fn0 = fileChooser.get_filename()
        fn = fileChooser.get_current_folder_uri()
        if fn != None:
            self.builder.get_object("projectsLocationInput").set_text(fn0)
            Configuration.setProjectsLocation(fn)
