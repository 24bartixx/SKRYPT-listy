from PySide6.QtWidgets import QApplication
from app.home.presentation.home_widget import HomeWidget

def main():
    app = QApplication()
    window = HomeWidget()
    window.show()
    app.exec()
    
    
if __name__ == "__main__":
    main()