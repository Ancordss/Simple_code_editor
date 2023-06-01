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
from typing import TYPE_CHECKING


class Editor(QsciScintilla):
    def __init__(self, main_window, parent=None):
        super(Editor, self).__init__(parent)
        self.main_window = main_window
        self._current_file_changed = False
        
        # Encoding
        self.setUtf8(True)
        
        # Font
        self.window_font = QFont("Fire Code")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)
        
        # Brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Indentation
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)

        # Autocomplete
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

        # Caret
        self.setCaretForegroundColor(QColor("#0A4435"))  # Green color
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)
        self.setCaretLineBackgroundColor(QColor("#0A4435"))  # Dark green color

        # EOL
        self.setEolMode(QsciScintilla.EolWindows)
        self.setEolVisibility(False)

        # Lexer for syntax highlighting
        self.pylexer = HTMLCustomLexer(self)
        self.pylexer.setDefaultFont(self.window_font)

        # API
        self.api = QsciAPIs(self.pylexer)
        for key in keyword.kwlist+dir(__builtins__):
            self.api.add(key)

        for _, name, _ in pkgutil.iter_modules():
            self.api.add(name)    

        # For test purpose, you can add custom function with its parameters
        self.api.add("addition(a: int, b: int)")
        self.api.prepare()
        self.setLexer(self.pylexer)

        # Line numbers
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "000")
        self.setMarginsForegroundColor(QColor("#c2d3b2"))  # Light green color
        self.setMarginsBackgroundColor(QColor("#173725"))  # Dark green color
        self.setMarginsFont(self.window_font)

    @property
    def current_file_changed(self, value: bool):
        curr_index = self.main_window
    
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Space:
            self.autoCompleteFromAll()
        else:
            return super().keyPressEvent(e)
