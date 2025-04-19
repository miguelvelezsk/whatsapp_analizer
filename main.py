from ui.app_ui import MyApp
from PySide6.QtWidgets import QApplication
import sys
from styles.styles import style_sheet

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = MyApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()