import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QSizePolicy

rc_dict = {"figure.autolayout": True, "font.family": 'serif', 'font.size': 18.0,
		   'lines.linewidth': 2.5, 'axes.titlepad':8.0,
          'xtick.minor.visible':True,'ytick.minor.visible':True, 'axes.linewidth':2.0, 'xtick.major.width':2.0,
		   'xtick.direction': 'in',
          'ytick.direction':'in','ytick.major.width':2.3,'xtick.minor.width':1.0,'ytick.minor.width':1.0,
		   'xtick.major.size':8.0,'ytick.major.size':8.0,
          'xtick.minor.size':4.0, 'ytick.minor.size': 4.0, 'savefig.pad_inches': 0.05}

plt.rcParams.update(rc_dict)


class PlotWidget(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100, labels=("", "")):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._initialize_canvas(labels)


    def _initialize_canvas(self, labels):

        self.scatter_plot = self.axes.scatter([], [], alpha=0)
        self.line_of_best_fit = self.axes.plot([],[], alpha=0)[0]
        self.axes.set_xlabel(labels[0])
        self.axes.set_ylabel(labels[1])
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.no_data_text = self.axes.text(0.5, 0.5, "No data in selected range",
                                           transform=self.axes.transAxes,
                                           ha='center', va='center', visible=False)

        #ax.set_aspect('equal')


    def clear_line_of_best_fit(self):
        self.line_of_best_fit.remove()

    def clear_scatter(self):
        self.scatter_plot.remove()

    def clear_all(self):
        self.clear_line_of_best_fit()
        self.clear_scatter()

    def update_plot(self, x, y, m, b, plotting_deltas):
        self.clear_all()
        self.no_data_text.set_visible(len(x) == 0)
        self.scatter_plot = self.axes.scatter(x, y, color='C0')

        if np.isnan(m):  # fewer than 2 points, so no fit
            self.line_of_best_fit = self.axes.plot([], [])[0]
        else:
            self.line_of_best_fit = self.axes.plot(x, m * plotting_deltas + b, color='C0')[0]

        if len(x) > 0:
            self.axes.set_xlim(np.min(x) - datetime.timedelta(days=3), np.max(x)+datetime.timedelta(days=3))
            self.axes.set_ylim(np.min(y) * 0.9, np.max(y) * 1.1)
        self.draw()


