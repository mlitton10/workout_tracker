import pandas as pd

from PyQt6.QtCore import pyqtSignal
from src.widgets.template_widgets.generic_worker import Worker


class LoadFileWorker(Worker):
    finished = pyqtSignal(list, list)   # filepath, length, radius

    def __init__(self, filepath: str, column, duration):
        super().__init__()
        self.filepath = filepath
        self.column = column
        self.duration = duration

    def do_work(self):
        dates, value = self.load_csv(self.filepath, self.column)


        return

    def load_csv(self, filepath: str, column):

        dataframe = pd.read_csv(filepath)

        dates = dataframe['Date']
        values = dataframe[column]

        return dates, values
