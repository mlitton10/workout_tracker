from PyQt6.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)

