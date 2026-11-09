from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGridLayout

from src.widgets.template_widgets.basic_app_widget import BasicAppWidget
from src.widgets.template_widgets.basic_plot_widget import PlotWidget
from src.widgets.template_widgets.input_widgets import DropdownRow


class PaceDisplayWidget(PlotWidget):
    def __init__(self, parent=None, width=5, height=4, dpi=100, labels=("", "")):
        super().__init__(parent, width, height, dpi, labels=labels)


class DisplaySelectionWidget(BasicAppWidget):
    durationSelected = pyqtSignal(str, str)
    def __init__(self,data_column:str, parent=None):
        super().__init__(parent=parent)
        self.data_column = data_column
        self.file_drop_down = DropdownRow("Duration: ",
                                          ["Week", "Month", "Three Months", "6 Months", "Year", "All"],
                                          self)
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

    def _emit_selection(self):
        duration = self.current_duration()
        self.durationSelected.emit(duration, self.data_column)

    def current_duration(self) -> str:
        return self.file_drop_down.current_option()
