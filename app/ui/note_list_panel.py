from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem


class NoteListPanel(QListWidget):
    def set_notes(
        self,
        notes,
        preview_length=30,
        pinned_first=True,
    ):
        self.clear()

        if pinned_first:
            notes = sorted(
                notes,
                key=lambda note: not note.pinned,
            )

        for note in notes:
            title = note.text.strip().replace(
                "\n",
                " ",
            )

            if not title:
                title = "Empty note"

            if len(title) > preview_length:
                title = (
                    title[:preview_length]
                    + "..."
                )

            if note.pinned:
                title = "[PIN] " + title

            item = QListWidgetItem(title)

            item.setData(
                Qt.ItemDataRole.UserRole,
                note.id,
            )

            self.addItem(item)

    def get_selected_note_id(self):
        item = self.currentItem()

        if item is None:
            return None

        return item.data(
            Qt.ItemDataRole.UserRole
        )
