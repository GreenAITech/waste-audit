from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from . import styles

class ControlButtons(QWidget):
    zero_clicked = pyqtSignal()
    tare_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.btn_zero = QPushButton("Zero")
        self.btn_zero.setStyleSheet(styles.BUTTON_ZERO_TARE)
        self.btn_zero.clicked.connect(self.zero_clicked.emit)
        self.btn_zero.setEnabled(False)

        self.btn_tare = QPushButton("Tare")
        self.btn_tare.setStyleSheet(styles.BUTTON_ZERO_TARE)
        self.btn_tare.clicked.connect(self.tare_clicked.emit)
        self.btn_tare.setEnabled(False)

        # Layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.btn_zero)
        main_layout.addWidget(self.btn_tare)

        self.setLayout(main_layout)

    def set_enabled(self, enabled: bool):

        self.btn_zero.setEnabled(enabled)
        self.btn_tare.setEnabled(enabled)