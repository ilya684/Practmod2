from PySide6.QtCore import QObject, Signal


class AppState(QObject):
    note_changed = Signal(int)
    notes_changed = Signal()
    settings_changed = Signal()

    def __init__(self, settings):
        super().__init__()

        self.settings = settings
        self.selected_note_id = None
        self.current_filter = "all"
        self.is_new_note = True
        self.pinned_first = True
        self.preview_length = settings.preview_length

    def select_note(self, note_id):
        self.selected_note_id = note_id
        self.is_new_note = False
        self.note_changed.emit(note_id)

    def start_new_note(self):
        self.selected_note_id = None
        self.is_new_note = True

    def set_filter(self, filter_name):
        self.current_filter = filter_name
        self.notes_changed.emit()

    def set_preferences(self, pinned_first, preview_length):
        self.pinned_first = pinned_first
        self.preview_length = preview_length
        self.settings.set_preview_length(preview_length)
        self.settings_changed.emit()

    def notify_note_changed(self, note_id):
        self.note_changed.emit(note_id)
        self.notes_changed.emit()
