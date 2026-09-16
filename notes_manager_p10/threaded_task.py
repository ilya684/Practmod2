import sys

from PySide6.QtCore import QObject, QThread, Signal, Slot
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


class Worker(QObject):
    progress = Signal(int)
    finished = Signal()

    @Slot()
    def run(self):
        for step in range(1, STEP_COUNT + 1):
            QThread.currentThread().msleep(SLEEP_MS)
            self.progress.emit(step)

        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            f"{APP_TITLE} - {STUDENT_NAME}, {STUDENT_GROUP}"
        )
        self.resize(500, 300)

        self.status_label = QLabel("Ready")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, STEP_COUNT)
        self.progress_bar.setValue(0)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_task)

        self.click_button = QPushButton("Click me (0)")
        self.click_count = 0
        self.click_button.clicked.connect(self.count_click)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)
        layout.addWidget(self.click_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.thread = None
        self.worker = None

    def start_task(self):
        if self.thread is not None and self.thread.isRunning():
            return

        self.status_label.setText("Working...")
        self.progress_bar.setValue(0)
        self.start_button.setEnabled(False)

        self.thread = QThread()
        self.worker = Worker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.task_finished)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread_finished)

        self.thread.start()

    @Slot(int)
    def update_progress(self, step):
        self.progress_bar.setValue(step)

    @Slot()
    def task_finished(self):
        self.status_label.setText("Done")
        self.start_button.setEnabled(True)

    @Slot()
    def thread_finished(self):
        self.worker = None
        self.thread = None

    def count_click(self):
        self.click_count += 1
        self.click_button.setText(
            f"Click me ({self.click_count})"
        )

    def closeEvent(self, event):
        if self.thread is not None:
            if self.thread.isRunning():
                self.thread.quit()
                self.thread.wait(3000)

            self.thread = None
            self.worker = None

        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
