from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal,QTimer
from PyQt5.QtGui import QImage, QPixmap
from . import styles

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("Warning: OpenCV not installed. Camera will not work.")

class CameraPanel(QWidget):
    camera_connected = pyqtSignal()
    camera_disconnected = pyqtSignal()
    frame_captured = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.camera_frame = QFrame()
        self.camera_frame.setFrameShape(QFrame.StyledPanel)
        self.camera_frame.setStyleSheet(styles.FRAME_CAMERA)
        self.camera_frame.setMinimumSize(960, 540)
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
        if not OPENCV_AVAILABLE:
            self.camera_label.setText("Error: OpenCV not installed\nRun: pip install opencv-python")
            return

        try:
            self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            if not self.camera.isOpened():
                self.camera_label.setText("Failed to open camera\nCheck if camera is connected")
                self.camera = None
                return

            self.timer = QTimer(self)
            self.timer.timeout.connect(self._update_frame)
            self.timer.start(33)

            self.btn_connect.setEnabled(False)
            self.btn_disconnect.setEnabled(True)
            self.camera_label.setText("Initializing camera...")
            self.camera_connected.emit()

            print("Camera connected successfully")

        except Exception as e:
            self.camera_label.setText(f"Camera error:\n{str(e)}")
            print(f"Camera connection error: {e}")
            if self.camera:
                self.camera.release()
                self.camera = None

    def _on_disconnect(self):
        if self.timer:
            self.timer.stop()
            self.timer = None
        if self.camera:
            self.camera.release()
            self.camera = None

        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)
        self.camera_label.setText("Camera disconnected")
        self.camera_disconnected.emit()
        print("Camera disconnected")

    def _update_frame(self):
        if not self.camera or not self.camera.isOpened():
            return

        try:
            ret, frame = self.camera.read()
            if not ret or frame is None:
                self.camera_label.setText("Failed to read frame")
                return

            self.frame_captured.emit(frame.copy())
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width = frame_rgb.shape[:2]
            qt_image = QImage(
                frame_rgb,
                width,
                height,
                QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(
                self.camera_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.camera_label.setPixmap(scaled_pixmap)

        except Exception as e:
            print(f"Frame update error: {e}")
            self.camera_label.setText(f"Display error:\n{str(e)}")

