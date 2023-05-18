import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import QsciLexerCustom, QsciScintilla

class HTMLCustomLexer(QsciLexerCustom):

    def __init__(self, parent):
        super(HTMLCustomLexer, self).__init__(parent)

        self.color1 = "#abb2bf"
        self.color2 = "#282c34"

        # Ajustes predeterminados
        self.setDefaultColor(QColor(self.color1))
        self.setDefaultPaper(QColor(self.color2))
        self.setDefaultFont(QFont("Consolas", 14))

        # Keywords
        self.KEYWORD_LIST = [
            "html", "head", "title", "body", "h1", "h2", "h3", "h4", "h5", "h6",
            "p", "div", "span", "a", "img", "ul", "ol", "li", "table", "tr", "td",
            "th", "form", "input", "button", "select", "option", "script", "style"
        ]

        # Color por estilo
        self.DEFAULT = 0
        self.KEYWORD = 1
        self.STRING = 2
        self.BRACKETS = 3
        self.COMMENTS = 4

        # Estilos
        self.setColor(QColor(self.color1), self.DEFAULT)
        self.setColor(QColor("#c678dd"), self.KEYWORD)
        self.setColor(QColor("#98C379"), self.STRING)
        self.setColor(QColor("#c678dd"), self.BRACKETS)
        self.setColor(QColor("#777777"), self.COMMENTS)

        # Papel de color
        self.setPaper(QColor(self.color2), self.DEFAULT)
        self.setPaper(QColor(self.color2), self.KEYWORD)
        self.setPaper(QColor(self.color2), self.STRING)
        self.setPaper(QColor(self.color2), self.BRACKETS)
        self.setPaper(QColor(self.color2), self.COMMENTS)

        # Fuente
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.DEFAULT)
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.KEYWORD)

    def language(self) -> str:
        return "HTMLCustomLexer"

    def description(self, style: int) -> str:
        if style == self.DEFAULT:
            return "DEFAULT"
        elif style == self.KEYWORD:
            return "KEYWORD"
        elif style == self.STRING:
            return "STRING"
        elif style == self.BRACKETS:
            return "BRACKETS"
        elif style == self.COMMENTS:
            return "COMMENTS"
        else:
            return ""

    def get_tokens(self, text) -> list[str, int]:
        p = re.compile(r"[]\/|\/[]|\s+|\w+|\W")
        return [(token, len(bytearray(token, "utf-8"))) for token in p.findall(text)]

    def styleText(self, start: int, end: int) -> None:
        self.startStyling(start)
        editor: QsciScintilla = self.parent()

        text = editor.text()[start:end]
        token_list = self.get_tokens(text)

        string_flag = False

        if start > 0:
            previous_style_nr = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if previous_style_nr == self.STRING:
                string_flag = False

        def next_tok(skip: int = None):
            if len(token_list) > 0:
                if skip is not None and skip != 0:
                    for _ in range(skip - 1):
                        if len(token_list) > 0:
                            token_list.pop(0)
                return token_list.pop(0)
            else:
                return None

        def peek_tok(n=0):
            try:
                return token_list[n]
            except IndexError:
                return ['']

        def skip_spaces_peek(skip=None):
            i = 0
            tok = " "
            if skip is not None:
                i = skip
            while tok[0].isspace():
                tok = peek_tok(i)
                i += 1
            return tok, i

        while True:
            curr_token = next_tok()

            if curr_token is None:
                break

            tok: str = curr_token[0]
            tok_len: int = curr_token[1]

            if string_flag:
                self.setStyling(tok_len, self.STRING)
                if tok == '"' or tok == "'":
                    string_flag = False
                continue

            if tok in self.KEYWORD_LIST:
                self.setStyling(tok_len, self.KEYWORD)
            elif tok in ["<", ">", "/", "="]:
                self.setStyling(tok_len, self.BRACKETS)
            elif tok == '"' or tok == "'":
                self.setStyling(tok_len, self.STRING)
                string_flag = True
            elif tok == "<!--":
                self.setStyling(tok_len, self.COMMENTS)
                while True:
                    curr_token = next_tok()
                    if curr_token is None:
                        break
                    tok: str = curr_token[0]
                    tok_len: int = curr_token[1]
                    self.setStyling(tok_len, self.COMMENTS)
                    if tok == "-->":
                        break
            else:
                self.setStyling(tok_len, self.DEFAULT)
