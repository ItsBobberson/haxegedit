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
        
        #self.builder.add_from_file(os.path.join(self.dataDir, "ui", "BottomPanel.glade"))
        #self.ui = Gtk.Builder()
        #self.ui.add_from_file(os.path.join(self.dataDir, "ui", "BottomPanel.ui"))
        #print self["scrolledWindow"]
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.dataDir + "/" + "ui" + "/" + "DebuggerBox.glade")
        self.builder.connect_signals(self)
        
        self.box = self.builder.get_object("box")
        
        self.textView = self.builder.get_object("textView")
        self.textView.set_editable (False)
        self.textView.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(red=65535, green=65535, blue=65535))
        self.textView.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(red=11776, green=13312, blue=13824))
        self.textView.modify_bg(Gtk.StateType.SELECTED, Gdk.Color(red=51776, green=0, blue=0))
        #self.textView.connect("button-press-event", self.onTextViewClick)

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
        
    def onStartDebugButtonClick(self, button):
        swf = self.builder.get_object("urlInput").get_text()
        hxml = self.plugin.sf(Configuration.getHxml())
        path = os.path.dirname(hxml) + "/" + swf
        if not os.path.isfile(path):
            self.appendText("Could not find " + path)
        else:
            self.plugin.debug(swf)
            self.builder.get_object("urlBox").hide()
            self.builder.get_object("buttonBox").show()
            
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
        
    #def onBreakDelAllButtonClick(self, button)
        
        """
        doc = self.geditWindow.get_active_document()
        if not doc.get_uri_for_display().endswith ('hx'):
            self.appendText("Can only set breakpoints in .hx file.\n")
            return
        insert = doc.get_iter_at_mark(doc.get_insert())
        lineOffset = insert.get_line()+1
        filePath = doc.get_uri_for_display()
        dirName = os.path.dirname(filePath)
        fileName = os.path.basename(filePath)
        self.plugin.sendDebugCommand("break "+fileName+":"+str(lineOffset))
        """
    
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
        
    
    """    
    def onTextViewClick(self, textView, event):
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            errorInfo = self.parseErrorLine()
            if errorInfo == None:
                return True
            characterRange = errorInfo['characterRange']
            if characterRange.find('-') == -1:
                characterRange = characterRange + "-" + characterRange
            charRange = characterRange.split("-")
            charRangeStart = int(charRange[0])
            charRangeEnd = int(charRange[1])
            lineNr = int(errorInfo['lineNumber'])
            offset = charRangeEnd
            if errorInfo['error'].startswith('Unexpected'):
                offset = charRangeStart

            if errorInfo['fileLocation'][0] == "/" :
                path = "/" + errorInfo['fileLocation']
            else:
                hxml = self.plugin.sf(Configuration.getHxml())
                path = os.path.dirname(hxml) + "/" + errorInfo['fileLocation']
                
            gio_file = Gio.file_new_for_path(path)
            tab = self.geditWindow.get_tab_from_location(gio_file)
            if tab == None:
                tab = self.geditWindow.create_tab_from_location(gio_file, None, lineNr, offset+1, False, True )
            else:
                self.geditWindow.set_active_tab(tab)
                view = self.geditWindow.get_active_view()
                buf = view.get_buffer() 
                i = buf.get_iter_at_line_offset(lineNr - 1, offset)
                buf.place_cursor(i)
                view.scroll_to_cursor()

            if errorInfo['error'].find(' should be ') != -1 or errorInfo['error'].startswith('Unknown identifier') or errorInfo['error'].startswith('Class not found'):
                view = self.geditWindow.get_active_view()
                buf = view.get_buffer()
                
                insertMark = buf.get_insert()
                selectionBoundMark = buf.get_selection_bound()
                startIter = buf.get_iter_at_mark(insertMark)
                startIter.backward_chars(charRangeEnd - charRangeStart)
                buf.move_mark(selectionBoundMark, startIter)
                
            if errorInfo['error'].startswith('Unexpected'):
                view = self.geditWindow.get_active_view()
                buf = view.get_buffer()
                
                insertMark = buf.get_insert()
                selectionBoundMark = buf.get_selection_bound()
                startIter = buf.get_iter_at_mark(insertMark)
                startIter.forward_chars(charRangeEnd - charRangeStart)
                buf.move_mark(selectionBoundMark, startIter)
                
            if errorInfo['error'].startswith("Invalid character"):
                view = self.geditWindow.get_active_view()
                buf = view.get_buffer()
                
                insertMark = buf.get_insert()
                selectionBoundMark = buf.get_selection_bound()
                startIter = buf.get_iter_at_mark(insertMark)
                startIter.forward_chars(1)
                buf.move_mark(selectionBoundMark, startIter)

            return True
                        
        if event.type == Gdk.EventType._3BUTTON_PRESS:
            errorInfo = self.parseErrorLine()
            if errorInfo != None and errorInfo['errorLine'].endswith("Missing ;"):
                self.geditWindow.get_active_document().insert_at_cursor (";")
            return True
        
    def parseErrorLine(self):
        doc = self.textView.get_buffer()
        iter = doc.get_iter_at_mark(doc.get_insert())
        lineStart = iter.copy()
        lineEnd = iter.copy()
        lineStart.set_offset (iter.get_offset () - iter.get_line_offset ())
        
        #get the complete line
        lineEnd.forward_to_line_end()
        currentLine = unicode (doc.get_text (lineStart, lineEnd, include_hidden_chars=True))
        if len(currentLine)==0:
            return None
        #print currentLine;
        
        #get the file location
        locationEnd = lineStart.copy()
        while locationEnd.forward_char():
            char = unicode(locationEnd.get_char())
            if char == ":":
                fileLocation = unicode (doc.get_text (lineStart, locationEnd, include_hidden_chars=True))
                lineNumberEnd = locationEnd.copy()
                #print fileLocation
                break
        try:
            lineNumberEnd
        except NameError:
            return None
            
        #get the line number
        locationEnd.forward_char()#skip colon
        while lineNumberEnd.forward_char():
            char = unicode(lineNumberEnd.get_char())
            if char == ":":
                lineNumber = unicode (doc.get_text (locationEnd, lineNumberEnd, include_hidden_chars=True))
                #print lineNumber
                break
        
        #get character range
        lineNumberEnd.forward_char()#skip colon
        lineNumberEnd.forward_char()#skip space
        lineNumberEnd.forward_word_end()#skip 'characters'
        lineNumberEnd.forward_char()#skip space
        characterRangeEnd = lineNumberEnd.copy()
        while characterRangeEnd.forward_char():
            char = unicode(characterRangeEnd.get_char())
            if char == " ":
                characterRange = unicode (doc.get_text (lineNumberEnd, characterRangeEnd, include_hidden_chars=True))
                #print characterRange
                break
        
        #get error
        characterRangeEnd.forward_char()#skip space
        characterRangeEnd.forward_char()#skip colon
        characterRangeEnd.forward_char()#skip space
        errorEnd = characterRangeEnd.copy()
        errorEnd.forward_sentence_end()
        error = unicode (doc.get_text (characterRangeEnd, errorEnd, include_hidden_chars=True))
        
        return {'errorLine':currentLine, 'fileLocation':fileLocation, 'lineNumber':lineNumber, 'characterRange':characterRange, 'error':error}
    """        
    
       
