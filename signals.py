from PyQt5.QtCore import pyqtSignal, QObject

# ---------- signals ----------

class WeightSignal(QObject):
    data_received = pyqtSignal(dict)
    status = pyqtSignal(str)

