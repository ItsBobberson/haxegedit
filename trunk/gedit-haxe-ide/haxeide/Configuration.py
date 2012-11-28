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
GCONF_KEYBINDING_BUILD = 'keybinding-build'
GCONF_DOT_COMPLETE = 'dot-complete'
GCONF_TOOLBAR_SHOW_HXML = 'toolbar-show-hxml'
GCONF_DOT_AUTO_HIDE_CONSOLE = 'auto-hide-console'
GCONF_DOT_AUTO_HIDE_SIDE_PANEL = 'auto-hide-side-panel'
GCONF_HXML_PATH = "hxml-uri"

GCONF_DEBUG_FILES = "debug-history"
GCONF_SESSIONS = "sessions"
GCONF_SESSION_PATH_OFFSET = "session-path-offset"
GCONF_SESSION_PATH_SHOW_HXML = "session-path-show-hxml"
GCONF_BUILD_PATH_SHOW_HXML = "build-path-show-hxml"
GCONF_PLAY_AFTER_BUILD = "play-after-build"
GCONF_RUN_FILE = "run-file"

GCONF_PROJECT_DEFAULT_LOCATION = "project-default-location"
GCONF_PROJECT_DEFAULT_PACKAGE = "project-default-package"
GCONF_PROJECT_DEFAULT_MAIN = "project-default-main"

DEFAULT_KEYBINDING_COMPLETE = "ctrl+space"
DEFAULT_KEYBINDING_BUILD = "shift+space"
DEFAULT_DOT_COMPLETE = True
DEFAULT_PROJECT_DEFAULT_LOCATION = ""

MODIFIER_CTRL = "ctrl"
MODIFIER_ALT = "alt"
MODIFIER_SHIFT = "shift"
KEY = "key"

HXML_FILE = None
HAXE_EXEC_PATH = "haxe"
   
__settings = Gio.Settings.new("org.gnome.gedit.plugins.haxecodecompletion")

__keybindingComplete = ""
__keybindingCompleteTuple = {}

__keybindingBuild = ""
__keybindingBuildTuple = {}

def settings():
    return __settings


"""
GCONF_PROJECT_DEFAULT_LOCATION
"""     
def setProjectDefaultLocation(path):
    __settings.set_string(GCONF_PROJECT_DEFAULT_LOCATION, path)

def getProjectDefaultLocation():
    s = __settings.get_string(GCONF_PROJECT_DEFAULT_LOCATION)
    if s == None or s == "":
    	return ""
    else:
        return s

"""
GCONF_PROJECT_DEFAULT_PACKAGE
"""  
def setProjectDefaultPackage(package):
    __settings.set_string(GCONF_PROJECT_DEFAULT_PACKAGE, package)

def getProjectDefaultPackage():
    return __settings.get_string(GCONF_PROJECT_DEFAULT_PACKAGE)

"""
GCONF_PROJECT_DEFAULT_MAIN
"""  
def setProjectDefaultMain(main):
    __settings.set_string(GCONF_PROJECT_DEFAULT_MAIN, main)

def getProjectDefaultMain():
    return __settings.get_string(GCONF_PROJECT_DEFAULT_MAIN)

        
"""
GCONF_DOT_COMPLETE
""" 
def getDotComplete():
    global __dotComplete
    __dotComplete = __settings.get_boolean(GCONF_DOT_COMPLETE)
    if __dotComplete == None:
        __dotComplete = DEFAULT_DOT_COMPLETE
    return __dotComplete

def setDotComplete(dot):
    global __dotComplete
    __dotComplete = dot
    __settings.set_boolean(GCONF_DOT_COMPLETE, dot)
    
"""
esc-hide-complete
"""     
def getEscHideComplete():
    return __settings.get_boolean("esc-hide-complete")
def setEscHideComplete(v):
    __settings.set_boolean("esc-hide-complete",v)

"""
typeonly-hide-complete
""" 
def getTypeOnlyHideComplete():
    return __settings.get_boolean("typeonly-hide-complete")
def setTypeOnlyHideComplete(v):
    __settings.set_boolean("typeonly-hide-complete",v)
    
"""
empty-hide-complete
""" 
def getEmptyHideComplete():
    return __settings.get_boolean("empty-hide-complete")
def setEmptyHideComplete(v):
    __settings.set_boolean("empty-hide-complete",v)

"""
space-complete
"""    
def getSpaceComplete():
    return __settings.get_boolean("space-complete")
def setSpaceComplete(v):
    __settings.set_boolean("space-complete",v)
    
"""
show-api-info-panel
"""    
def getShowApiInfoPanel():
    return __settings.get_boolean("show-api-info-panel")
def setShowApiInfoPanel(v):
    __settings.set_boolean("show-api-info-panel",v)

"""
auto-hide-api-info-panel
"""    
def getAutoHideApiInfoPanel():
    return __settings.get_boolean("auto-hide-api-info-panel")
def setAutoHideApiInfoPanel(v):
    __settings.set_boolean("auto-hide-api-info-panel",v)

"""
tab-complete
"""   
def getTabComplete():
    return __settings.get_boolean("tab-complete")
def setTabComplete(v):
    __settings.set_boolean("tab-complete",v)

"""
enter-complete
"""     
def getEnterComplete():
    return __settings.get_boolean("enter-complete")
def setEnterComplete(v):
    __settings.set_boolean("enter-complete",v)

"""
double-dot-complete
"""   
def getDoubleDotComplete():
    return __settings.get_boolean("double-dot-complete")
def setDoubleDotComplete(v):
    __settings.set_boolean("double-dot-complete",v)

"""
non-alpha-complete
"""      
def getNonAlphaComplete():
    return __settings.get_boolean("non-alpha-complete")
def setNonAlphaComplete(v):
    __settings.set_boolean("non-alpha-complete",v)

       
"""
GCONF_DOT_AUTO_HIDE_CONSOLE
""" 
def getAutoHideConsole():
    return __settings.get_boolean(GCONF_DOT_AUTO_HIDE_CONSOLE)
    
def setAutoHideConsole(flag):
    __settings.set_boolean(GCONF_DOT_AUTO_HIDE_CONSOLE, flag)
    
"""
GCONF_DOT_AUTO_HIDE_SIDE_PANEL
"""         
def getAutoHideSidePanel():
    return __settings.get_boolean(GCONF_DOT_AUTO_HIDE_SIDE_PANEL)

def setAutoHideSidePanel(flag):
    __settings.set_boolean(GCONF_DOT_AUTO_HIDE_SIDE_PANEL, flag)

"""
GCONF_KEYBINDING_COMPLETE
"""    
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

def setKeybindingComplete(keybinding):
    global __keybindingComplete
    global __keybindingCompleteTuple
    __settings.set_string(GCONF_KEYBINDING_COMPLETE, keybinding)
    __keybindingComplete = keybinding
    __keybindingCompleteTuple = {}
           
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

"""
GCONF_KEYBINDING_BUILD
"""    
def getKeybindingBuild():
    global __keybindingBuild
    if len(__keybindingBuild) == 0:
        keybinding = __settings.get_string(GCONF_KEYBINDING_BUILD)
        __keybindingBuildTuple = {} # Invalidate cache
        if not keybinding:
            __keybindingBuild = DEFAULT_KEYBINDING_BUILD
        else:
            __keybindingBuild = keybinding
    return __keybindingBuild
 
def getKeybindingBuildTuple():
    global __keybindingBuildTuple
    if len(__keybindingBuildTuple) != 0:
        return __keybindingBuildTuple
    alt = False
    ctrl = False
    shift = False
    key = ""
    keybinding = getKeybindingBuild().split('+')
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
    __keybindingBuildTuple = keybindingTuple
    return __keybindingBuildTuple

def setKeybindingBuild(keybinding):
    global __keybindingBuild
    global __keybindingBuildTuple
    __settings.set_string(GCONF_KEYBINDING_BUILD, keybinding)
    __keybindingBuild = keybinding
    __keybindingBuildTuple = {}


"""
GCONF_HXML_PATH
"""
def getHxmlFile():
    global HXML_FILE
    return getHxml()
	
def setHxmlFile(newFile):
    global HXML_FILE
    HXML_FILE = newFile
    setHxml(HXML_FILE)
	
def setHxml(hxmlPath):
    HXML_FILE = hxmlPath
    __settings.set_string(GCONF_HXML_PATH, hxmlPath)

def getHxml():
    return __settings.get_string(GCONF_HXML_PATH)

"""
GCONF_SESSION_PATH_SHOW_HXML
"""
def getSessionPathShowHxml():
    return __settings.get_boolean(GCONF_SESSION_PATH_SHOW_HXML)
    
def setSessionPathShowHxml(value):
    __settings.set_boolean(GCONF_SESSION_PATH_SHOW_HXML, value)

"""
GCONF_BUILD_PATH_SHOW_HXML
"""
def getBuildPathShowHxml():
    return __settings.get_boolean(GCONF_BUILD_PATH_SHOW_HXML)
    
def setBuildPathShowHxml(value):
    __settings.set_boolean(GCONF_BUILD_PATH_SHOW_HXML, value)

"""
GCONF_TOOLBAR_SHOW_HXML
"""
def getToolBarShowHxml():
    return __settings.get_boolean(GCONF_TOOLBAR_SHOW_HXML)
    
def setToolBarShowHxml(value):
    __settings.set_boolean(GCONF_TOOLBAR_SHOW_HXML, value)
    
"""
GCONF_PLAY_AFTER_BUILD
""" 
def getPlayAfterBuild():
    return __settings.get_boolean(GCONF_PLAY_AFTER_BUILD)
    
def setPlayAfterBuild(value):
    __settings.set_boolean(GCONF_PLAY_AFTER_BUILD, value)
    
"""
GCONF_RUN_FILE
""" 
def getRunFile():
    s = __settings.get_string(GCONF_RUN_FILE)
    if s=="None" or s==None:
        s = ""
    return s 
    
def setRunFile(value):
    __settings.set_string(GCONF_RUN_FILE, value)


"""
GCONF_SESSION_PATH_OFFSET
""" 
def getSessionPathOffset():
    return __settings.get_int(GCONF_SESSION_PATH_OFFSET)
    
def decrementSessionPathOffset():
    currentOffset = __settings.get_int(GCONF_SESSION_PATH_OFFSET)
    if currentOffset == 0:
        pass
    else:
        __settings.set_int(GCONF_SESSION_PATH_OFFSET, currentOffset-1)
        
def incrementSessionPathOffset():
    currentOffset = __settings.get_int(GCONF_SESSION_PATH_OFFSET)
    __settings.set_int(GCONF_SESSION_PATH_OFFSET, currentOffset+1)

"""
GCONF_SESSIONS
"""  
def getSessions():
    sessionsTxt = __settings.get_string(GCONF_SESSIONS)
    if sessionsTxt == "" or sessionsTxt == None or sessionsTxt == "None":
        return {}
    sessionsList = sessionsTxt.split("[session]")
    new_sessionsList = []
    for i in sessionsList:
        if i !="":
            new_sessionsList.append(i)
    sessionsHash = {}
    for i in new_sessionsList:
        fileList = i.split('\n')
        new_fileList = []
        for j in fileList:
            if j != "":
                new_fileList.append(j)
        if len(new_fileList) != 0:
            sessionsHash[new_fileList[0]] = new_fileList
    return sessionsHash
    
def saveSessions(sessionsHash):
    content = ""
    for hxmlPath in sessionsHash:
        content += "[session]\n"
        fileList = sessionsHash[hxmlPath]
        for fileName in fileList:
            if fileName != None:
                content += fileName + "\n"
    __settings.set_string(GCONF_SESSIONS, content)
    
"""
GCONF_DEBUG_FILES
"""  
def getDebugFiles():
    txt = __settings.get_string(GCONF_DEBUG_FILES)
    if txt == "" or txt == None or txt == "None":
        return []
    return txt.split('\n')
    
def saveDebugFiles(debugFiles, file):
    out = [file]
    for f in debugFiles:
        if f[0]!=file:
            out.append(f[0]) 
    __settings.set_string(GCONF_DEBUG_FILES,'\n'.join(out))
    
"""
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
"""
