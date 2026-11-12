from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QDialog, QMessageBox, QWidget

from src.utils.csv_store import append_record
from src.widgets.template_widgets.data_entry_dialog import DataEntryDialog
from src.widgets.template_widgets.generic_worker import Worker


class ApplicationTab(QWidget):
    def __init__(self):
        super().__init__()

        self._jobs = []

    def _build_layout(self):
        raise NotImplementedError("build_layout not implemented")

    def _connect_signals(self):
        raise NotImplementedError("connect_signals not implemented")

    def _initialize_tab(self):
        raise NotImplementedError("initialize_tab not implemented")

    def refresh(self):
        """Reload the tab's displays after its data has changed."""
        raise NotImplementedError("refresh not implemented")

    def open_entry_dialog(self, dialog: DataEntryDialog, filepath: str, columns: list[str]) -> bool:
        """Show a data-entry popup; if accepted, append its record and refresh.
        Returns True if a record was saved."""
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return False
        try:
            append_record(filepath, columns, dialog.get_record())
        except OSError as e:
            QMessageBox.critical(self, "Save Error", f"Could not save to {filepath}:\n{e}")
            return False
        self.refresh()
        return True

    def shutdown(self):
        """Stop every worker thread that's still running and wait for it to exit."""
        for thread, _worker in list(self._jobs):
            if thread.isRunning():
                thread.quit()
                thread.wait()

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

