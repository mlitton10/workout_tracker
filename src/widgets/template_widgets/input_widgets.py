from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout


class DropdownRow(QWidget):
    optionSelected = pyqtSignal(str)

    def __init__(self, label_text: str, options: list[str], parent=None):
        super().__init__(parent)

        self.options = options

        self.label = QLabel(label_text)
        self.combo = QComboBox()
        self.combo.addItems(options)

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.combo)

        self.combo.currentIndexChanged.connect(self._emit_selected_option)

    def _emit_selected_option(self, index: int):
        if 0 <= index < len(self.options):
            self.optionSelected.emit(self.options[index])

    def current_option(self) -> str:
        return self.options[self.combo.currentIndex()]
