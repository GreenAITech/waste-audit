from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from .serial_selector import SerialSelector
from .counter_display import CounterDisplay
from .weight_display import WeightDisplay
from .control_buttons import ControlButtons
from . import styles


class RightPanel(QWidget):
    serial_connect_requested = pyqtSignal(str)
    serial_disconnect_requested = pyqtSignal()
    command_requested = pyqtSignal(str)
    category_changed = pyqtSignal(str)
    reset_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.serial_selector = SerialSelector()
        self.counter_display = CounterDisplay()
        self.weight_display = WeightDisplay()
        self.control_buttons = ControlButtons()

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(styles.LABEL_STATUS)

        # Layout setup
        main_layout = QVBoxLayout(self)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.serial_selector)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.counter_display)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.weight_display)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.control_buttons)
        main_layout.addStretch(1)
        main_layout.addWidget(self.status_label)

    def _connect_signals(self):
        self.serial_selector.connect_requested.connect(self.serial_connect_requested.emit)
        self.serial_selector.disconnect_requested.connect(self.serial_disconnect_requested.emit)
        self.control_buttons.zero_clicked.connect(lambda: self.command_requested.emit('Z'))
        self.control_buttons.tare_clicked.connect(lambda: self.command_requested.emit('T'))
        self.counter_display.category_changed.connect(self.category_changed.emit)
        self.counter_display.reset_clicked.connect(self.reset_clicked.emit)

    def set_serial_connected(self, connected: bool):
        self.serial_selector.set_connected(connected)
        self.control_buttons.set_enabled(connected)

    def update_weight_data(self, data: dict):
        self.weight_display.update_data(data)

    def update_status(self, msg: str):
        self.status_label.setText(msg)

    def update_count(self, count: int):
        self.counter_display.set_count(count)