from PyQt6.QtWidgets import QGridLayout, QMessageBox, QPushButton

from src.widgets.cardio_widgets.data_entry import RunEntryDialog
from src.widgets.cardio_widgets.pace_display_widget import (
    DisplaySelectionWidget,
    PaceDisplayWidget,
)
from src.widgets.template_widgets.basic_application_tabs import ApplicationTab
from src.widgets.template_widgets.basic_plot_widget import SERIES_COLORS
from src.workers.file_reader import LoadFileWorker

CARDIO_DATA_PATH = "./src/data/cardio/runs.csv"
CARDIO_COLUMNS = ['Date', 'Pace', 'Distance']


class Cardio(ApplicationTab):
    def __init__(self, data_path: str = CARDIO_DATA_PATH):
        super().__init__()

        self.data_path = data_path
        # Columns whose plot must reload once its in-flight load finishes.
        self._pending_reloads = set()

        self.pace_display_selection = DisplaySelectionWidget('Pace')
        self.pace_display = PaceDisplayWidget(labels=['Date', 'Pace [min/mile]'], color=SERIES_COLORS['Pace'])

        self.distance_display_selection = DisplaySelectionWidget('Distance')
        self.distance_display = PaceDisplayWidget(labels=['Date', 'Distance [mi]'],
                                                  color=SERIES_COLORS['Distance'])

        self.log_run_button = QPushButton("Log Run")

        self._initialize_tab()

    def _build_layout(self):
        layout = QGridLayout(self)
        layout.addWidget(self.pace_display, 0, 0, 3,3)
        layout.addWidget(self.pace_display_selection, 3, 0,1,1)

        layout.addWidget(self.distance_display, 0, 3, 3, 3)
        layout.addWidget(self.distance_display_selection, 3, 3, 1, 1)

        layout.addWidget(self.log_run_button, 3, 5, 1, 1)


    def _connect_signals(self):
        self.pace_display_selection.durationSelected.connect(self.load_file_async)
        self.distance_display_selection.durationSelected.connect(self.load_file_async)
        self.log_run_button.clicked.connect(self.log_run)

    def _initialize_tab(self):
        self._build_layout()
        self._connect_signals()
        self.refresh()

    def _targets(self):
        return {'Pace': (self.pace_display, self.pace_display_selection),
                'Distance': (self.distance_display, self.distance_display_selection)}

    def log_run(self):
        self.open_entry_dialog(RunEntryDialog(self), self.data_path, CARDIO_COLUMNS)

    def refresh(self):
        for column, (_widget, selector) in self._targets().items():
            if selector.isEnabled():
                self.load_file_async(selector.current_duration(), column)
            else:
                # A load is in flight and may have read the old file; reload after it.
                self._pending_reloads.add(column)

    def load_file_async(self, duration, column):
        widget, selector = self._targets()[column]

        # The selector stays disabled until its load finishes, so a plot never
        # has two loads in flight. Loads for different plots can run in parallel.
        selector.setEnabled(False)
        self.run_worker_async(LoadFileWorker(self.data_path, duration, column),
                                lambda *args, w=widget: self.on_load_finished(*args, widget=w), self.on_load_failed, selector)

    def on_thread_finished(self, widget=None):
        super().on_thread_finished(widget)
        column = getattr(widget, 'data_column', None)
        if column in self._pending_reloads:
            self._pending_reloads.discard(column)
            self.load_file_async(widget.current_duration(), column)

    def on_load_finished(self, x, y, m, b, plotting_deltas, widget=None):
        widget.update_plot(x, y, m, b, plotting_deltas)

    def on_load_failed(self, message: str):
        QMessageBox.critical(self, "Load Error", message)
