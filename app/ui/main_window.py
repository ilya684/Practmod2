import csv

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QDockWidget,
    QMainWindow,
    QMessageBox,
    QMenu,
    QToolButton,
)

from app.config import APP_TITLE, STUDENT_GROUP, STUDENT_NAME
from app.ui.note_editor_panel import NoteEditorPanel
from app.ui.note_list_panel import NoteListPanel
from app.ui.preferences_dialog import PreferencesDialog


class MainWindow(QMainWindow):
    def __init__(
        self,
        storage,
        app_state,
        window_manager,
        window_number,
    ):
        super().__init__()

        self.storage = storage
        self.app_state = app_state
        self.window_manager = window_manager
        self.window_number = window_number

        self.setAttribute(
            Qt.WidgetAttribute.WA_DeleteOnClose
        )

        self.resize(1000, 650)

        self.editor = NoteEditorPanel()
        self.setCentralWidget(self.editor)

        self.notes_dock = self.create_notes_dock()

        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            self.notes_dock,
        )

        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()

        self.app_state.notes_changed.connect(
            self.refresh_from_state
        )

        self.app_state.settings_changed.connect(
            self.refresh_from_state
        )

        self.setWindowTitle(
            self.window_title()
        )

        self.load_notes()

    def window_title(self):
        if self.window_number == 1:
            return (
                f"{APP_TITLE} - "
                f"{STUDENT_NAME}, {STUDENT_GROUP}"
            )

        return (
            f"{APP_TITLE} ({self.window_number}) - "
            f"{STUDENT_NAME}, {STUDENT_GROUP}"
        )

    def create_notes_dock(self):
        dock = QDockWidget("Notes", self)

        dock.setObjectName(
            f"NotesDock{self.window_number}"
        )

        self.note_list = NoteListPanel()

        self.note_list.itemSelectionChanged.connect(
            self.on_note_selected
        )

        self.note_list.itemDoubleClicked.connect(
            self.open_selected_note
        )

        dock.setWidget(self.note_list)

        return dock

    def create_actions(self):
        self.new_action = QAction(
            "New note",
            self,
        )
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(
            self.new_note
        )

        self.save_action = QAction(
            "Save note",
            self,
        )
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(
            self.save_note
        )

        self.delete_action = QAction(
            "Delete note",
            self,
        )
        self.delete_action.setShortcut("Delete")
        self.delete_action.triggered.connect(
            self.delete_note
        )

        self.pin_action = QAction(
            "Pin",
            self,
        )
        self.pin_action.setShortcut("Ctrl+P")
        self.pin_action.triggered.connect(
            self.toggle_pin
        )

        self.open_note_action = QAction(
            "Open in new window",
            self,
        )
        self.open_note_action.setShortcut(
            "Ctrl+Return"
        )
        self.open_note_action.triggered.connect(
            self.open_selected_note
        )

        self.new_window_action = QAction(
            "New window",
            self,
        )
        self.new_window_action.setShortcut(
            "Ctrl+Shift+N"
        )
        self.new_window_action.triggered.connect(
            self.open_new_window
        )

        self.close_window_action = QAction(
            "Close window",
            self,
        )
        self.close_window_action.setShortcut(
            "Ctrl+W"
        )
        self.close_window_action.triggered.connect(
            self.close
        )

        self.preferences_action = QAction(
            "Preferences...",
            self,
        )
        self.preferences_action.setShortcut(
            "Ctrl+,"
        )
        self.preferences_action.triggered.connect(
            self.open_preferences
        )

        self.all_action = QAction(
            "All",
            self,
        )
        self.all_action.triggered.connect(
            lambda: self.change_filter("all")
        )

        self.pinned_action = QAction(
            "Pinned",
            self,
        )
        self.pinned_action.triggered.connect(
            lambda: self.change_filter("pinned")
        )

        self.other_action = QAction(
            "Other",
            self,
        )
        self.other_action.triggered.connect(
            lambda: self.change_filter("other")
        )

        self.export_txt_action = QAction(
            "TXT",
            self,
        )
        self.export_txt_action.triggered.connect(
            self.export_txt
        )

        self.export_csv_action = QAction(
            "CSV",
            self,
        )
        self.export_csv_action.triggered.connect(
            self.export_csv
        )

        self.clear_all_action = QAction(
            "Clear all notes",
            self,
        )
        self.clear_all_action.triggered.connect(
            self.clear_all_notes
        )

        self.quit_action = QAction(
            "Quit",
            self,
        )
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(
            self.quit_application
        )

        self.about_action = QAction(
            "About",
            self,
        )
        self.about_action.triggered.connect(
            self.show_about
        )

    def create_menus(self):
        note_menu = self.menuBar().addMenu(
            "Note"
        )

        note_menu.addAction(
            self.new_action
        )

        note_menu.addAction(
            self.save_action
        )

        note_menu.addAction(
            self.delete_action
        )

        note_menu.addAction(
            self.pin_action
        )

        note_menu.addSeparator()

        note_menu.addAction(
            self.open_note_action
        )

        note_menu.addSeparator()

        note_menu.addAction(
            self.clear_all_action
        )

        note_menu.addSeparator()

        note_menu.addAction(
            self.quit_action
        )

        edit_menu = self.menuBar().addMenu(
            "Edit"
        )

        edit_menu.addAction(
            self.save_action
        )

        edit_menu.addAction(
            self.delete_action
        )

        export_menu = edit_menu.addMenu(
            "Export"
        )

        export_menu.addAction(
            self.export_txt_action
        )

        export_menu.addAction(
            self.export_csv_action
        )

        edit_menu.addSeparator()

        edit_menu.addAction(
            self.preferences_action
        )

        window_menu = self.menuBar().addMenu(
            "Window"
        )

        window_menu.addAction(
            self.new_window_action
        )

        window_menu.addAction(
            self.close_window_action
        )

        view_menu = self.menuBar().addMenu(
            "View"
        )

        view_menu.addAction(
            self.all_action
        )

        view_menu.addAction(
            self.pinned_action
        )

        view_menu.addAction(
            self.other_action
        )

        view_menu.addSeparator()

        view_menu.addAction(
            self.notes_dock.toggleViewAction()
        )

        help_menu = self.menuBar().addMenu(
            "Help"
        )

        help_menu.addAction(
            self.about_action
        )

    def create_toolbar(self):
        toolbar = self.addToolBar("Main")

        toolbar.setObjectName(
            f"MainToolbar{self.window_number}"
        )

        toolbar.addAction(
            self.new_action
        )

        toolbar.addAction(
            self.save_action
        )

        toolbar.addAction(
            self.delete_action
        )

        toolbar.addSeparator()

        toolbar.addAction(
            self.open_note_action
        )

        toolbar.addAction(
            self.new_window_action
        )

        toolbar.addSeparator()

        toolbar.addAction(
            self.pin_action
        )

        toolbar.addSeparator()

        toolbar.addAction(
            self.all_action
        )

        toolbar.addAction(
            self.pinned_action
        )

        toolbar.addAction(
            self.other_action
        )

        toolbar.addSeparator()

        export_button = QToolButton()

        export_button.setText("Export")

        export_button.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )

        export_menu = QMenu(self)

        export_menu.addAction(
            self.export_txt_action
        )

        export_menu.addAction(
            self.export_csv_action
        )

        export_button.setMenu(
            export_menu
        )

        toolbar.addWidget(
            export_button
        )

    def create_status_bar(self):
        self.statusBar().showMessage(
            "Ready"
        )

        self.window_status = QToolButton()

        self.window_status.setText(
            f"Window: {self.window_number}"
        )

        self.window_status.setEnabled(
            False
        )

        self.statusBar().addPermanentWidget(
            self.window_status
        )

        self.notes_status = QToolButton()

        self.notes_status.setText(
            "Notes: 0"
        )

        self.notes_status.setEnabled(
            False
        )

        self.statusBar().addPermanentWidget(
            self.notes_status
        )

    def load_notes(self):
        notes = self.storage.get_notes(
            self.app_state.current_filter
        )

        self.note_list.set_notes(
            notes,
            self.app_state.preview_length,
            self.app_state.pinned_first,
        )

        count = self.storage.count_notes(
            self.app_state.current_filter
        )

        self.notes_status.setText(
            f"Notes: {count}"
        )

    def refresh_from_state(self):
        self.load_notes()

        if (
            self.app_state.selected_note_id
            is not None
        ):
            note = self.storage.get_note(
                self.app_state.selected_note_id
            )

            if note is not None:
                self.editor.set_note_text(
                    note.text
                )

    def on_note_selected(self):
        note_id = (
            self.note_list.get_selected_note_id()
        )

        if note_id is None:
            return

        note = self.storage.get_note(
            note_id
        )

        if note is None:
            return

        self.app_state.select_note(
            note.id
        )

        self.editor.set_note_text(
            note.text
        )

    def new_note(self):
        self.app_state.start_new_note()

        self.note_list.clearSelection()

        self.editor.clear_note()

        self.editor.setFocus()

    def save_note(self):
        text = self.editor.get_text()

        if not text.strip():
            QMessageBox.warning(
                self,
                "Warning",
                "Note cannot be empty.",
            )
            return

        if self.app_state.is_new_note:
            note_id = self.storage.create_note(
                text
            )

            self.app_state.select_note(
                note_id
            )

            self.app_state.notes_changed.emit()

            return

        note_id = (
            self.app_state.selected_note_id
        )

        self.storage.update_note(
            note_id,
            text,
        )

        self.app_state.note_changed.emit(
            note_id
        )

        self.app_state.notes_changed.emit()

    def delete_note(self):
        note_id = (
            self.note_list.get_selected_note_id()
        )

        if note_id is None:
            QMessageBox.information(
                self,
                "Information",
                "Select a note first.",
            )
            return

        answer = QMessageBox.question(
            self,
            "Delete note",
            "Delete selected note?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if (
            answer
            != QMessageBox.StandardButton.Yes
        ):
            return

        self.storage.delete_note(
            note_id
        )

        self.app_state.note_changed.emit(
            note_id
        )

        self.app_state.start_new_note()

        self.editor.clear_note()

        self.app_state.notes_changed.emit()

    def toggle_pin(self):
        note_id = (
            self.note_list.get_selected_note_id()
        )

        if note_id is None:
            return

        self.storage.toggle_pin(
            note_id
        )

        self.app_state.note_changed.emit(
            note_id
        )

        self.app_state.notes_changed.emit()

    def change_filter(self, filter_name):
        self.app_state.set_filter(
            filter_name
        )

    def open_selected_note(self):
        note_id = (
            self.note_list.get_selected_note_id()
        )

        if note_id is None:
            QMessageBox.information(
                self,
                "Information",
                "Select a note first.",
            )
            return

        self.window_manager.open_note_window(
            note_id
        )

    def open_new_window(self):
        self.window_manager.open_main_window()

    def open_preferences(self):
        dialog = PreferencesDialog(
            self.app_state
        )

        dialog.exec()

    def clear_all_notes(self):
        answer = QMessageBox.question(
            self,
            "Clear all notes",
            "Delete all notes?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if (
            answer
            != QMessageBox.StandardButton.Yes
        ):
            return

        note_ids = [
            note.id
            for note in self.storage.get_notes(
                "all"
            )
        ]

        self.storage.delete_all()

        for note_id in note_ids:
            self.app_state.note_changed.emit(
                note_id
            )

        self.app_state.start_new_note()

        self.editor.clear_note()

        self.app_state.notes_changed.emit()

    def export_txt(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export TXT",
            "",
            "Text files (*.txt)",
        )

        if not file_name:
            return

        notes = self.storage.get_notes(
            "all"
        )

        with open(
            file_name,
            "w",
            encoding="utf-8",
        ) as file:
            for note in notes:
                file.write(
                    f"{note.id} | "
                    f"{note.created_at} | "
                    f"{note.text}\n"
                )

    def export_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV",
            "",
            "CSV files (*.csv)",
        )

        if not file_name:
            return

        notes = self.storage.get_notes(
            "all"
        )

        with open(
            file_name,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    "id",
                    "text",
                    "created_at",
                    "pinned",
                ]
            )

            for note in notes:
                writer.writerow(
                    [
                        note.id,
                        note.text,
                        note.created_at,
                        int(note.pinned),
                    ]
                )

    def show_about(self):
        QMessageBox.about(
            self,
            "About",
            f"{APP_TITLE}\n"
            f"{STUDENT_NAME}, {STUDENT_GROUP}",
        )

    def quit_application(self):
        self.window_manager.close_all_windows()
