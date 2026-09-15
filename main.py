import sys

from PySide6.QtWidgets import QApplication

from app.config import DB_FILE
from app.state import AppState
from app.storage import SqliteStorage
from app.ui.window_manager import WindowManager


def main():
    app = QApplication(sys.argv)

    storage = SqliteStorage(DB_FILE)
    app_state = AppState()
    window_manager = WindowManager(
        app_state,
        storage,
    )

    app.aboutToQuit.connect(
        storage.close
    )

    window_manager.open_main_window()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
