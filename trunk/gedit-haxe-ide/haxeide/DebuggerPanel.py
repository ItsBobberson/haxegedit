import Configuration
import os
from gi.repository import GObject, Gtk, Gdk, Gedit, Gio, GLib
import string

class DebuggerPanel(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "DebuggerPanel"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self, plugin):
        GObject.Object.__init__(self)
        self.plugin = plugin
        self.dataDir = plugin.plugin_info.get_data_dir()
        self.geditWindow = plugin.window
        self.debugType = "fdb"
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "DebuggerBox.glade")
        self.builder.connect_signals(self)
        
        self.box = self.builder.get_object("box")
        
        self.textView = self.builder.get_object("textView")
        self.textView.set_editable (False)
        self.textView.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(red=65535, green=65535, blue=65535))
        self.textView.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(red=11776, green=13312, blue=13824))
        self.textView.modify_bg(Gtk.StateType.SELECTED, Gdk.Color(red=51776, green=0, blue=0))

        self.geditBottomPanel = self.geditWindow.get_bottom_panel()
        self.geditBottomPanel.add_item(self.box, "haxe_debugger_panel", "debugger", Gtk.Image.new_from_file(self.dataDir + "/" + "icons" + "/" + "haxe_logo_16.png"))# Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU))
        self.geditBottomPanel.activate_item(self.box)
        
        self.builder.get_object("buttonBox").hide()
        
        self.toolbar = self.builder.get_object("toolbar")

        self.breakButton = Gtk.ToolButton(stock_id=Gtk.STOCK_ADD)
        self.breakButton.connect("clicked", self.onBreakButtonClick)
        self.breakButton.set_tooltip_text('Set breakpoint on selected line')
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.breakButton)
        
        self.clearButton = Gtk.ToolButton(stock_id=Gtk.STOCK_DELETE)
        self.clearButton.connect("clicked", self.onClearButtonClick)
        self.clearButton.set_tooltip_text('Clear breakpoint from selected line')
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.clearButton)
        
        self.killButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_STOP)
        self.killButton.connect("clicked", self.onKillButtonClick)
        self.killButton.set_tooltip_text('Kill execution of program being debugged')
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.killButton)
        
        self.continueButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_PLAY)
        self.continueButton.connect("clicked", self.onContinueButtonClick)
        self.continueButton.set_tooltip_text('Continue execution after stopping at breakpoint')
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.continueButton)
        
        self.stepButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_NEXT)
        self.stepButton.connect("clicked", self.onStepButtonClick)
        self.stepButton.set_tooltip_text('Step program until it reaches a different source line')
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.stepButton)
        
        self.finishButton = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_FORWARD)
        self.finishButton.connect("clicked", self.onFinishButtonClick)
        self.finishButton.set_tooltip_text('Execute until current function returns')
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.finishButton)
        
        self.quitButton = Gtk.ToolButton(stock_id=Gtk.STOCK_QUIT)
        self.quitButton.connect("clicked", self.onQuitButtonClick)
        self.quitButton.set_tooltip_text('Exit fdb')
        self.toolbar.insert(pos = len(self.toolbar.get_children()), item = self.quitButton)

        self.toolbar.show_all()
        
    def activate(self):
        self.geditBottomPanel.activate_item(self.box)
            
    def remove(self):
        self.geditBottomPanel.remove_item(self.box)
        
    def onConsoleButtonClick(self, button):
        txt = self.builder.get_object("consoleInput").get_text()
        self.builder.get_object("consoleInput").set_text("")
        self.plugin.sendDebugCommand(txt)

    def setText(self, txt):
        textBuffer = self.textView.get_buffer()
        textBuffer.set_text(txt)
        
    def appendText(self, txt):
        textBuffer = self.textView.get_buffer()
        textBuffer.insert(textBuffer.get_end_iter(), txt)
        self.textView.scroll_mark_onscreen(textBuffer.get_insert())
        #self.textView.scroll_to_mark(textBuffer.get_insert(), 0)
        
    def onBinFileInputChange(self, entry):
        if entry.get_text().endswith(".swf"):
            self.debugType = "fdb"
            self.builder.get_object("urlLabel").set_text("swf:")
            self.builder.get_object("consoleLabel").set_text(self.debugType + ":")
        else:
            self.debugType = "gdb"
            self.builder.get_object("urlLabel").set_text("cpp:")
            self.builder.get_object("consoleLabel").set_text(self.debugType + ":")
            
    def onStartDebugButtonClick(self, button):
        file = self.builder.get_object("urlInput").get_text()
        hxml = self.plugin.sf(Configuration.getHxml())
        path = os.path.dirname(hxml) + "/" + file
        if not os.path.isfile(path):
            self.appendText("Could not find " + path)
        else:
            self.builder.get_object("urlBox").hide()
            self.builder.get_object("buttonBox").show()

            if self.debugType=="fdb":
                GObject.idle_add(self.plugin.debugAVM2, file)
            else:
                GObject.idle_add(self.plugin.debugCPP, file)
            
    def onQuitButtonClick(self, button):
        self.plugin.sendDebugCommand("quit")
        self.builder.get_object("urlBox").show()
        self.builder.get_object("buttonBox").hide()
            
    def onBreakButtonClick(self, button):
        fileLine = self.getFileLine()
        if fileLine != None:
            self.plugin.sendDebugCommand("break "+fileLine)        
            
    def onClearButtonClick(self, button):
        fileLine = self.getFileLine()
        if fileLine != None:
            self.plugin.sendDebugCommand("clear "+fileLine)
            
    def onKillButtonClick(self, button):    
        self.plugin.sendDebugCommand("kill")
    
    def onNextButtonClick(self, button):
        self.plugin.sendDebugCommand("next")
        
    def onContinueButtonClick(self, button):
        self.plugin.sendDebugCommand("continue")
        
    def onFinishButtonClick(self, button):
        self.plugin.sendDebugCommand("finish")
    def onStepButtonClick(self, button):
        self.plugin.sendDebugCommand("step")
        
    def getFileLine(self):
        doc = self.geditWindow.get_active_document()
        if not doc.get_uri_for_display().endswith ('hx'):
            self.appendText("Can only set breakpoints in .hx file.\n")
            return None
        insert = doc.get_iter_at_mark(doc.get_insert())
        lineOffset = insert.get_line()+1
        filePath = doc.get_uri_for_display()
        dirName = os.path.dirname(filePath)
        fileName = os.path.basename(filePath)
        return fileName+":"+str(lineOffset)
