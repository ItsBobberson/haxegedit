from gi.repository import GObject, Gtk, Gedit, PeasGtk# Gdk, Peas, 
from KeybindingInput import KeybindingInput
import Configuration

class SettingsFrame(Gtk.Frame):
    __gtype_name__ = "SettingsFrame"

    def __init__(self, plugin):
        Gtk.Frame.__init__(self)

        self.plugin = plugin
        self.dataDir = plugin.plugin_info.get_data_dir()

        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "SettingsBox.glade")
        self.builder.connect_signals(self)


        #    Code Completion
        self.completeChanges = []
        self.keybindingComplete = Configuration.getKeybindingComplete()
        self.keybindingCompleteInput = KeybindingInput()
        self.keybindingCompleteInput.setKeybinding(self.keybindingComplete)
        self.keybindingCompleteInput.connect("keybinding-changed", self.onKeybindingCompleteInputChange)
        self.builder.get_object("completeKeybindingPlaceholder").add(self.keybindingCompleteInput)
        self.builder.get_object("useDotCompleteCheckbutton").set_active(Configuration.getDotComplete())
        self.builder.get_object("escHideCompleteBtn").set_active(Configuration.getEscHideComplete())
        self.builder.get_object("emptyHideCompleteBtn").set_active(Configuration.getEmptyHideComplete())
        self.builder.get_object("spaceCompleteBtn").set_active(Configuration.getSpaceComplete())
        self.builder.get_object("tabCompleteBtn").set_active(Configuration.getTabComplete())
        self.builder.get_object("enterCompleteBtn").set_active(Configuration.getEnterComplete())
        self.builder.get_object("nonAlphaCompleteBtn").set_active(Configuration.getNonAlphaComplete())
        self.builder.get_object("doubleDotCompleteBtn").set_active(Configuration.getDoubleDotComplete())
        
        
        #    Project
        uri = Configuration.getProjectDefaultLocation()
        if uri !=None and uri !="" and uri !="None":
            self.builder.get_object("filechooserbutton").set_current_folder_uri(uri)

        package = Configuration.getProjectDefaultPackage()
        if package ==None or package == "None":
            package = ""
        self.builder.get_object("projectDefaultPackageInput").set_text(package)
            
        main = Configuration.getProjectDefaultMain()
        if main ==None or main=="None":
            main = ""
        self.builder.get_object("projectDefaultMainInput").set_text(main)
            
        
        #    Building
        self.buildChanges = []
        self.keybindingBuild = Configuration.getKeybindingBuild()
        self.keybindingBuildInput = KeybindingInput()
        self.keybindingBuildInput.setKeybinding(self.keybindingBuild)
        self.keybindingBuildInput.connect("keybinding-changed", self.onKeybindingBuildInputChange)
        self.builder.get_object("buildKeybindingPlaceholder").add(self.keybindingBuildInput)
        self.builder.get_object("playAfterBuildCheckbutton").set_active(Configuration.getPlayAfterBuild())
        self.builder.get_object("runFileInput").set_text(Configuration.getRunFile())
        
        
        #    ToolBars and Panels
        self.builder.get_object("showToolBarHxmlCheckbutton").set_active(Configuration.getToolBarShowHxml())
        self.builder.get_object("autoHideConsoleCheckbutton").set_active(Configuration.getAutoHideConsole())
        self.builder.get_object("autoHideSidePanelCheckbutton").set_active(Configuration.getAutoHideSidePanel())

        self.add(self.builder.get_object("vbox"))
        
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.set_hexpand(False)
        self.set_vexpand(False)
                
        self.show_all()
    
    
    
    #   Code Completion
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
        
    def updateKeybindingCompleteButtons(self, flag):
        self.builder.get_object("completeKeybindingBtnApply").set_sensitive(flag)
        self.builder.get_object("completeKeybindingBtnClear").set_sensitive(flag)  

    def onUseDotCompleteToggle(self, button):
        Configuration.setDotComplete(button.get_active())
            
    def onEscHideCompleteToggle(self, button):
        Configuration.setEscHideComplete(button.get_active())
    
    def onEmptyHideCompleteToggle(self, button):
        Configuration.setEmptyHideComplete(button.get_active())
            
    def onSpaceCompleteToggle(self, button):
        Configuration.setSpaceComplete(button.get_active())
    
    def onTabCompleteToggle(self, button):
        Configuration.setTabComplete(button.get_active())
        
    def onEnterCompleteToggle(self, button):
        Configuration.setEnterComplete(button.get_active())
            
    def onNonAlphaCompleteToggle(self, button):
        Configuration.setNonAlphaComplete(button.get_active())
        
    def onDoubleDotCompleteToggle(self, button):
        Configuration.setDoubleDotComplete(button.get_active())
        
       
       
    #   Building
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
        
    def updateKeybindingBuildButtons(self, flag):
        self.builder.get_object("buildKeybindingBtnApply").set_sensitive(flag)
        self.builder.get_object("buildKeybindingBtnClear").set_sensitive(flag)
    
    def onPlayAfterBuildToggle(self, button):
        Configuration.setPlayAfterBuild(button.get_active())

    def onRunFileInputChange(self, entry):
        Configuration.setRunFile(entry.get_text())
    
    
    
    #   Create Project
    def onFolderSelect(self,fileChooser):
        fn0 = fileChooser.get_filename()
        fn = fileChooser.get_current_folder_uri()
        if fn != None:
            self.builder.get_object("projectDefaultLocationInput").set_text(fn0)
            Configuration.setProjectDefaultLocation(fn)
    
    def onProjectDefaultPackageInputChange(self, entry):
        Configuration.setProjectDefaultPackage(entry.get_text())
        
    def onProjectDefaultMainInputChange(self, entry):
        Configuration.setProjectDefaultMain(entry.get_text())
            
            
            
    #   Toolbars and panels
    def onShowToolBarHxmlToggle(self, button):
        Configuration.setToolBarShowHxml(button.get_active())
        
    def onAutoHideConsoleToggle(self, button):
        Configuration.setAutoHideConsole(button.get_active())
        
    def onAutoHideSidePanelToggle(self, button):
        Configuration.setAutoHideSidePanel(button.get_active())    
