from PyQt6.QtCore import QThread, QThreadPool
from PyQt6.QtWidgets import QWidget

from src.widgets.template_widgets.generic_worker import Worker


class ApplicationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.thread = None
        self.worker = None
        self._jobs = []

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
        thread = QThread(self)
        job = (thread, worker)
        self._jobs.append(job)

        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.finished.connect(finished_call)
        worker.failed.connect(failed_call)

        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(worker.deleteLater)

        def cleanup():
            self._jobs.remove(job)
            self.on_thread_finished(widget)

        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(cleanup)

        thread.start()

    def on_thread_finished(self, widget=None):
        if widget is not None:
            widget.setEnabled(True)

