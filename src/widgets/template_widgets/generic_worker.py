from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class Worker(QObject):
    finished = pyqtSignal()
    failed = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def run(self):
        try:
            result = self.do_work()
            self.finished.emit(*result)
        except Exception as e:  # noqa: BLE001 - report any worker failure to the UI thread
            self.failed.emit(str(e))

    def do_work(self):
        raise NotImplementedError()