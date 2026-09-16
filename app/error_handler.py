import logging
import sys
import traceback

from PySide6.QtWidgets import QMessageBox


def install_exception_handler():
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(
                exc_type,
                exc_value,
                exc_traceback,
            )
            return

        logger = logging.getLogger("app")

        try:
            logger.critical(
                "Unhandled exception",
                exc_info=(
                    exc_type,
                    exc_value,
                    exc_traceback,
                ),
            )
        except Exception as log_error:
            sys.stderr.write(
                "Failed to write exception to log: "
                f"{log_error}\n"
            )

        try:
            details = "".join(
                traceback.format_exception(
                    exc_type,
                    exc_value,
                    exc_traceback,
                )
            )

            QMessageBox.critical(
                None,
                "Application error",
                "An unexpected error occurred.\n\n"
                + details,
            )
        except Exception as message_error:
            sys.stderr.write(
                "Failed to show error message: "
                f"{message_error}\n"
            )
            sys.__excepthook__(
                exc_type,
                exc_value,
                exc_traceback,
            )

    sys.excepthook = handle_exception
