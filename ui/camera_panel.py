from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal,QTimer
from PyQt5.QtGui import QImage, QPixmap
from . import styles
import os

class CameraPanel(QWidget):
    camera_connected = pyqtSignal()
    camera_disconnected = pyqtSignal()
    frame_captured = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._connected = False
        self._current_image_path = None
        self._is_warning_state = False
        self._init_ui()

    def _init_ui(self):
        self._setup_alert_button()

        self.camera_frame = QFrame()
        self.camera_frame.setFrameShape(QFrame.StyledPanel)
        self.camera_frame.setStyleSheet(styles.FRAME_CAMERA)
        self.camera_frame.setMinimumSize(720, 520)
        self.camera_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.camera_label = QLabel("Camera Preview (reserved)")
        self.camera_label.setStyleSheet(styles.LABEL_CAMERA)
        self.camera_label.setAlignment(Qt.AlignCenter)

        cam_frame_layout = QVBoxLayout(self.camera_frame)
        cam_frame_layout.addWidget(self.camera_label)

        self._setup_buttons()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.alert_button)
        main_layout.addWidget(self.camera_frame)
        main_layout.addLayout(self.buttons_layout)

    def _setup_alert_button(self):
        self.alert_button = QPushButton("Please put waste items one by one into the bin.")
        self.alert_button.setStyleSheet(styles.NORMAL_BUTTON)
        self.alert_button.clicked.connect(self._on_alert_button_clicked)
        self.alert_button.setMinimumHeight(60)
        self._is_warning_state = False



    def _setup_buttons(self):
        self.btn_connect = QPushButton("Enable Image Display")
        self.btn_connect.setStyleSheet(styles.BUTTON_CONNECT_CAMERA)
        self.btn_connect.clicked.connect(self._on_connect)

        self.btn_disconnect = QPushButton("Disable Image Display")
        self.btn_disconnect.setStyleSheet(styles.BUTTON_CONNECT_CAMERA)
        self.btn_disconnect.clicked.connect(self._on_disconnect)
        self.btn_disconnect.setEnabled(False)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.btn_connect)
        self.buttons_layout.addWidget(self.btn_disconnect)

    def _on_connect(self):
        self._connected = True
        self.btn_connect.setEnabled(False)
        self.btn_disconnect.setEnabled(True)
        self.camera_label.setText("Waiting...")
        self.camera_connected.emit()
        print("Image display")


    def _on_alert_button_clicked(self):
        if self._is_warning_state:
            print("Alert acknowledged by user")
            self.set_alert_normal() 

    def _on_disconnect(self):
        self._connected = False
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)
        self.camera_label.setText("Disconnected")
        self.camera_disconnected.emit()
        print("Image disconnected")

    def display_image_from_path(self, image_path:str):
        if not self._connected:
            print("Image display disabled")
            return
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return
        try:
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                self.camera_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.camera_label.setPixmap(scaled_pixmap)
            self._current_image_path = image_path
        except Exception as e:
            print(f"Error displaying image {image_path}: {e}")
            self.camera_label.setText(f"Display error:\n{str(e)}")


    def set_alert_normal(self):
        self.alert_button.setText("Please put waste items one by one into the bin.")
        self.alert_button.setStyleSheet(styles.NORMAL_BUTTON)
        self._is_warning_state = False

    def set_alert_warning(self):
        self.alert_button.setText("Warning: Unrecognizable item detected, please take it out!")
        self.alert_button.setStyleSheet(styles.ALERT_BUTTON)
        self._is_warning_state = True