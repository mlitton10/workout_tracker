from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout
from src.widgets.template_widgets.basic_app_widget import BasicAppWidget
from src.widgets.template_widgets.basic_plot_widget import PlotWidget
from src.widgets.template_widgets.input_widgets import DropdownRow


class PaceDisplayWidget(PlotWidget):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent, width, height, dpi)



class PaceDisplaySelection(BasicAppWidget):
    durationSelected = pyqtSignal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.file_drop_down = DropdownRow("Select Device: ", ["Week", "Month", "Year", "All"], parent)
        self._initialize_widget()

    def _connect_signals(self):
        self.file_drop_down.optionSelected.connect(self._emit_selection)

    def _build_layout(self):
        main_layout = QGridLayout(self)

        self.file_drop_down.layout().setContentsMargins(0, 0, 0, 0)
        self.file_drop_down.layout().setSpacing(0)

        main_layout.addWidget(self.file_drop_down, 0, 1)

    def _initialize_widget(self):
        self._build_layout()
        self._connect_signals()

    def _emit_selection(self, index: int):
        duration = self.current_duration()
        self.durationSelected.emit(duration, 'Pace')

    def current_duration(self) -> str:
        return self.file_drop_down.current_option()
