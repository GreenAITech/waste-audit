from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QFrame, QSizePolicy, QMessageBox, QStyledItemDelegate
)
from PyQt5.QtCore import Qt, QTimer
from serial.tools import list_ports

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from signals import WeightSignal
from serial_reader import SerialReader
import ui.styles as styles


class WeightUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GOLIS Serial Weight Reader")
        # Left camera placeholder
        self.camera_frame = QFrame()
        self.camera_frame.setFrameShape(QFrame.StyledPanel)
        self.camera_frame.setStyleSheet(styles.FRAME_CAMERA)
        self.camera_frame.setMinimumSize(600, 640)
        self.camera_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.camera_label = QLabel("Camera Preview (reserved)")
        self.camera_label.setStyleSheet(styles.LABEL_CAMERA)
        self.camera_label.setAlignment(Qt.AlignCenter)

        cam_frame_layout = QVBoxLayout(self.camera_frame)
        cam_frame_layout.addWidget(self.camera_label)

        # Connect Camera Button
        self.btn_connect_camera = QPushButton("Connect Camera")
        self.btn_connect_camera.setStyleSheet(styles.BUTTON_CONNECT_CAMERA)
        self.btn_connect_camera.clicked.connect(self.connect_camera)

        # Disconnect Camera Button
        self.btn_disconnect_camera = QPushButton("Disconnect Camera")
        self.btn_disconnect_camera.setStyleSheet(styles.BUTTON_DISCONNECT_CAMERA)
        self.btn_disconnect_camera.clicked.connect(self.disconnect_camera)
        self.btn_disconnect_camera.setEnabled(False)

        camera_buttons_row = QHBoxLayout()
        camera_buttons_row.addWidget(self.btn_connect_camera)
        camera_buttons_row.addWidget(self.btn_disconnect_camera)

        # Left panel layout
        left_panel = QVBoxLayout()
        left_panel.addWidget(self.camera_frame)
        left_panel.addLayout(camera_buttons_row)

        # Right top row

        # Port selector
        self.port_selector = QComboBox()
        self.refresh_ports()

        class ItemDelegate(QStyledItemDelegate):
            def sizeHint(self, option, index):
                size = super().sizeHint(option, index)
                size.setHeight(35)
                return size

        self.port_selector.setItemDelegate(ItemDelegate())
        self.port_selector.setStyleSheet(styles.COMBOBOX_PORT_SELECTOR)

        self.btn_connect = QPushButton("Connect")
        self.btn_connect.setStyleSheet(styles.BUTTON_CONNECT_SERIAL)
        self.btn_disconnect = QPushButton("Disconnect")
        self.btn_disconnect.setStyleSheet(styles.BUTTON_DISCONNECT_SERIAL)
        self.btn_disconnect.setEnabled(False)

        top_section = QVBoxLayout()

        selector_row = QHBoxLayout()
        selector_row.addWidget(self.port_selector)
        top_section.addLayout(selector_row)

        top_section.addSpacing(20)

        buttons_row = QHBoxLayout()
        buttons_row.addWidget(self.btn_connect)
        buttons_row.addWidget(self.btn_disconnect)
        top_section.addLayout(buttons_row)

        # Value labels
        self.label_net = QLabel("Net Weight: -- kg")
        self.label_gross = QLabel("Gross Weight: -- kg")
        self.label_tare = QLabel("Tare Weight: -- kg")
        self.label_flags = QLabel("Flags: --")
        for lab in (self.label_net, self.label_gross, self.label_tare, self.label_flags):
            lab.setAlignment(Qt.AlignLeft)
            lab.setStyleSheet(styles.LABEL_WEIGHT)

        # Zero/Tare buttons
        self.btn_zero = QPushButton("置零 (Z)")
        self.btn_zero.setStyleSheet(styles.BUTTON_ZERO_TARE)
        self.btn_tare = QPushButton("去皮 (T)")
        self.btn_tare.setStyleSheet(styles.BUTTON_ZERO_TARE)
        self.btn_zero.setEnabled(False)
        self.btn_tare.setEnabled(False)
        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn_zero)
        btn_row.addWidget(self.btn_tare)

        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(styles.LABEL_STATUS)

        # Right panel layout
        right_panel = QVBoxLayout()
        right_panel.addSpacing(10)
        right_panel.addLayout(top_section)
        right_panel.addSpacing(20)
        right_panel.addWidget(self.label_net)
        right_panel.addWidget(self.label_gross)
        right_panel.addWidget(self.label_tare)
        right_panel.addWidget(self.label_flags)
        right_panel.addSpacing(20)
        right_panel.addLayout(btn_row)
        right_panel.addStretch(1)
        right_panel.addWidget(self.status_label)

        # Main layout
        root = QHBoxLayout(self)
        root.addLayout(left_panel, stretch=3)
        right_container = QFrame()
        right_container.setLayout(right_panel)
        right_container.setMinimumWidth(360)
        root.addWidget(right_container, stretch=2)
        self.setLayout(root)
        self.resize(1080, 640)

        # Signals / reader
        self.signal = WeightSignal()
        self.signal.data_received.connect(self._on_data)
        self.signal.status.connect(self._on_status)
        self.reader = None

        # Wiring
        self.btn_connect.clicked.connect(self.connect_to_serial)
        self.btn_disconnect.clicked.connect(self.disconnect_serial)
        self.btn_zero.clicked.connect(lambda: self._enqueue_cmd('Z'))
        self.btn_tare.clicked.connect(lambda: self._enqueue_cmd('T'))

        # 1 Hz UI refresh
        self._last_data = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_labels_once_per_second)
        self._timer.start(1000)

    # ---- ports ----
    def refresh_ports(self):
        self.port_selector.clear()
        ports = [p.device for p in list_ports.comports()]
        if not ports:
            ports = ["COM1", "COM2", "COM3", "COM4"]
        self.port_selector.addItems(ports)

    # ---- serial controls ----
    def connect_to_serial(self):
        port = self.port_selector.currentText().strip()
        if not port:
            QMessageBox.warning(self, "Port", "No serial port selected.")
        if self.reader:
            self.disconnect_serial()

        self.reader = SerialReader(port=port, baudrate=9600, signal=self.signal)
        self.reader.start()

        self.btn_connect.setEnabled(False)
        self.btn_disconnect.setEnabled(True)
        self.btn_zero.setEnabled(True)
        self.btn_tare.setEnabled(True)
        self.status_label.setText(f"Connecting {port}...")

    def disconnect_serial(self):
        if self.reader:
            self.reader.stop()
            self.reader.join(timeout=1.5)
            self.reader = None
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)
        self.btn_zero.setEnabled(False)
        self.btn_tare.setEnabled(False)
        self.status_label.setText("Disconnected")

    def _enqueue_cmd(self, cmd: str):
        if self.reader:
            self.reader.enqueue_command(cmd)
        else:
            QMessageBox.information(self, "Info", "Not connected.")

    # ---- camera (placeholder) ----
    def connect_camera(self):

        self.btn_connect_camera.setEnabled(False)
        self.btn_disconnect_camera.setEnabled(True)
        self.camera_label.setText("Camera connected")

    def disconnect_camera(self):

        self.btn_connect_camera.setEnabled(True)
        self.btn_disconnect_camera.setEnabled(False)
        self.camera_label.setText("Camera disconnected")

    # ---- UI update ----
    def _on_data(self, data: dict):
        self._last_data = data

    def _refresh_labels_once_per_second(self):
        d = self._last_data
        if not d:
            return
        self.label_net.setText(f"Net Weight: {d['NetWeight']:.3f} kg")
        self.label_gross.setText(f"Gross Weight: {d['RoughWeight']:.3f} kg")
        self.label_tare.setText(f"Tare Weight: {d['TareWeight']:.3f} kg")
        flags = f"Zero: {d['ZeroFlag']}, Stable: {d['StableFlag']}, Tare: {d['TareFlag']}, Overload: {d['Overload']}"
        self.label_flags.setText(f"Flags: {flags}")

    def _on_status(self, msg: str):
        self.status_label.setText(msg)

    def closeEvent(self, event):
        self.disconnect_serial()
        event.accept()
