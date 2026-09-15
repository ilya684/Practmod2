import csv

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QDockWidget,
    QMainWindow,
    QMessageBox,
    QToolButton,
    QMenu,
)

from app.config import APP_TITLE, STUDENT_GROUP, STUDENT_NAME
from app.state import AppState
from app.ui.note_editor_panel import NoteEditorPanel
from app.ui.note_list_panel import NoteListPanel


class MainWindow(QMainWindow):
    def __init__(self, storage):
        super().__init__()

        self.storage = storage
        self.state = AppState()

        self.setWindowTitle(
            f"{APP_TITLE} - {STUDENT_NAME}, {STUDENT_GROUP}"
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

        self.statusBar().showMessage("Filter: All | Notes: 0")

        self.load_notes()

    def create_notes_dock(self):
        dock = QDockWidget("Notes", self)
        dock.setObjectName("NotesDock")
        dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
            | Qt.DockWidgetArea.RightDockWidgetArea
        )

        self.note_list = NoteListPanel()
        self.note_list.itemSelectionChanged.connect(
            self.on_note_selected
        )

        dock.setWidget(self.note_list)

        return dock

    def create_actions(self):
        self.new_action = QAction("New", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_note)

        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_note)

        self.delete_action = QAction("Delete", self)
        self.delete_action.setShortcut("Delete")
        self.delete_action.triggered.connect(self.delete_note)

        self.pin_action = QAction("Pin", self)
        self.pin_action.setShortcut("Ctrl+P")
        self.pin_action.triggered.connect(self.toggle_pin)

        self.all_action = QAction("All", self)
        self.all_action.triggered.connect(
            lambda: self.change_filter("all")
        )

        self.pinned_action = QAction("Pinned", self)
        self.pinned_action.triggered.connect(
            lambda: self.change_filter("pinned")
        )

        self.other_action = QAction("Other", self)
        self.other_action.triggered.connect(
            lambda: self.change_filter("other")
        )

        self.export_txt_action = QAction("TXT", self)
        self.export_txt_action.triggered.connect(self.export_txt)

        self.export_csv_action = QAction("CSV", self)
        self.export_csv_action.triggered.connect(self.export_csv)

        self.clear_all_action = QAction("Clear all notes", self)
        self.clear_all_action.triggered.connect(self.clear_all_notes)

        self.quit_action = QAction("Quit", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)

    def create_menus(self):
        note_menu = self.menuBar().addMenu("Note")
        note_menu.addAction(self.new_action)
        note_menu.addAction(self.save_action)
        note_menu.addAction(self.delete_action)
        note_menu.addAction(self.pin_action)
        note_menu.addSeparator()
        note_menu.addAction(self.clear_all_action)

        edit_menu = self.menuBar().addMenu("Edit")
        edit_menu.addAction(self.new_action)
        edit_menu.addAction(self.save_action)
        edit_menu.addAction(self.delete_action)

        export_menu = edit_menu.addMenu("Export")
        export_menu.addAction(self.export_txt_action)
        export_menu.addAction(self.export_csv_action)

        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction(self.all_action)
        view_menu.addAction(self.pinned_action)
        view_menu.addAction(self.other_action)
        view_menu.addSeparator()
        view_menu.addAction(self.notes_dock.toggleViewAction())

        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_action)
        help_menu.addSeparator()
        help_menu.addAction(self.quit_action)

    def create_toolbar(self):
        toolbar = self.addToolBar("Main")
        toolbar.setObjectName("MainToolbar")

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.save_action)
        toolbar.addAction(self.delete_action)
        toolbar.addAction(self.pin_action)

        toolbar.addSeparator()

        toolbar.addAction(self.all_action)
        toolbar.addAction(self.pinned_action)
        toolbar.addAction(self.other_action)

        toolbar.addSeparator()

        export_button = QToolButton()
        export_button.setText("Export")
        export_button.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )

        export_menu = QMenu(self)
        export_menu.addAction(self.export_txt_action)
        export_menu.addAction(self.export_csv_action)

        export_button.setMenu(export_menu)
        toolbar.addWidget(export_button)

    def load_notes(self):
        try:
            notes = self.storage.get_notes(
                self.state.current_filter
            )

            self.note_list.set_notes(notes)

            count = self.storage.count_notes(
                self.state.current_filter
            )

            filter_names = {
                "all": "All",
                "pinned": "Pinned",
                "other": "Other",
            }

            filter_name = filter_names.get(
                self.state.current_filter,
                "All",
            )

            self.statusBar().showMessage(
                f"Filter: {filter_name} | Notes: {count}"
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error),
            )

    def on_note_selected(self):
        note_id = self.note_list.get_selected_note_id()

        if note_id is None:
            return

        try:
            note = self.storage.get_note(note_id)

            if note is None:
                return

            self.state.select_note(note.id)
            self.editor.set_note_text(note.text)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error),
            )

    def new_note(self):
        self.state.start_new_note()
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

        try:
            if self.state.is_new_note:
                note_id = self.storage.create_note(text)
                self.state.select_note(note_id)
            else:
                self.storage.update_note(
                    self.state.selected_note_id,
                    text,
                )

            self.load_notes()
            self.select_note_by_id(
                self.state.selected_note_id
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error),
            )

    def select_note_by_id(self, note_id):
        if note_id is None:
            return

        for index in range(self.note_list.count()):
            item = self.note_list.item(index)

            if item.data(Qt.ItemDataRole.UserRole) == note_id:
                self.note_list.setCurrentItem(item)
                return

    def delete_note(self):
        note_id = self.note_list.get_selected_note_id()

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

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self.storage.delete_note(note_id)
            self.state.start_new_note()
            self.editor.clear_note()
            self.load_notes()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error),
            )

    def toggle_pin(self):
        note_id = self.note_list.get_selected_note_id()

        if note_id is None:
            QMessageBox.information(
                self,
                "Information",
                "Select a note first.",
            )
            return

        try:
            self.storage.toggle_pin(note_id)
            self.load_notes()
            self.select_note_by_id(note_id)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error),
            )

    def change_filter(self, filter_name):
        self.state.set_filter(filter_name)
        self.load_notes()

    def clear_all_notes(self):
        answer = QMessageBox.question(
            self,
            "Clear all notes",
            "Delete all notes?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self.storage.delete_all()
            self.state.start_new_note()
            self.editor.clear_note()
            self.load_notes()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error),
            )

    def export_txt(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export TXT",
            "",
            "Text files (*.txt)",
        )

        if not file_name:
            return

        try:
            notes = self.storage.get_notes("all")

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

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error),
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

        try:
            notes = self.storage.get_notes("all")

            with open(
                file_name,
                "w",
                newline="",
                encoding="utf-8",
            ) as file:
                writer = csv.writer(file)

                writer.writerow(
                    ["id", "text", "created_at", "pinned"]
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

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error),
            )

    def show_about(self):
        QMessageBox.about(
            self,
            "About",
            f"{APP_TITLE}\n"
            f"{STUDENT_NAME}, {STUDENT_GROUP}",
        )

    def closeEvent(self, event):
        self.storage.close()
        event.accept()
