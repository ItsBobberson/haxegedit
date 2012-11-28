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
#__settings.connect("changed::hxml-uri", self.onHxmlUriChange)

# Cached keybinding
__keybindingComplete = ""
__keybindingCompleteTuple = {}

__dotComplete = True

def getEscHideComplete():
    return __settings.get_boolean("esc-hide-complete")
def setEscHideComplete(v):
    __settings.set_boolean("esc-hide-complete",v)

def getEmptyHideComplete():
    return __settings.get_boolean("empty-hide-complete")
def setEmptyHideComplete(v):
    __settings.set_boolean("empty-hide-complete",v)

def getTypeOnlyHideComplete():
    return __settings.get_boolean("typeonly-hide-complete")
def setTypeOnlyHideComplete(v):
    __settings.set_boolean("typeonly-hide-complete",v)
    
def getSpaceComplete():
    return __settings.get_boolean("space-complete")
def setSpaceComplete(v):
    __settings.set_boolean("space-complete",v)
    
def getTabComplete():
    return __settings.get_boolean("tab-complete")
def setTabComplete(v):
    __settings.set_boolean("tab-complete",v)
    
def getEnterComplete():
    return __settings.get_boolean("enter-complete")
def setEnterComplete(v):
    __settings.set_boolean("enter-complete",v)
    
def getDoubleDotComplete():
    return __settings.get_boolean("double-dot-complete")
def setDoubleDotComplete(v):
    __settings.set_boolean("double-dot-complete",v)
    
def getNonAlphaComplete():
    return __settings.get_boolean("non-alpha-complete")
def setNonAlphaComplete(v):
    __settings.set_boolean("non-alpha-complete",v)


    
def getDotComplete():
    """
    Returns a boolean (as flag to toggle dot completion) from configuration file, e.g. "True"
    """
    global __dotComplete
    __dotComplete = DEFAULT_DOT_COMPLETE
    dot = __settings.get_boolean(GCONF_DOT_COMPLETE)
    
    #print "popup event.keyval %s" % event.keyval
    """
    if not dot:
        __dotComplete = DEFAULT_DOT_COMPLETE
    else:
        __dotComplete = dot
    """
    
    __dotComplete = dot
    return __dotComplete

def setDotComplete(dot):
    """
    Saves a boolean with the value used to toglle  dot code completion to the gconf entry, e.g. "False".
    """
    global __dotComplete
    __settings.set_boolean(GCONF_DOT_COMPLETE, dot)
    __dotComplete = dot
    
def getKeybindingComplete():
    """
    Returns a string with the keybinding used to do code completion from the
    configuration file, e.g. "ctrl+alt+space"
    """
    global __keybindingComplete
    # Get keybinding from cache, then gconf or else use default.
    if len(__keybindingComplete) == 0:
        keybinding = __settings.get_string(GCONF_KEYBINDING_COMPLETE)
        __keybindingCompleteTuple = {} # Invalidate cache
        if not keybinding:
            __keybindingComplete = DEFAULT_KEYBINDING_COMPLETE
        else:
            __keybindingComplete = keybinding
    
    return __keybindingComplete
    
def getKeybindingCompleteTuple():
    """
    Returns a tuple with the keybinding used to do code completion from the
    configuration file, e.g. {"alt" : True, "ctrl" : True, "key" : "space"}.
    """
    global __keybindingCompleteTuple
    # Return cached result
    if len(__keybindingCompleteTuple) != 0:
        return __keybindingCompleteTuple
        
    # Parse keybinding
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
    """
    Saves a string with the keybinding used to do code completion to the gconf
    entry, e.g. "ctrl+alt+space".
    """
    global __keybindingComplete
    global __keybindingCompleteTuple
    __settings.set_string(GCONF_KEYBINDING_COMPLETE, keybinding)
    __keybindingComplete = keybinding
    __keybindingCompleteTuple = {}

def getHxml():
    return __settings.get_string(GCONF_HXML_PATH)
    
def getHxmlFile():
	global HXML_FILE
	#return HXML_FILE
	return __settings.get_string(GCONF_HXML_PATH)
	
def setHxmlFile(newFile):
	global HXML_FILE
	HXML_FILE = newFile
	__settings.set_string(GCONF_HXML_PATH, newFile)
      
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
