import os
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class HomeWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = self.load_ui()
        self.setCentralWidget(self.ui)
        self.setFixedSize(self.ui.size())

    def load_ui(self):
        loader = QUiLoader()
        file = QFile(os.path.join(os.path.dirname(__file__), "home.ui"))
        file.open(QFile.ReadOnly)
        widget = loader.load(file)
        file.close()
        return widget