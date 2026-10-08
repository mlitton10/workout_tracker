from PyQt6.QtCore import QThread, QThreadPool
from PyQt6.QtWidgets import (
    QWidget
)

from src.widgets.template_widgets.generic_worker import Worker


class ApplicationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.thread = None
        self.worker = None

        self.threadpool = QThreadPool()

    def _build_layout(self):
        raise NotImplementedError("build_layout not implemented")

    def _connect_signals(self):
        raise NotImplementedError("connect_signals not implemented")

    def _initialize_tab(self):
        raise NotImplementedError("initialize_tab not implemented")

    def shutdown(self):
        """Stop both the calculation thread and the persistent Pi thread."""
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

    def run_worker_async(self, worker: Worker, finished_call, failed_call, widget=None):
        self.thread = QThread(self)
        self.worker = worker

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(finished_call)
        self.worker.failed.connect(failed_call)

        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.failed.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: self.on_thread_finished(widget))

        self.thread.start()

    def on_thread_finished(self, widget=None):
        self.thread = None
        self.worker = None
        if widget is not None:
            widget.setEnabled(True)

