import os
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QStyleFactory, QTabWidget

from src.widgets.cardio import Cardio


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Matt's Workout Tracker")

		self.cardio_tab = Cardio()

		tabs = QTabWidget()
		tabs.addTab(self.cardio_tab, "Cardio")

		self.setCentralWidget(tabs)
		self.resize(1600, 700)

	def closeEvent(self, event):
		self.cardio_tab.shutdown()
		super().closeEvent(event)

def main():
	style_path = os.path.join(
		"src/resources",
		"styles",
		"dark.qss"
	)

	app = QApplication(sys.argv)
	app.setStyle(QStyleFactory.create("Fusion"))

	with open(style_path) as f:
		app.setStyleSheet(f.read())

	window = MainWindow()
	window.show()

	sys.exit(app.exec())


if __name__ == '__main__':

	main()
