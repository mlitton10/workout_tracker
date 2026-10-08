from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject


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
        except Exception as e:
            self.failed.emit(str(e))

    def do_work(self):
        raise NotImplementedError()