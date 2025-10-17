from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame, QMessageBox
from PyQt5.QtCore import QTimer

from signals import WeightSignal
from serial_reader import SerialReader
from .camera_panel import CameraPanel
from .right_panel import RightPanel


class WeightUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GOLIS Serial Weight Reader")
        self._init_components()
        self._setup_layout()
        self._init_serial()
        self._connect_signals()
        self._setup_timer()
        self.resize(1080, 640)

    def _init_components(self):
        self.camera_panel = CameraPanel()
        self.right_panel = RightPanel()

    def _setup_layout(self):
        right_container = QFrame()
        right_container.setLayout(self.right_panel.layout())
        right_container.setMinimumWidth(360)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.camera_panel, stretch=3)
        main_layout.addWidget(right_container, stretch=2)

    def _init_serial(self):
        self.signal = WeightSignal()
        self.reader = None

    def _connect_signals(self):
        self.signal.data_received.connect(self._on_data)
        self.signal.status.connect(self.right_panel.update_status)

        self.right_panel.serial_connect_requested.connect(self._connect_serial)
        self.right_panel.serial_disconnect_requested.connect(self._disconnect_serial)
        self.right_panel.command_requested.connect(self._enqueue_cmd)
        self.right_panel.category_changed.connect(self._on_category_changed)

        self.camera_panel.camera_connected.connect(lambda: print("Camera connected"))
        self.camera_panel.camera_disconnected.connect(lambda: print("Camera disconnected"))

    def _setup_timer(self):
        self._last_data = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_ui)
        self._timer.start(1000)

    def _connect_serial(self, port: str):
        if self.reader:
            self._disconnect_serial()

        self.reader = SerialReader(port=port, baudrate=9600, signal=self.signal)
        self.reader.start()

        self.right_panel.set_serial_connected(True)
        self.right_panel.update_status(f"Connecting {port}...")

    def _disconnect_serial(self):
        if self.reader:
            self.reader.stop()
            self.reader.join(timeout=1.5)
            self.reader = None

        self.right_panel.set_serial_connected(False)
        self.right_panel.update_status("Disconnected")

    def _enqueue_cmd(self, cmd: str):
        if self.reader:
            self.reader.enqueue_command(cmd)
        else:
            QMessageBox.information(self, "Info", "Not connected.")

    def _on_data(self, data: dict):

        self._last_data = data

    def _refresh_ui(self):
        if self._last_data:
            self.right_panel.update_weight_data(self._last_data)

    def _on_category_changed(self, category: str):
        print(f"Category changed to: {category}")

        # TODO:

    def closeEvent(self, event):

        self._disconnect_serial()
        event.accept()