import pandas as pd

from PyQt6.QtCore import pyqtSignal
from fake_data_maker import good_inds
from src.widgets.template_widgets.generic_worker import Worker
from datetime import date, timedelta
import numpy as np

def convert_date_strings(date_string_array):
    return np.array([date.fromisoformat(d) for d in date_string_array])

def select_for_duration(dates, duration):
    if duration.lower() == 'week':
        duration_int = 7
    elif duration.lower() == 'month':
        duration_int = 30
    elif duration.lower() == 'year':
        duration_int = 365

    duration_delta = timedelta(days=duration_int)

    good_inds = date.today() - duration_delta < dates

    return good_inds


class LoadFileWorker(Worker):
    finished = pyqtSignal(list, list)   # filepath, length, radius

    def __init__(self, filepath: str, column, duration):
        super().__init__()
        self.filepath = filepath
        self.column = column
        self.duration = duration

    def do_work(self):
        date_strings, value = self.load_csv_data(self.filepath, self.column)

        dates = convert_date_strings(date_strings)

        filter_for_duration = select_for_duration(dates, self.duration)

        good_dates = dates[filter_for_duration]
        good_values = value[filter_for_duration]

        return good_dates, good_values

    def load_csv_data(self, filepath: str, column):

        dataframe = pd.read_csv(filepath)

        date_strings = dataframe['Date']
        values = dataframe[column]

        return date_strings, values
