import sys

from PySide6.QtWidgets import QApplication

from app.config import DB_FILE
from app.storage import SqliteStorage
from app.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    storage = SqliteStorage(DB_FILE)
    window = MainWindow(storage)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
