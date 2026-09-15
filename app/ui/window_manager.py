from PySide6.QtWidgets import QApplication

from app.config import CASCADE_STEP


class WindowManager:
    def __init__(self, app_state, storage):
        self.app_state = app_state
        self.storage = storage

        self.main_windows = []
        self.note_windows = {}
        self.window_counter = 0

    def open_main_window(self):
        from app.ui.main_window import MainWindow

        self.window_counter += 1

        window = MainWindow(
            self.storage,
            self.app_state,
            self,
            self.window_counter,
        )

        self.main_windows.append(window)

        offset = (
            self.window_counter - 1
        ) * CASCADE_STEP

        window.move(offset, offset)

        window.destroyed.connect(
            lambda _=None, w=window:
            self.remove_main_window(w)
        )

        window.show()

        return window

    def remove_main_window(self, window):
        if window in self.main_windows:
            self.main_windows.remove(window)

    def open_note_window(self, note_id):
        if note_id in self.note_windows:
            window = self.note_windows[note_id]

            window.show()
            window.raise_()
            window.activateWindow()

            return window

        from app.ui.note_window import NoteWindow

        window = NoteWindow(
            self.storage,
            self.app_state,
            self,
            note_id,
        )

        self.note_windows[note_id] = window

        window.destroyed.connect(
            lambda _=None, note_id=note_id:
            self.remove_note_window(note_id)
        )

        window.show()
        window.raise_()
        window.activateWindow()

        return window

    def remove_note_window(self, note_id):
        self.note_windows.pop(
            note_id,
            None,
        )

    def close_all_windows(self):
        for window in list(
            self.note_windows.values()
        ):
            window.close()

        for window in list(
            self.main_windows
        ):
            window.close()

        QApplication.closeAllWindows()
