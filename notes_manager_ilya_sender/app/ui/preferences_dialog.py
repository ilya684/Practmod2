from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
)

from app.config import DEFAULT_PREVIEW_LENGTH


class PreferencesDialog(QDialog):
    def __init__(self, app_state):
        super().__init__()

        self.app_state = app_state

        self.setWindowTitle("Preferences")
        self.setModal(True)

        self.pinned_first_box = QCheckBox(
            "Show pinned notes first"
        )

        self.preview_spin = QSpinBox()
        self.preview_spin.setMinimum(1)
        self.preview_spin.setMaximum(200)
        self.preview_spin.setValue(
            self.app_state.preview_length
            or DEFAULT_PREVIEW_LENGTH
        )

        self.pinned_first_box.setChecked(
            self.app_state.pinned_first
        )

        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("Applies to every open window.")
        )

        layout.addWidget(
            self.pinned_first_box
        )

        preview_layout = QHBoxLayout()

        preview_layout.addWidget(
            QLabel("Preview length:")
        )

        preview_layout.addWidget(
            self.preview_spin
        )

        layout.addLayout(preview_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def accept(self):
        self.app_state.set_preferences(
            self.pinned_first_box.isChecked(),
            self.preview_spin.value(),
        )

        super().accept()
