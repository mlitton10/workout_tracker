from PyQt6.QtWidgets import QGridLayout, QMessageBox

from src.widgets.cardio_widgets.pace_display_widget import (
    DisplaySelectionWidget,
    PaceDisplayWidget,
)
from src.widgets.template_widgets.basic_application_tabs import ApplicationTab
from src.workers.file_reader import LoadFileWorker


class Cardio(ApplicationTab):
    def __init__(self):
        super().__init__()

        self.pace_display_selection = DisplaySelectionWidget('Pace')
        self.pace_display = PaceDisplayWidget(labels=['Date', 'Pace'])

        self.distance_display_selection = DisplaySelectionWidget('Distance')
        self.distance_display = PaceDisplayWidget(labels=['Date', 'Distance'])

        self._initialize_tab()

    def _build_layout(self):
        layout = QGridLayout(self)
        layout.addWidget(self.pace_display, 0, 0, 3,3)
        layout.addWidget(self.pace_display_selection, 3, 0,1,1)

        layout.addWidget(self.distance_display, 0, 3, 3, 3)
        layout.addWidget(self.distance_display_selection, 3, 3, 1, 1)


    def _connect_signals(self):
        self.pace_display_selection.durationSelected.connect(self.load_file_async)
        self.distance_display_selection.durationSelected.connect(self.load_file_async)

    def _initialize_tab(self):
        self._build_layout()
        self._connect_signals()

        self.load_file_async(self.pace_display_selection.current_duration(), 'Pace')
        self.load_file_async(self.distance_display_selection.current_duration(), 'Distance')

    def load_file_async(self, duration, column):
        targets = {'Pace': (self.pace_display, self.pace_display_selection),
                    'Distance': (self.distance_display, self.distance_display_selection)}

        widget, selector = targets[column]

        # The selector stays disabled until its load finishes, so a plot never
        # has two loads in flight. Loads for different plots can run in parallel.
        selector.setEnabled(False)
        self.run_worker_async(LoadFileWorker("./src/data/test.csv", duration, column),
                                lambda *args, w=widget: self.on_load_finished(*args, widget=w), self.on_load_failed, selector)


    def on_load_finished(self, x, y, m, b, plotting_deltas, widget=None):
        widget.update_plot(x, y, m, b, plotting_deltas)

    def on_load_failed(self, message: str):
        QMessageBox.critical(self, "Load Error", message)




