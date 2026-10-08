import os
import sys

from PyQt6.QtWidgets import QApplication, QStyleFactory, QMainWindow
from pathlib import Path


class MainWindow(QMainWindow):


def main():
	style_path = os.path.join(
		"gui_tester/resources",
		"styles",
		"dark.qss"
	)

	app = QApplication(sys.argv)
	app.setStyle(QStyleFactory.create("Fusion"))

	with open(style_path) as f:
		app.setStyleSheet(f.read())


	window.show()

	sys.exit(app.exec())


if __name__ == '__main__':

	main()
