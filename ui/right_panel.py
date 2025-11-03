from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from .serial_selector import SerialSelector
from .weight_display import WeightDisplay
from .control_buttons import ControlButtons
from .recognition_panel import RecognitionPanel
from . import styles


class RightPanel(QWidget):
    serial_connect_requested = pyqtSignal(str)
    serial_disconnect_requested = pyqtSignal()
    command_requested = pyqtSignal(str)

    category_selected = pyqtSignal(str)
    recognition_started = pyqtSignal(str)      
    recognition_paused = pyqtSignal()          
    recognition_resumed = pyqtSignal()         
    recognition_completed = pyqtSignal(int)    
    round_info_requested = pyqtSignal(int)
    recognition_reset = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.serial_selector = SerialSelector()
        self.weight_display = WeightDisplay()
        self.control_buttons = ControlButtons()
        self.recognition_panel = RecognitionPanel()

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(styles.LABEL_STATUS)

        # Layout setup
        main_layout = QVBoxLayout(self)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.serial_selector)
        main_layout.addSpacing(20)

        main_layout.addWidget(self.weight_display)
        main_layout.addWidget(self.control_buttons)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.recognition_panel)
        main_layout.addSpacing(20)

        main_layout.addStretch(1)
        main_layout.addWidget(self.status_label)

    def _connect_signals(self):
        self.serial_selector.connect_requested.connect(self.serial_connect_requested.emit)
        self.serial_selector.disconnect_requested.connect(self.serial_disconnect_requested.emit)
        self.control_buttons.zero_clicked.connect(lambda: self.command_requested.emit('Z'))
        self.control_buttons.tare_clicked.connect(lambda: self.command_requested.emit('T'))

        self.recognition_panel.category_selected.connect(self.category_selected.emit)
        self.recognition_panel.start_clicked.connect(self._on_recognition_start)
        self.recognition_panel.done_clicked.connect(self._on_recognition_done)
        self.recognition_panel.pause_clicked.connect(self.recognition_paused.emit)
        self.recognition_panel.resume_clicked.connect(self.recognition_resumed.emit)
        self.recognition_panel.round_info_requested.connect(self.round_info_requested.emit)
        self.recognition_panel.reset_clicked.connect(self.recognition_reset.emit)

    def _on_recognition_start(self):
        category = self.recognition_panel.get_selected_category()
        self.recognition_started.emit(category)

    def _on_recognition_done(self):
        round_number = self.recognition_panel.get_current_round() - 1
        self.recognition_completed.emit(round_number)


    def set_serial_connected(self, connected: bool):
        self.serial_selector.set_connected(connected)
        self.control_buttons.set_enabled(connected)

    def update_weight_data(self, data: dict):
        self.weight_display.update_data(data)

    def update_status(self, msg: str):
        self.status_label.setText(msg)

    def get_current_recognition_round(self):
        return self.recognition_panel.get_current_round()
    
    def get_current_category(self):
        return self.recognition_panel.get_selected_category()
    
    def update_count(self, count):
        self.recognition_panel.update_count(count)
