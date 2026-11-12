import re

from PyQt6.QtCore import QDate, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QDateEdit, QDoubleSpinBox, QFormLayout, QLineEdit

from src.widgets.template_widgets.data_entry_dialog import DataEntryDialog

PACE_PATTERN = r"^\d{1,2}:[0-5]\d$"


def parse_pace(text: str) -> float:
    """Convert an 'mm:ss' pace (e.g. '8:45') to decimal minutes (8.75)."""
    text = text.strip()
    if not re.match(PACE_PATTERN, text):
        raise ValueError(f"Pace must look like 8:45 (mm:ss), got {text!r}")
    minutes, seconds = text.split(":")
    return int(minutes) + int(seconds) / 60


class RunEntryDialog(DataEntryDialog):
    def __init__(self, parent=None):
        super().__init__("Log Run", parent)

    def _build_fields(self, form: QFormLayout):
        today = QDate.currentDate()
        self.date_edit = QDateEdit(today)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMaximumDate(today)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")

        self.distance_edit = QDoubleSpinBox()
        self.distance_edit.setRange(0.01, 100.0)
        self.distance_edit.setDecimals(2)
        self.distance_edit.setSingleStep(0.1)
        self.distance_edit.setSuffix(" mi")
        self.distance_edit.setValue(1.0)

        self.pace_edit = QLineEdit()
        self.pace_edit.setPlaceholderText("8:45")
        self.pace_edit.setValidator(QRegularExpressionValidator(QRegularExpression(PACE_PATTERN)))

        form.addRow("Date:", self.date_edit)
        form.addRow("Distance:", self.distance_edit)
        form.addRow("Pace (min/mi):", self.pace_edit)

    def _validate(self) -> str | None:
        if not self.pace_edit.text().strip():
            return "Enter a pace, e.g. 8:45."
        try:
            pace = parse_pace(self.pace_edit.text())
        except ValueError as e:
            return str(e)
        if pace <= 0:
            return "Pace must be greater than 0:00."
        return None

    def get_record(self) -> dict:
        return {
            'Date': self.date_edit.date().toString("yyyy-MM-dd"),
            'Pace': round(parse_pace(self.pace_edit.text()), 4),
            'Distance': round(self.distance_edit.value(), 2),
        }
