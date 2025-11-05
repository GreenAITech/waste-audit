from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal,QTimer
from PyQt5.QtGui import QImage, QPixmap
from . import styles
from .alert_dialog import AlertDialog
import os

class CameraPanel(QWidget):
    camera_connected = pyqtSignal()
    camera_disconnected = pyqtSignal()
    alert_pause_requested = pyqtSignal()
    alert_resume_requested = pyqtSignal()


    def __init__(self, parent=None):
        super().__init__(parent)
        self._connected = False
        self._current_image_path = None
        self._init_ui()
        self._init_alert_dialog()

    def _init_ui(self):

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
        main_layout.addWidget(self.camera_frame)
        main_layout.addLayout(self.buttons_layout)

    def _init_alert_dialog(self):
        self.alert_dialog = AlertDialog(self)
        self.alert_dialog.item_removed.connect(self._on_alert_confirmed)
        self.alert_dialog.pause_requested.connect(self._on_alert_pause_requested)   
        self.alert_dialog.resume_requested.connect(self._on_alert_resume_requested) 


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


    def _on_disconnect(self):
        self._connected = False
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)
        self.camera_label.setText("Disconnected")
        self.camera_disconnected.emit()
        print("Image disconnected")

    def _on_alert_confirmed(self):
        print("Alert dialog confirmed by user")

    def _on_alert_pause_requested(self):
        print("Alert dialog requested pause")
        self.alert_pause_requested.emit()
    
    def _on_alert_resume_requested(self):
        print("Alert dialog requested resume")
        self.alert_resume_requested.emit()

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
        pass

    def set_alert_warning(self):
        self.alert_dialog.show_alert()