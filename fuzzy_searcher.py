from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem

import os
from pathlib import Path
import re


class SearchItem(QListWidgetItem):
    def __init__(self, name, full_path, lineno, end, line):
        self.name = name
        self.full_path = full_path
        self.lineno = lineno
        self.end = end
        self.line = line
        self.formatted = f'{self.name}:{self.lineno}:{self.end} - {self.line} ...'
        super().__init__(self.formatted)

    def __str__(self):
        return self.formatted

    def __repr__(self):
        return self.formatted


class SearchWorker(QThread):
    finished = pyqtSignal(list)

    def __init__(self):
        super(SearchWorker, self).__init__(None)
        self.items = []
        self.search_file: str = None
        self.search_text: str = None

    def search(self):
        debug = False
        self.items = []

        exclude_files = set([".svg", ".png", ".exe", ".pyc", ".qm"])

        if not os.path.isfile(self.search_file):
            return

        file_ = os.path.basename(self.search_file)
        full_path = os.path.abspath(self.search_file)

        if Path(file_).suffix in exclude_files:
            return

        try:
            with open(full_path, 'r', encoding='utf8') as f:
                try:
                    reg = re.compile(self.search_text, re.IGNORECASE)
                    for i, line in enumerate(f):
                        if m := reg.search(line):
                            fd = SearchItem(
                                file_,
                                full_path,
                                i,
                                m.end(),
                                line[m.start():].strip()[:50],  # limiting to 50 chars
                            )
                            self.items.append(fd)
                except re.error as e:
                    if debug:
                        print(e)
        except UnicodeDecodeError as e:
            if debug:
                print(e)
                return

        self.finished.emit(self.items)

    def run(self):
        self.search()

    def update(self, pattern, file_path, full_path):
        self.search_text = pattern
        self.search_file = file_path
        self.full_path= full_path
        print(self.search_text)
        print(self.search_file)
        print(f"full path {full_path}")
        self.start()
