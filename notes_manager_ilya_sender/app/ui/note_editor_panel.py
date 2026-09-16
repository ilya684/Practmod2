from PySide6.QtWidgets import QTextEdit


class NoteEditorPanel(QTextEdit):
    def get_text(self):
        return self.toPlainText()

    def set_note_text(self, text):
        self.setPlainText(text)

    def clear_note(self):
        self.clear()
