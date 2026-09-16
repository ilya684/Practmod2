from PySide6.QtGui import QFont
from PySide6.QtWidgets import QTextEdit


class NoteEditorPanel(QTextEdit):
    def get_text(self):
        return self.toPlainText()

    def set_note_text(self, text):
        self.setPlainText(text)

    def clear_note(self):
        self.clear()

    def apply_font_size(self, size):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)
