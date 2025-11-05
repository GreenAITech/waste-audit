from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from . import styles

class AlertDialog(QDialog):
    item_removed = pyqtSignal()
    pause_requested = pyqtSignal()
    resume_requested = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Unrecognizable Item Alert")
        self.setModal(True)
        self.setFixedSize(600, 350)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)


        title_layout = QVBoxLayout()

        title_label = QLabel("Unrecognizable Item Detected!")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(styles.ALERT_LABEL_TITLE)

        title_layout.addWidget(title_label)

        message_label = QLabel(
            "\n"
            "An unrecognizable item has been detected in the bin.\n\n"
            "Please remove the item from the bin and\n\n"
            "click 'Confirmed' to continue."
        )
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet(styles.LABEL_HISTORY)

        button_layout = QHBoxLayout()

        self.confirm_button = QPushButton("Confirmed")
        self.confirm_button.setStyleSheet(styles.BUTTON_CONNECT_SERIAL)
        self.confirm_button.clicked.connect(self._on_confirmed_clicked)

        button_layout.addStretch()
        button_layout.addWidget(self.confirm_button)
        button_layout.addStretch()
        
        main_layout.addLayout(title_layout)
        main_layout.addWidget(message_label)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)    
    
    def _on_confirmed_clicked(self):
        self.item_removed.emit()
        self.resume_requested.emit()
        self.accept()

    def show_alert(self):
        print("Showing unrecognizable item alert dialog")
        self.pause_requested.emit()
        self.exec_()

    def closeEvent(self, event):
        print("Alert dialog closed - resuming recognition")
        self.resume_requested.emit()
        super().closeEvent(event)