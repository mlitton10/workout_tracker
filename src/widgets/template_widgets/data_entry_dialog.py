from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLabel, QVBoxLayout


class DataEntryDialog(QDialog):
    """Popup form that produces one record (column -> value) for a tab's CSV.

    Subclasses implement:
      _build_fields(form)  add input widgets to the QFormLayout
      _validate()          return an error message, or None if the input is valid
      get_record()         return {column: value} for the entered data
    The dialog only closes on OK once _validate() passes.
    """

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(320)

        self.form = QFormLayout()
        self._build_fields(self.form)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #f28b82;")
        self.error_label.setWordWrap(True)
        self.error_label.hide()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                                   | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(self.form)
        layout.addWidget(self.error_label)
        layout.addWidget(buttons)

    def _build_fields(self, form: QFormLayout):
        raise NotImplementedError("Add the input fields")

    def _validate(self) -> str | None:
        raise NotImplementedError("Validate the input")

    def get_record(self) -> dict:
        raise NotImplementedError("Return the entered record")

    def accept(self):
        error = self._validate()
        if error:
            self.error_label.setText(error)
            self.error_label.show()
            return
        super().accept()
