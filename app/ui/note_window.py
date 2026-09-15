from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_TITLE


class NoteWindow(QWidget):
    def __init__(
        self,
        storage,
        app_state,
        window_manager,
        note_id,
    ):
        super().__init__(None)

        self.storage = storage
        self.app_state = app_state
        self.window_manager = window_manager
        self.note_id = note_id

        self.is_modified = False

        self.text_edit = QTextEdit()
        self.pinned_box = QCheckBox("Pinned")
        self.updated_label = QLabel()
        self.close_button = QPushButton("Close")

        self.create_ui()
        self.load_note()

        self.text_edit.textChanged.connect(
            self.on_text_changed
        )

        self.pinned_box.toggled.connect(
            self.on_pinned_changed
        )

        self.close_button.clicked.connect(
            self.close
        )

        self.app_state.note_changed.connect(
            self.on_note_changed
        )

    def create_ui(self):
        self.setAttribute(
            Qt.WidgetAttribute.WA_DeleteOnClose
        )

        self.resize(600, 450)

        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        top_layout.addWidget(
            QLabel(f"Note {self.note_id}")
        )

        top_layout.addStretch()
        top_layout.addWidget(
            self.pinned_box
        )

        layout.addLayout(top_layout)
        layout.addWidget(self.text_edit)

        bottom_layout = QHBoxLayout()

        bottom_layout.addWidget(
            self.updated_label
        )

        bottom_layout.addStretch()

        bottom_layout.addWidget(
            self.close_button
        )

        layout.addLayout(bottom_layout)

    def load_note(self):
        note = self.storage.get_note(
            self.note_id
        )

        if note is None:
            self.close()
            return

        self.text_edit.blockSignals(True)
        self.pinned_box.blockSignals(True)

        self.text_edit.setPlainText(
            note.text
        )

        self.pinned_box.setChecked(
            note.pinned
        )

        self.updated_label.setText(
            f"Updated: {note.created_at}"
        )

        self.text_edit.document().setModified(
            False
        )

        self.is_modified = False

        self.text_edit.blockSignals(False)
        self.pinned_box.blockSignals(False)

        self.update_title()

    def on_text_changed(self):
        text = self.text_edit.toPlainText()

        self.is_modified = True

        try:
            self.storage.update_note(
                self.note_id,
                text,
            )
        except Exception:
            return

        self.app_state.notes_changed.emit()
        self.update_title()

    def on_pinned_changed(self, checked):
        note = self.storage.get_note(
            self.note_id
        )

        if note is None:
            return

        if note.pinned != checked:
            self.storage.toggle_pin(
                self.note_id
            )

        self.app_state.notes_changed.emit()

    def on_note_changed(self, note_id):
        if note_id != self.note_id:
            return

        self.load_note()

    def update_title(self):
        title = f"Note {self.note_id}"

        if self.is_modified:
            title += "*"

        self.setWindowTitle(
            f"{title} - {APP_TITLE}"
        )

    def closeEvent(self, event):
        event.accept()
