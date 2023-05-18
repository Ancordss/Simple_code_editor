from msilib.schema import SelfReg
from multiprocessing import parent_process
from random import paretovariate

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *



import keyword
import pkgutil
from lexer import HTMLCustomLexer

class Editor(QsciScintilla):
    
    def __init__(self,parent=None):
            super (Editor, self).__init__(parent)

        #Encoding
            self.setUtf8(True)
        #Font
            self.window_font = QFont("Fire Code")
            self.window_font.setPointSize(12)
            self.setFont(self.window_font)
        #brace matching
            self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        
        #indentation
            self.setIndentationGuides(True)
            self.setTabWidth(4)
            self.setIndentationsUseTabs(False)
            self.setAutoIndent(True)
        
        # autocomplete
            self.setAutoCompletionSource(QsciScintilla.AcsAll)
            self.setAutoCompletionThreshold(1)
            self.setAutoCompletionCaseSensitivity(False)
            self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)
        
        #caret
            self.setCaretForegroundColor(QColor("#dedcdc"))
            self.setCaretLineVisible(True)
            self.setCaretWidth(2)
            self.setCaretLineBackgroundColor(QColor("#2c313c"))
        
        # EOL
            self.setEolMode(QsciScintilla.EolWindows)
            self.setEolVisibility(False)
        
        # lexet for syntax highlightning

            self.pylexer = HTMLCustomLexer(self) # Lexer Languajes¿
            self.pylexer.setDefaultFont(self.window_font)

        
        #Api
            self.api = QsciAPIs(self.pylexer)
            for key in keyword.kwlist+dir(__builtins__):
                self.api.add(key)

            for _, name, _ in pkgutil.iter_modules():
                self.api.add(name)    

        # for test purpose
        # you can add custom function with its parameters   
            self.api.add("addition(a: int, b: int)")
            self.api.prepare()
            self.setLexer(self.pylexer)

        #Line numbers
            self.setMarginType(0, QsciScintilla.NumberMargin)
            self.setMarginWidth(0,"000")
            self.setMarginsForegroundColor(QColor("#ff888888"))
            self.setMarginsBackgroundColor(QColor("#282c34"))
            self.setMarginsFont(self.window_font)

        #key press
            #self.keyPressEvent = self.handle_editor_press
    def keyPressEvent(self,e: QKeyEvent) -> None:
            if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Space:
                self.autoCompleteFromAll()
            else:
                return super().keyPressEvent(e)