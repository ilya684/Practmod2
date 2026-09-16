import sys
import time

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

STUDENT_NAME = "Ilya Sender"
STUDENT_GROUP = "IT-42"
APP_TITLE = "Task Demo"
STEP_COUNT = 10
SLEEP_MS = 500


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            f"{APP_TITLE} - "
            f"{STUDENT_NAME}, {STUDENT_GROUP}"
        )

        self.resize(500, 300)

        self.status_label = QLabel("Ready")

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(STEP_COUNT)
        self.progress_bar.setValue(0)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(
            self.start_task
        )

        self.click_button = QPushButton(
            "Click me (0)"
        )
        self.click_count = 0
        self.click_button.clicked.connect(
            self.count_click
        )

        layout = QVBoxLayout()

        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)
        layout.addWidget(self.click_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_task(self):
        self.status_label.setText("Working...")
        self.progress_bar.setValue(0)
        self.start_button.setEnabled(False)

        for step in range(1, STEP_COUNT + 1):
            time.sleep(SLEEP_MS / 1000)
            self.progress_bar.setValue(step)

        self.status_label.setText("Done")
        self.start_button.setEnabled(True)

    def count_click(self):
        self.click_count += 1
        self.click_button.setText(
            f"Click me ({self.click_count})"
        )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
