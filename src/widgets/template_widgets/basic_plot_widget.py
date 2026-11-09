import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QSizePolicy

# Colors match src/resources/styles/dark.qss
SURFACE = '#202124'
TEXT = '#e8eaed'
MUTED = '#8a8d91'
AXIS = '#55585c'
GRID = '#35383c'

# One fixed color per metric, used everywhere that metric is plotted.
# Validated against SURFACE for colorblind separation and >= 3:1 contrast.
SERIES_COLORS = {'Pace': '#3987e5', 'Distance': '#d95926'}
DEFAULT_COLOR = SERIES_COLORS['Pace']

rc_dict = {
    'figure.facecolor': SURFACE, 'axes.facecolor': SURFACE, 'savefig.facecolor': SURFACE,
    'figure.autolayout': True,
    'font.family': 'sans-serif', 'font.size': 15,
    'text.color': TEXT, 'axes.labelcolor': MUTED, 'axes.titlecolor': TEXT,
    'axes.edgecolor': AXIS, 'axes.linewidth': 1.0,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.grid.axis': 'y', 'grid.color': GRID, 'grid.linewidth': 0.8,
    'axes.axisbelow': True,
    'xtick.color': AXIS, 'ytick.color': AXIS, 'xtick.labelcolor': MUTED, 'ytick.labelcolor': MUTED,
    'xtick.direction': 'out', 'ytick.direction': 'out',
    'xtick.major.size': 4, 'ytick.major.size': 4,
    'lines.linewidth': 2.0, 'lines.solid_capstyle': 'round',
}

plt.rcParams.update(rc_dict)


def padded_limits(values, fraction=0.1):
    """Axis limits with padding proportional to the data range, so it works for
    negative values and for a single point (zero range)."""
    lo, hi = float(np.min(values)), float(np.max(values))
    span = hi - lo
    pad = span * fraction if span > 0 else max(abs(hi) * fraction, 1.0)
    return lo - pad, hi + pad


class PlotWidget(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100, labels=("", ""), color=DEFAULT_COLOR):
        self.color = color
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
        locator = mdates.AutoDateLocator()
        self.axes.xaxis.set_major_locator(locator)
        self.axes.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        self.no_data_text = self.axes.text(0.5, 0.5, "No data in selected range",
                                           transform=self.axes.transAxes, color=MUTED,
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
        empty = len(x) == 0
        # With no data, matplotlib would show placeholder ticks (1970 dates, ±0.04), so hide them.
        self.no_data_text.set_visible(empty)
        self.axes.tick_params(labelbottom=not empty, labelleft=not empty,
                              bottom=not empty, left=not empty)
        self.axes.yaxis.grid(not empty)
        self.scatter_plot = self.axes.scatter(x, y, s=36, color=self.color, alpha=0.9,
                                              edgecolors=SURFACE, linewidths=1, zorder=3)

        if np.isnan(m):  # fewer than 2 points, so no fit
            self.line_of_best_fit = self.axes.plot([], [])[0]
        else:
            self.line_of_best_fit = self.axes.plot(x, m * plotting_deltas + b, color=self.color,
                                                   linestyle=(0, (4, 3)), alpha=0.8, zorder=2)[0]

        if len(x) > 0:
            self.axes.set_xlim(np.min(x) - datetime.timedelta(days=3), np.max(x)+datetime.timedelta(days=3))
            self.axes.set_ylim(*padded_limits(y))
        self.draw()


