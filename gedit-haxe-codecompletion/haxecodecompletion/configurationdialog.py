# Copyright (C) 2008 Michael Mc Donnell
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import os
from gi.repository import GObject, Gtk, Gedit, PeasGtk# Gdk, Peas, 
import logging
import keybindingwidget
import configuration

class ConfigurationDialog(): 
    __gtype_name__ = "HaxeCompletionPluginConfig"

    def __init__(self):
        pass
        #GObject.Object.__init__(self)

    def do_activate(self):
        pass

    def do_deactivate(self):
        pass

    def do_update_state(self):
        pass

    def create_widget(self):
        self.changes = []
        keybinding = configuration.getKeybindingComplete()
        self.__setKeybinding(keybinding)
        
        #Image + title box
        l = Gtk.Label()
        l.set_markup("<b>Code completion settings</b>") 
        titleBox = Gtk.HBox(homogeneous=False, spacing=10)
        titleBox.set_halign(Gtk.Align.CENTER)
        titleBox.pack_start(Gtk.Image.new_from_file("haxe_logo_32.png"), expand=True, fill=True, padding=0)
        titleBox.pack_start(l, expand=True, fill=True, padding=0)
        
        
        # Select hxml file box
        self.hxmlfolderLabel = Gtk.Label("-swf-version 9 -swf /tmp/void.swf")

        fileChooserBtn = Gtk.FileChooserButton("Select hxml file",Gtk.FileChooserAction.OPEN)#,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))        
        fileChooserBtn.set_size_request(200, 20)
        filter = Gtk.FileFilter()
        filter.set_name("*.hxml")
        filter.add_pattern("*.hxml")
        fileChooserBtn.add_filter(filter)
        self.handler_id = fileChooserBtn.connect("file-set", self.onHxmlFileSelect)
        self.handler_id2 = fileChooserBtn.connect("selection-changed", self.onHxmlFileSelect)
        
        oldFile = configuration.getHxmlFile()
        if oldFile != None:
            self.hxmlfolderLabel.set_text(os.path.dirname (oldFile))
            fileChooserBtn.set_filename(oldFile)
        
        fileChooserBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        fileChooserBox.pack_start(self.hxmlfolderLabel, expand=True, fill=True, padding=0)
        fileChooserBox.pack_start(fileChooserBtn, expand=True, fill=True, padding=0)
        
        hxmlBox = Gtk.HBox(homogeneous=False, spacing=10)
        hxmlBox.set_halign(Gtk.Align.START)
        l = Gtk.Label()
        l.set_markup("* Select hxml file:")
        hxmlBox.pack_start(l, expand=True, fill=True, padding=0)
        hxmlBox.pack_start(fileChooserBox,expand=True, fill=True, padding=0)
        
        
        # use keybinding complete box
        self.keybindingInput = keybindingwidget.KeybindingWidget()
        self.keybindingInput.setKeybinding(keybinding)
        self.keybindingInput.connect("keybinding-changed", self.on_keybinding_changed)

        useKeybindingBox = Gtk.HBox(homogeneous=False, spacing=10)
        useKeybindingBox.set_halign(Gtk.Align.START)
        useKeybindingBox.pack_start(Gtk.Label("* Show popup with keybinding:"), expand=True, fill=True, padding=0)
        useKeybindingBox.pack_start(self.keybindingInput, expand=True, fill=True, padding=0)
        
        
        # use dot complete box
        useDotCompleteBtn = Gtk.CheckButton()
        useDotCompleteBtn.set_active(configuration.getDotComplete())
        useDotCompleteBtn.connect('toggled', self.on_check_button_toggled)
        
        useDotCompletionBox = Gtk.HBox(homogeneous=False, spacing=10)
        useDotCompletionBox.set_halign(Gtk.Align.START)
        useDotCompletionBox.pack_start(Gtk.Label("* Show popup after dot:"), expand=True, fill=True, padding=0)
        useDotCompletionBox.pack_start(useDotCompleteBtn, expand=True, fill=True, padding=0)
        
        
        # popup window configuration
        escHideCompleteBtn = Gtk.CheckButton("Hide popup with <ESC>")
        escHideCompleteBtn.set_active(configuration.getEscHideComplete())
        escHideCompleteBtn.connect('toggled', self.onEscHideCompleteToggle)
        
        emptyHideCompleteBtn = Gtk.CheckButton("Hide popup when the list is empty")
        emptyHideCompleteBtn.set_active(configuration.getEmptyHideComplete())
        emptyHideCompleteBtn.connect('toggled', self.onEmptyHideCompleteToggle)
 
        spaceCompleteBtn = Gtk.CheckButton("Complete with <SPACE>")
        spaceCompleteBtn.set_active(configuration.getSpaceComplete())
        spaceCompleteBtn.connect('toggled', self.onSpaceCompleteToggle)

        tabCompleteBtn = Gtk.CheckButton("Complete with <TAB>")
        tabCompleteBtn.set_active(configuration.getTabComplete())
        tabCompleteBtn.connect('toggled', self.onTabCompleteToggle)
        
        enterCompleteBtn = Gtk.CheckButton("Complete with <ENTER>")
        enterCompleteBtn.set_active(configuration.getEnterComplete())
        enterCompleteBtn.connect('toggled', self.onEnterCompleteToggle)
        
        nonAlphaCompleteBtn = Gtk.CheckButton("Complete with non alpha numeric")
        nonAlphaCompleteBtn.set_active(configuration.getNonAlphaComplete())
        nonAlphaCompleteBtn.connect('toggled', self.onNonAlphaCompleteToggle)
        
        doubleDotCompleteBtn = Gtk.CheckButton("Complete with dot key and relaunch popup")
        doubleDotCompleteBtn.set_active(configuration.getDoubleDotComplete())
        doubleDotCompleteBtn.connect('toggled', self.onDoubleDotCompleteToggle)


        # apply clear button box
        self.btnApply = Gtk.Button(stock=Gtk.STOCK_APPLY)
        self.btnApply.set_sensitive(False)
        self.btnApply.connect("clicked", self.applyChanges)
        self.btnClear =  Gtk.Button(stock=Gtk.STOCK_CLEAR)
        self.btnClear.connect("clicked", self.clearChanges)
        
        buttonBox = Gtk.HBox(homogeneous=False, spacing=10)
        buttonBox.set_halign(Gtk.Align.CENTER)
        buttonBox.pack_start(self.btnApply, expand=False, fill=False, padding=0)
        buttonBox.pack_start(self.btnClear, expand=False, fill=False, padding=0)


        #VBox containing all widgets (to be returned for the configuration dialog)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.pack_start(titleBox, expand=True, fill=True, padding=0)
        vbox.pack_start(hxmlBox, expand=True, fill=True, padding=0)
        vbox.pack_start(useKeybindingBox, expand=True, fill=True, padding=0) 
        vbox.pack_start(useDotCompletionBox, expand=True, fill=True, padding=0)
        
        l = Gtk.Label()
        l.set_markup("<b>Popup configuration</b>")
        vbox.pack_start(l, expand=True, fill=True, padding=0)
        vbox.pack_start(escHideCompleteBtn, expand=True, fill=True, padding=0)
        vbox.pack_start(emptyHideCompleteBtn, expand=True, fill=True, padding=0)
        vbox.pack_start(spaceCompleteBtn, expand=True, fill=True, padding=0)
        vbox.pack_start(tabCompleteBtn, expand=True, fill=True, padding=0)
        vbox.pack_start(enterCompleteBtn, expand=True, fill=True, padding=0)
        vbox.pack_start(nonAlphaCompleteBtn, expand=True, fill=True, padding=0)
        vbox.pack_start(doubleDotCompleteBtn, expand=True, fill=True, padding=0)
        #vbox.pack_start(table, expand=True, fill=True, padding=0) 
        vbox.pack_start(buttonBox, expand=True, fill=True, padding=0)
        #vbox.set_size_request(500, 300)
        #vbox.set_halign(Gtk.Align.CENTER)
        #vbox.set_halign(Gtk.Align.FILL)
        #vbox.set_valign(Gtk.Align.FILL)
        #vbox.set_hexpand(True)
        #vbox.set_vexpand(True)
        vbox.set_margin_left(20)
        vbox.set_margin_top(20)
        vbox.set_margin_right(20)
        vbox.set_margin_bottom(20)
        #vbox.show_all()

        return vbox
    
    def onEscHideCompleteToggle(self, button):
        configuration.setEscHideComplete(button.get_active())
    
    def onEmptyHideCompleteToggle(self, button):
        configuration.setEmptyHideComplete(button.get_active())
            
    def onSpaceCompleteToggle(self, button):
        configuration.setSpaceComplete(button.get_active())
        
    def onEnterCompleteToggle(self, button):
        configuration.setEnterComplete(button.get_active())
        
    def onTabCompleteToggle(self, button):
        configuration.setTabComplete(button.get_active())
        
    def onNonAlphaCompleteToggle(self, button):
        configuration.setNonAlphaComplete(button.get_active())
        
    def onDoubleDotCompleteToggle(self, button):
        configuration.setDoubleDotComplete(button.get_active())

    def onHxmlFileSelect(self,fileChooser):
        fn = fileChooser.get_filename()
        if fn != None:
            configuration.setHxmlFile(fn)
            self.hxmlfolderLabel.set_text(os.path.dirname(fn) +'/')
            
    def on_check_button_toggled(self, button):
        change = (configuration.setDotComplete, button.get_active())
        self.changes.append(change)
        self.btnApply.set_sensitive(True)
        
    def __getKeybinding(self):
        return self.__keybinding
        
    def __setKeybinding(self, keybinding):
        self.__keybinding = keybinding
        
    def on_keybinding_changed(self, widget, keybinding):
        change1 = (configuration.setKeybindingComplete, keybinding)
        change2 = (self.__setKeybinding, keybinding)
        self.changes.append(change1)
        self.changes.append(change2)
        
        self.btnApply.set_sensitive(True)
        
    def clearChanges(self, widget):
        self.changes = []
        self.keybindingInput.setKeybinding(self.__getKeybinding())
        self.btnApply.set_sensitive(False)
    
    def applyChanges(self, widget):
        for change in self.changes:
            change[0](change[1])
        
        self.btnApply.set_sensitive(False)
        
    def close(self, widget, *event):
        self.hide()
        self.destroy()
        
        """
        table = Gtk.Table(2, 2, homogeneous=False)
        table.set_row_spacings(10)
        table.set_col_spacings(10)
        l0 = Gtk.Label("Show popup with keybinding:")
        #l0.set_halign(Gtk.Align.END)
        table.attach(l0, 0, 1, 0, 1, xoptions=False, yoptions=False)
        table.attach(self.keybindingInput, 1, 2, 0, 1, xoptions=False, yoptions=False)
        
        l1 = Gtk.Label("Select hxml file:")
        #l1.set_halign(Gtk.Align.END)
        table.attach(l1, 0, 1, 1, 2, xoptions=False, yoptions=False)
        #table.attach(hxmlBox,1 ,2 ,1 ,2 , xoptions=False, yoptions=False)
        """
if __name__ == '__main__':
    dlg = ConfigurationDialog()
    Gtk.main()
