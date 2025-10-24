from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStyledItemDelegate, QHBoxLayout, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import pyqtSignal, QSize
from serial.tools import list_ports
from . import styles


class ItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(35)
        return size


class SerialSelector(QWidget):
    connect_requested = pyqtSignal(str)
    disconnect_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.port_selector = QComboBox()
        self.refresh_ports()
        self.port_selector.setItemDelegate(ItemDelegate())
        self.port_selector.setStyleSheet(styles.COMBOBOX_PORT_SELECTOR)

        self.btn_connect = QPushButton("Connect")
        self.btn_connect.setStyleSheet(styles.BUTTON_CONNECT_SERIAL)
        self.btn_connect.clicked.connect(self._on_connect)

        self.btn_disconnect = QPushButton("Disconnect")
        self.btn_disconnect.setStyleSheet(styles.BUTTON_CONNECT_SERIAL)
        self.btn_disconnect.clicked.connect(lambda: self.disconnect_requested.emit())
        self.btn_disconnect.setEnabled(False)

        selector_row = QHBoxLayout()
        selector_row.addWidget(self.port_selector)

        buttons_row = QHBoxLayout()
        buttons_row.addWidget(self.btn_connect)
        buttons_row.addWidget(self.btn_disconnect)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(selector_row)
        main_layout.addSpacing(30)
        main_layout.addLayout(buttons_row)
        main_layout.setContentsMargins(0, 0, 0, 0)

    def refresh_ports(self):
        self.port_selector.clear()
        ports = [p.device for p in list_ports.comports()]
        if not ports:
            ports = ["COM1", "COM2", "COM3", "COM4"]
        self.port_selector.addItems(ports)

    def _on_connect(self):
        port = self.port_selector.currentText().strip()
        if not port:
            QMessageBox.warning(self, "No Port Selected", "Please select a valid serial port.")
            return
        self.connect_requested.emit(port)

    def set_connected(self, connected: bool):
        self.btn_connect.setEnabled(not connected)
        self.btn_disconnect.setEnabled(connected)
