import logging
import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from app.config import APP_TITLE, DB_FILE
from app.error_handler import install_exception_handler
from app.logging_setup import setup_logging
from app.settings import AppSettings
from app.state import AppState
from app.storage import SqliteStorage, StorageError
from app.ui.window_manager import WindowManager


def main():
    app = QApplication(sys.argv)

    settings = AppSettings()
    setup_logging(settings.log_level)
    install_exception_handler()

    logger = logging.getLogger(__name__)

    try:
        storage = SqliteStorage(DB_FILE)
    except StorageError as error:
        logger.error("Application startup failed: %s", error)
        QMessageBox.critical(
            None,
            APP_TITLE,
            str(error),
        )
        return 1

    app_state = AppState(settings)

    window_manager = WindowManager(
        app_state,
        storage,
    )

    app.aboutToQuit.connect(storage.close)

    window_manager.open_main_window()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
