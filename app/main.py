from PySide6.QtWidgets import QApplication
from app.presentation.home_window import HomeWindow

def main():
    app = QApplication()
    window = HomeWindow()
    window.setWindowTitle("Logs reader")
    window.show()
    app.exec()
    
    
if __name__ == "__main__":
    main()