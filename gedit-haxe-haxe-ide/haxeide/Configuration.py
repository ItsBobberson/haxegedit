"""
Read and write gconf entry for python code completion. Uses caching to save
number of look-ups.

This code is alpha, it doesn't do very much input validation!
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

from gi.repository import Gio

CONSOLE_KEY_BASE = 'org.gnome.gedit.plugins.haxecodecompletion'

GCONF_KEYBINDING_COMPLETE = 'keybinding-complete'
GCONF_DOT_COMPLETE = 'dot-complete'
GCONF_HXML_PATH = "hxml-uri"
DEFAULT_KEYBINDING_COMPLETE = "ctrl+space"
DEFAULT_DOT_COMPLETE = True
MODIFIER_CTRL = "ctrl"
MODIFIER_ALT = "alt"
MODIFIER_SHIFT = "shift"
KEY = "key"
HXML_FILE = None
HAXE_EXEC_PATH = "haxe"

__settings = Gio.Settings.new("org.gnome.gedit.plugins.haxecodecompletion")
__keybindingComplete = ""
__keybindingCompleteTuple = {}


def getDotComplete():
    global __dotComplete
    __dotComplete = __settings.get_boolean(GCONF_DOT_COMPLETE)
    if not __dotComplete:
        __dotComplete = DEFAULT_DOT_COMPLETE
    return __dotComplete

def setDotComplete(dot):
    global __dotComplete
    __dotComplete = dot
    __settings.set_boolean(GCONF_DOT_COMPLETE, dot)
    
def getKeybindingComplete():
    global __keybindingComplete
    if len(__keybindingComplete) == 0:
        keybinding = __settings.get_string(GCONF_KEYBINDING_COMPLETE)
        __keybindingCompleteTuple = {} # Invalidate cache
        if not keybinding:
            __keybindingComplete = DEFAULT_KEYBINDING_COMPLETE
        else:
            __keybindingComplete = keybinding
    
    return __keybindingComplete
    
def getKeybindingCompleteTuple():
    global __keybindingCompleteTuple
    if len(__keybindingCompleteTuple) != 0:
        return __keybindingCompleteTuple

    alt = False
    ctrl = False
    shift = False
    key = ""
    keybinding = getKeybindingComplete().split('+')
    keybindingTuple = {
        MODIFIER_CTRL : False,
        MODIFIER_ALT : False,
        MODIFIER_SHIFT : False,
        KEY : ""
    }
    
    for s in keybinding:
        s = s.lower()
        if s == MODIFIER_ALT:
            keybindingTuple[MODIFIER_ALT] = True
        elif s == MODIFIER_CTRL:
            keybindingTuple[MODIFIER_CTRL] = True
        elif s == MODIFIER_SHIFT:
            keybindingTuple[MODIFIER_SHIFT] = True
        else:
            keybindingTuple[KEY] = s 
    
    __keybindingCompleteTuple = keybindingTuple
    
    return __keybindingCompleteTuple
    
def setKeybindingComplete(keybinding):
    global __keybindingComplete
    global __keybindingCompleteTuple
    __settings.set_string(GCONF_KEYBINDING_COMPLETE, keybinding)
    __keybindingComplete = keybinding
    __keybindingCompleteTuple = {}

def getHxmlFile():
	global HXML_FILE
	return HXML_FILE
	
def setHxmlFile(newFile):
	global HXML_FILE
	HXML_FILE = newFile
	setHxmlPath(HXML_FILE)
	
def setHxml(hxmlPath):
    __settings.set_string(GCONF_HXML_PATH, hxmlPath)
    
if __name__ == "__main__":
    __settings.set_string(GCONF_KEYBINDING_COMPLETE, DEFAULT_KEYBINDING_COMPLETE)
    print "Old keybindging was:", getKeybindingComplete()
    print "Old keybindging tuple was:", getKeybindingCompleteTuple()
    newKeybinding = "ctrl+space"
    print "Setting to new keybinding:", newKeybinding
    setKeybindingComplete(newKeybinding)
    print "New keybinding is:", getKeybindingComplete()
    print "New keybinding tuple is:", getKeybindingCompleteTuple()
    HXML_FILE = None
