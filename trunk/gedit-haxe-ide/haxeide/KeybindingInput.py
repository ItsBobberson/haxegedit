"""
A widget for entering keybindings, e.g. ctr+alt+space.

Signals: keybinding-changed
"""
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

from gi.repository import GObject, Gtk, Gdk
import string

ACTIVATED_TEXT = "Press new keybinding..."
COLOR_FOCUS_IN = "white"
DEFAULT_TEXT = "None set"
WIDTH_CHARS = 18

class KeybindingInput(Gtk.EventBox):
    def __init__(self):
        Gtk.EventBox.__init__(self)
        
        self._label = Gtk.Label()
        self._label.set_text(DEFAULT_TEXT)
        self._label.set_width_chars(WIDTH_CHARS)
        self._label.set_alignment(0.0, 0.5)
        #self._label.unset_flags(Gtk.CAN_FOCUS)
        self._label.set_can_focus(False)
        self.add(self._label)
        events = Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.FOCUS_CHANGE_MASK
        self.add_events(events)
        self.active = False
        self._keybinding = []
    
    def getKeybinding(self):
        return self._keybinding
    
    def setKeybinding(self, keybinding):
        self._keybinding = keybinding
        self._label.set_text(keybinding)
        
    def do_button_press_event(self, event):
        #self.set_flags(Gtk.CAN_FOCUS)
        self.set_can_focus(True)
        self.grab_focus()
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(COLOR_FOCUS_IN))
        self.active = True

    def do_key_press_event(self, event):
        if not self.active:
            return False
        key_name = Gdk.keyval_name(event.keyval)
        
        # Deactivate on Escape
        if key_name == "Escape":
            self.deactivate()
            return True

        keybinding = []
        
        # FIXME Doesn't work with any super combination
        # FIXME What if keys are already used by another plugin?
        if key_name == "space" or key_name == "Tab" \
            or key_name in string.ascii_letters:
            # Check for Ctrl
            if event.state & Gdk.ModifierType.CONTROL_MASK:
                keybinding.append("ctrl")
            # Check for Alt
            if event.state & Gdk.ModifierType.MOD1_MASK:
                keybinding.append("alt")
            # Check for Shift
            if event.state & Gdk.ModifierType.SHIFT_MASK:
                keybinding.append("shift")

            keybinding.append(key_name.lower())
            self.setKeybinding('+'.join(keybinding))
            self.deactivate()
            self.emit("keybinding-changed", self.getKeybinding())
            return True
            
    def do_focus_out_event(self, event):
        self.deactivate()
        
    def deactivate(self):
        # Revert color back to normal
        default_bg_color = self.get_style().bg[Gtk.StateType.NORMAL]
        self.modify_bg(Gtk.StateType.NORMAL, default_bg_color)
        #self.unset_flags(Gtk.CAN_FOCUS)
        self.set_can_focus(False)
        self.active = False
        keybinding = self.getKeybinding()
        
        if not keybinding:
            self._label.set_text(DEFAULT_TEXT)
        else:
            self._label.set_text(keybinding)
        

GObject.type_register(KeybindingInput)
GObject.signal_new("keybinding-changed", KeybindingInput,
                       GObject.SignalFlags.RUN_LAST,
                       GObject.TYPE_NONE,
                       (GObject.TYPE_PYOBJECT,))
