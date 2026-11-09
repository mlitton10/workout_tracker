from datetime import date, timedelta

import numpy as np
import pandas as pd
from PyQt6.QtCore import pyqtSignal

from src.widgets.template_widgets.generic_worker import Worker


def convert_date_strings(date_string_array):
    return np.array([date.fromisoformat(d) for d in date_string_array])

def select_for_duration(dates, duration):
    if duration.lower() == 'week':
        duration_int = 7
    elif duration.lower() == 'month':
        duration_int = 30
    elif duration.lower() == 'three months':
        duration_int = 90
    elif duration.lower() == '6 months':
        duration_int = 180
    elif duration.lower() == 'year':
        duration_int = 365
    elif duration.lower() == 'all':
        good_inds = np.arange(len(dates))
        return good_inds

    duration_delta = timedelta(days=duration_int)

    good_inds = date.today() - duration_delta < dates
    return good_inds

def fit_data(dates, values):
    today = date.today()
    deltas = today - dates
    deltas_ints = np.array([float(delta.days) for delta in deltas])

    m, b = np.polyfit(deltas_ints, values, 1)

    return m, b, deltas_ints

class LoadFileWorker(Worker):
    finished = pyqtSignal(list, list, float, float, np.ndarray)

    def __init__(self, filepath: str, duration, column):
        super().__init__()
        self.filepath = filepath
        self.column = column
        self.duration = duration

    def do_work(self):
        date_strings, values = self.load_csv_data(self.filepath, self.column)

        dates = convert_date_strings(date_strings)
        filter_for_duration = select_for_duration(dates, self.duration)

        good_dates = dates[filter_for_duration]
        good_values = values[filter_for_duration]


        m,b, plotting_deltas = fit_data(good_dates, good_values)

        return good_dates, good_values, m, b, plotting_deltas

    def load_csv_data(self, filepath: str, column):

        dataframe = pd.read_csv(filepath)

        date_strings = dataframe['Date'].to_list()
        values = dataframe[column].to_numpy()

        return date_strings, values
