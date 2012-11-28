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
        
        checkButton = Gtk.CheckButton("Use dot completion")
        checkButton.set_active(configuration.getDotComplete())
        checkButton.connect('toggled', self.on_check_button_toggled)

        self.keybindingInput = keybindingwidget.KeybindingWidget()
        self.keybindingInput.setKeybinding(keybinding)
        self.keybindingInput.connect("keybinding-changed", self.on_keybinding_changed)

        
        self.hxmlfolderLabel = Gtk.Label()
        self.fileChooserBtn = Gtk.FileChooserButton("Select HXML file",Gtk.FileChooserAction.OPEN)#,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))        
        self.fileChooserBtn.set_size_request(200, 20)
        filter = Gtk.FileFilter()
        filter.add_pattern("*.hxml")
        self.fileChooserBtn.add_filter(filter)
        self.handler_id = self.fileChooserBtn.connect("file-set", self.onHxmlFileSelect)
        self.handler_id2 = self.fileChooserBtn.connect("selection-changed", self.onHxmlFileSelect)
        oldFile = configuration.getHxmlFile()
        if oldFile != None:
            self.hxmlfolderLabel.set_text(os.path.dirname (oldFile))
            self.fileChooserBtn.set_filename(oldFile)
        
        self.hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        #self.hbox0.set_halign(Gtk.Align.FILL)
        self.hbox0.pack_start(self.hxmlfolderLabel, expand=True, fill=True, padding=0)
        self.hbox0.pack_start(self.fileChooserBtn, expand=True, fill=True, padding=0)
        
        self.table = Gtk.Table(2, 2, homogeneous=True)
        self.table.set_row_spacings(10)
        self.table.set_col_spacings(10)
        l0 = Gtk.Label("Change keybinding:")
        #l0.set_halign(Gtk.Align.END)
        self.table.attach(l0, 0, 1, 0, 1, xoptions=False, yoptions=False)
        self.table.attach(self.keybindingInput, 1, 2, 0, 1, xoptions=False, yoptions=False)
        
        l1 = Gtk.Label("Set hxml file:")
        #l1.set_halign(Gtk.Align.END)
        self.table.attach(l1, 0, 1, 1, 2, xoptions=False, yoptions=False)
        self.table.attach(self.hbox0,1 ,2 ,1 ,2 , xoptions=False, yoptions=False)

        self.btnApply = Gtk.Button(stock=Gtk.STOCK_APPLY)
        self.btnApply.set_sensitive(False)
        self.btnApply.connect("clicked", self.applyChanges)
        
        btnClear =  Gtk.Button(stock=Gtk.STOCK_CLEAR)
        btnClear.connect("clicked", self.clearChanges)
        
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.hbox.set_halign(Gtk.Align.CENTER)
        self.hbox.pack_start(self.btnApply, expand=False, fill=False, padding=0)
        self.hbox.pack_start(btnClear, expand=False, fill=False, padding=0)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.vbox.pack_start(checkButton, expand=True, fill=True, padding=0)
        self.vbox.pack_start(self.table, expand=True, fill=True, padding=0) 
        self.vbox.pack_start(self.hbox, expand=True, fill=True, padding=0)
        
        #self.vbox.set_size_request(500, 300)
        self.vbox.set_halign(Gtk.Align.CENTER)
        self.vbox.set_halign(Gtk.Align.FILL)
        self.vbox.set_valign(Gtk.Align.FILL)
        self.vbox.set_hexpand(True)
        self.vbox.set_vexpand(True)
        self.vbox.set_margin_left(50)
        self.vbox.set_margin_top(50)
        self.vbox.set_margin_right(50)
        self.vbox.set_margin_bottom(50)
        
        self.vbox.show_all()

        return self.vbox

    def onHxmlFileSelect(self,fileChooser):
        fn = fileChooser.get_filename()
        if fn != None:
            configuration.setHxmlFile(fn)
            self.hxmlfolderLabel.set_text(os.path.dirname(fn))
            
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
        
if __name__ == '__main__':
    dlg = ConfigurationDialog()
    Gtk.main()
