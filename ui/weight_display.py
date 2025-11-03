from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from . import styles


class WeightDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        title_label = QLabel("Weight Display")
        title_label.setStyleSheet(styles.LABEL_STATUS)

        self.label_net = QLabel("Net Weight: -- kg")
        self.label_gross = QLabel("Gross Weight: -- kg")
        self.label_tare = QLabel("Tare Weight: -- kg")
        self.label_flags = QLabel("Flags: --")
        for lab in (self.label_net, self.label_gross, self.label_tare, self.label_flags):
            lab.setAlignment(Qt.AlignLeft)
            lab.setStyleSheet(styles.LABEL_WEIGHT)

        label_layout = QVBoxLayout()
        label_layout.addWidget(title_label)
        label_layout.addSpacing(10)
        label_layout.addWidget(self.label_net)
        label_layout.addSpacing(5)
        label_layout.addWidget(self.label_gross)
        label_layout.addSpacing(5)
        label_layout.addWidget(self.label_tare)
        label_layout.addSpacing(5)
        label_layout.addWidget(self.label_flags)

        self.setLayout(label_layout)

    def update_data(self, data: dict):
        self.label_net.setText(f"Net Weight: {data['NetWeight']:.3f} kg")
        self.label_gross.setText(f"Gross Weight: {data['RoughWeight']:.3f} kg")
        self.label_tare.setText(f"Tare Weight: {data['TareWeight']:.3f} kg")

        flags = (f"Zero: {data['ZeroFlag']}, Stable: {data['StableFlag']}, "
                 f"Tare: {data['TareFlag']}, Overload: {data['Overload']}")
        self.label_flags.setText(f"Flags: {flags}")