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
#import gtk
#import gtk.gdk
from gi.repository import GObject, Gtk, Gedit, PeasGtk# Gdk, Peas, 
import logging
import keybindingwidget
import configuration

TEXT_KEYBINDING = "Change keybinding:"
TEXT_TITLE = "Configure haXe code completion"
TEXT_HXMLFILE = "hxml file:"
DEFAULT_WINDOW_WIDTH = 370
DEFAULT_WINDOW_HEIGHT = 0
LOG_NAME = "ConfigurationDialog"

log = logging.getLogger(LOG_NAME)

#class ConfigurationDialog(Gtk.Dialog):
class ConfigurationDialog():#GObject.Object)#, Gedit.AppActivatable, PeasGtk.Configurable): 
    __gtype_name__ = "HaxeCompletionPluginConfig"
    #window = GObject.property(type=Gedit.Window)
    #app = GObject.property(type=Gedit.App)

    def __init__(self):
        pass
        #GObject.Object.__init__(self)

    def do_activate(self):
        pass

    def do_deactivate(self):
        pass

    def do_update_state(self):
        pass

    #def do_create_configure_widget(self):
    def create_widget(self):
        
        #Gtk.Dialog.__init__(self)
        #self.set_border_width(5)
        #self.set_title(TEXT_TITLE)
        #self.set_default_size(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        checkButton = Gtk.CheckButton("Use dot competion")
        checkButton.set_active(configuration.getDotComplete())
        #checkButton.set_border_width(6)
        checkButton.connect('toggled', self.on_check_button_toggled)

        self.changes = []
        keybinding = configuration.getKeybindingComplete()
        log.info("Got keybinding from gconf %s" % str(keybinding))
        #label = Gtk.Label(keybinding)
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.vbox.pack_start(checkButton, True, True, 0)
        
        self.__setKeybinding(keybinding)
        
        self.table = Gtk.Table(2, 2, homogeneous=False)
        self.table.set_row_spacings(4)
        self.table.set_col_spacings(4)
        self.vbox.pack_start(self.table, expand=False, fill=False, padding=4) 
        
        lblKeybinding = Gtk.Label()
        lblKeybinding.set_text(TEXT_KEYBINDING)
        self.table.attach(lblKeybinding, 0, 1, 0, 1, xoptions=False, yoptions=False)
        
        self.__kbWidget = keybindingwidget.KeybindingWidget()
        self.__kbWidget.setKeybinding(keybinding)
        self.table.attach(self.__kbWidget, 1, 2, 0, 1, xoptions=False, yoptions=False)
        
        """
        lblhxmlfile = Gtk.Label()
        lblhxmlfile.set_text(TEXT_HXMLFILE)
        self.table.attach(lblhxmlfile,0 , 1, 1, 2, xoptions=False, yoptions=False)
        
        #self.__fcDialog = Gtk.FileChooserDialog("Select HXML file",self,Gtk.FILE_CHOOSER_ACTION_OPEN,(Gtk.STOCK_CANCEL,Gtk.RESPONSE_CANCEL,Gtk.STOCK_OPEN,Gtk.RESPONSE_OK))
        self.__fcDialog = Gtk.FileChooserDialog("Select HXML file",self,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
        oldFile = configuration.getHxmlFile()
        if oldFile != None:
        	self.__fcDialog.set_filename(oldFile)
        self.__fcDialog.connect('response',self.__closeFC,self);
        
        self.__fcWidget = Gtk.FileChooserButton(self.__fcDialog)
        
        self.table.attach(self.__fcWidget,1 ,2 ,1 ,2 , xoptions=False, yoptions=False)
        """
        
        # Buttons in the action area
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.__btnApply = Gtk.Button(stock=Gtk.STOCK_APPLY)
        self.__btnApply.set_sensitive(False)
        
        btnClear =  Gtk.Button(stock=Gtk.STOCK_CLEAR)

        self.hbox.pack_start(self.__btnApply, True, True, 0)
        self.hbox.pack_start(btnClear, True, True, 0)

        self.vbox.pack_start(self.hbox, True, True, 0)
        
        # Connect all signals
        self.__kbWidget.connect("keybinding-changed", self.on_keybinding_changed)
        
        self.__btnApply.connect("clicked", self.applyChanges)
        btnClear.connect("clicked", self.clearChanges)
        #self.connect('delete-event', self.close)
        #self.show_all()

        return self.vbox
        
    def __closeFC(dialog,response_id,user_param1,rself):
    	s = rself.__fcDialog.get_filename()
    	if user_param1 == Gtk.RESPONSE_OK:
    		configuration.setHxmlFile(s)
    	return True
    	
    def on_check_button_toggled(self, button):
        change = (configuration.setDotComplete, button.get_active())
        self.changes.append(change)
        self.__btnApply.set_sensitive(True)
        #configuration.setDotComplete(button.get_active())
        
    def __getKeybinding(self):
        return self.__keybinding
        
    def __setKeybinding(self, keybinding):
        self.__keybinding = keybinding
        
    def on_keybinding_changed(self, widget, keybinding):
        log.info("on_keybinding_changed")
        log.info("New keybinding is %s" % str(keybinding))
        change1 = (configuration.setKeybindingComplete, keybinding)
        change2 = (self.__setKeybinding, keybinding)
        self.changes.append(change1)
        self.changes.append(change2)
        
        self.__btnApply.set_sensitive(True)
        
    def clearChanges(self, widget):
        log.info("clearChanges")
        self.changes = []
        self.__kbWidget.setKeybinding(self.__getKeybinding())
        self.__btnApply.set_sensitive(False)
    
    def applyChanges(self, widget):
        log.info("applyChanges")
        # Commit changes (function pointer, data)
        for change in self.changes:
            change[0](change[1])
        
        self.__btnApply.set_sensitive(False)
        
    def close(self, widget, *event):
        log.info("close")
        self.hide()
        self.destroy()
        
if __name__ == '__main__':
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
    
    dlg = ConfigurationDialog()

    Gtk.main()
