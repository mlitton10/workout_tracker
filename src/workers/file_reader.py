from datetime import date, timedelta

import numpy as np
import pandas as pd
from PyQt6.QtCore import pyqtSignal

from src.widgets.template_widgets.generic_worker import Worker


def convert_date_strings(date_string_array):
    return np.array([date.fromisoformat(d) for d in date_string_array])

DURATION_DAYS = {
    'week': 7,
    'month': 30,
    'three months': 90,
    '6 months': 180,
    'year': 365,
}


def select_for_duration(dates, duration):
    key = duration.lower()
    if key == 'all':
        return np.ones(len(dates), dtype=bool)
    if key not in DURATION_DAYS:
        raise ValueError(f"Unknown duration: {duration!r}")

    return dates > date.today() - timedelta(days=DURATION_DAYS[key])

def fit_data(dates, values):
    """Linear fit of values vs. days-before-today. Returns NaN slope/intercept
    when there are fewer than 2 points to fit."""
    today = date.today()
    deltas_ints = np.array([float((today - d).days) for d in dates])

    if len(deltas_ints) < 2:
        return float('nan'), float('nan'), deltas_ints

    m, b = np.polyfit(deltas_ints, values, 1)

    return float(m), float(b), deltas_ints

class LoadFileWorker(Worker):
    finished = pyqtSignal(object, object, float, float, object)

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
