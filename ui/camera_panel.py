from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from . import styles


class CameraPanel(QWidget):
    camera_connected = pyqtSignal()
    camera_disconnected = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
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

        self._setup_buttons()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.camera_frame)
        main_layout.addLayout(self.buttons_layout)

    def _setup_buttons(self):
        self.btn_connect = QPushButton("Connect Camera")
        self.btn_connect.setStyleSheet(styles.BUTTON_CONNECT_CAMERA)
        self.btn_connect.clicked.connect(self._on_connect)

        self.btn_disconnect = QPushButton("Disconnect Camera")
        self.btn_disconnect.setStyleSheet(styles.BUTTON_DISCONNECT_CAMERA)
        self.btn_disconnect.clicked.connect(self._on_disconnect)
        self.btn_disconnect.setEnabled(False)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.btn_connect)
        self.buttons_layout.addWidget(self.btn_disconnect)

    def _on_connect(self):
        self.btn_connect.setEnabled(False)
        self.btn_disconnect.setEnabled(True)
        self.camera_label.setText("Camera connected")
        self.camera_connected.emit()

    def _on_disconnect(self):
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)
        self.camera_label.setText("Camera disconnected")
        self.camera_disconnected.emit()