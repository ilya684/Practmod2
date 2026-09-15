from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem


class NoteListPanel(QListWidget):
    def set_notes(self, notes):
        self.clear()

        for note in notes:
            title = note.text.strip().replace("\n", " ")

            if not title:
                title = "Empty note"

            if len(title) > 50:
                title = title[:50] + "..."

            if note.pinned:
                title = "[PIN] " + title

            item = QListWidgetItem(title)
            item.setData(Qt.ItemDataRole.UserRole, note.id)
            self.addItem(item)

    def get_selected_note_id(self):
        item = self.currentItem()

        if item is None:
            return None

        return item.data(Qt.ItemDataRole.UserRole)
