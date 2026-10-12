from PyQt6.QtWidgets import QGridLayout, QMessageBox
from src.widgets.cardio_widgets.pace_display_widget import PaceDisplayWidget, DisplaySelectionWidget
from src.widgets.template_widgets.basic_application_tabs import ApplicationTab
from src.workers.file_reader import LoadFileWorker


class Cardio(ApplicationTab):
    def __init__(self, test=True):
        super().__init__()

        self.test=test

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

        pass

    def _connect_signals(self):
        pass

    def _initialize_tab(self):
        self._build_layout()
        self._connect_signals()

        pass

    def load_file_async(self, filepath: str):
        # If a load is already running, ignore new requests for simplicity.
        if self.thread is not None and self.thread.isRunning():
            return

        self.ds.setEnabled(False)

        self.run_worker_async(LoadMachineWorker(filepath), self.on_load_finished, self.on_load_failed, self.ds)

    def on_load_finished(self, filepath: str, length: float, radius: float):
        self.canvas.update_machine_radial_outline(radius)

    #		self.status_label.setText(f"Loaded {os.path.basename(filepath)}")

    def on_load_failed(self, message: str):
        #		self.status_label.setText("Load failed")
        QMessageBox.critical(self, "Load Error", message)




