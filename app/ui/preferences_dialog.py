from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QSpinBox,
    QVBoxLayout,
)


class PreferencesDialog(QDialog):
    def __init__(self, app_state):
        super().__init__()

        self.app_state = app_state
        self.settings = app_state.settings

        self.setWindowTitle("Preferences")
        self.setModal(True)

        self.pinned_first_box = QCheckBox(
            "Show pinned notes first"
        )
        self.pinned_first_box.setChecked(
            self.app_state.pinned_first
        )

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(
            self.settings.MIN_FONT_SIZE,
            self.settings.MAX_FONT_SIZE,
        )
        self.font_size_spin.setValue(
            self.settings.font_size
        )

        self.preview_spin = QSpinBox()
        self.preview_spin.setRange(
            self.settings.MIN_PREVIEW_LENGTH,
            self.settings.MAX_PREVIEW_LENGTH,
        )
        self.preview_spin.setValue(
            self.settings.preview_length
        )

        self.autosave_box = QCheckBox(
            "Enable autosave"
        )
        self.autosave_box.setChecked(
            self.settings.autosave
        )

        self.autosave_interval_spin = QSpinBox()
        self.autosave_interval_spin.setRange(
            self.settings.MIN_AUTOSAVE_INTERVAL,
            self.settings.MAX_AUTOSAVE_INTERVAL,
        )
        self.autosave_interval_spin.setValue(
            self.settings.autosave_interval_s
        )

        self.confirm_delete_box = QCheckBox(
            "Confirm note deletion"
        )
        self.confirm_delete_box.setChecked(
            self.settings.confirm_delete
        )

        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(
            ["INFO", "DEBUG"]
        )
        self.log_level_combo.setCurrentText(
            self.settings.log_level
        )

        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        form.addRow(
            "Show pinned notes first:",
            self.pinned_first_box,
        )
        form.addRow(
            "Editor font size:",
            self.font_size_spin,
        )
        form.addRow(
            "Preview length:",
            self.preview_spin,
        )
        form.addRow(
            "Autosave:",
            self.autosave_box,
        )
        form.addRow(
            "Autosave interval (s):",
            self.autosave_interval_spin,
        )
        form.addRow(
            "Confirm delete:",
            self.confirm_delete_box,
        )
        form.addRow(
            "Log level:",
            self.log_level_combo,
        )

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def accept(self):
        self.app_state.pinned_first = (
            self.pinned_first_box.isChecked()
        )

        self.settings.set_font_size(
            self.font_size_spin.value()
        )
        self.settings.set_preview_length(
            self.preview_spin.value()
        )
        self.settings.set_autosave(
            self.autosave_box.isChecked()
        )
        self.settings.set_autosave_interval_s(
            self.autosave_interval_spin.value()
        )
        self.settings.set_confirm_delete(
            self.confirm_delete_box.isChecked()
        )
        self.settings.set_log_level(
            self.log_level_combo.currentText()
        )
        self.settings.sync()

        self.app_state.preview_length = (
            self.settings.preview_length
        )
        self.app_state.settings_changed.emit()

        super().accept()
