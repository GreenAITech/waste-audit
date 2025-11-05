from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt
from . import styles

class HistoryDialog(QDialog):
    def __init__(self, round_info, parent=None):
        super().__init__(parent)
        self.round_info = round_info

        print(f"🔍 HistoryDialog received round_info: {round_info}")
        self.setWindowTitle(f"Round {round_info['round']} Information")
        self.setFixedSize(450, 320)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self._setup_ui()
    
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        title_label = QLabel(f"Round {self.round_info['round']} Details")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #2C3E50; 
            font-family: 'Arial';
            padding: 10px;
        """)
         

        category_layout = QHBoxLayout()
        category_label = QLabel("Category:")
        category_label.setStyleSheet(styles.LABEL_HISTORY)
        category_value = QLabel(self.round_info.get('category', 'Unknown'))
        category_value.setStyleSheet(styles.LABEL_HISTORY)
        category_layout.addWidget(category_label)
        category_layout.addStretch()
        category_layout.addWidget(category_value)
        

        amount_layout = QHBoxLayout()
        amount_label = QLabel("Total Amount:")
        amount_label.setStyleSheet(styles.LABEL_HISTORY)
        amount_value = QLabel(str(self.round_info.get('total_amount', 0)))
        amount_value.setStyleSheet(styles.LABEL_HISTORY)
        amount_layout.addWidget(amount_label)
        amount_layout.addStretch()
        amount_layout.addWidget(amount_value)

        weight_layout = QHBoxLayout()
        weight_label = QLabel("Total Weight:")
        weight_label.setStyleSheet(styles.LABEL_HISTORY)
        weight_value = QLabel(f"{self.round_info.get('total_weight', 0.0):.3f} kg")
        weight_value.setStyleSheet(styles.LABEL_HISTORY)
        weight_layout.addWidget(weight_label)
        weight_layout.addStretch()
        weight_layout.addWidget(weight_value)
        
        start_time_layout = QHBoxLayout()
        start_time_label = QLabel("Start Time:")
        start_time_label.setStyleSheet(styles.LABEL_HISTORY)
        
        start_time_value = QLabel("Unknown")
        if (self.round_info.get('start_time') and 
            hasattr(self.round_info['start_time'], 'strftime')):
            start_time_text = self.round_info['start_time'].strftime('%Y-%m-%d %H:%M')
            start_time_value.setText(start_time_text)
        
        start_time_value.setStyleSheet(styles.LABEL_HISTORY)
        start_time_layout.addWidget(start_time_label)
        start_time_layout.addStretch()
        start_time_layout.addWidget(start_time_value)
        

        end_time_layout = QHBoxLayout()
        end_time_label = QLabel("End Time:")
        end_time_label.setStyleSheet(styles.LABEL_HISTORY)
        
        end_time_value = QLabel("Unknown")
        if (self.round_info.get('end_time') and 
            hasattr(self.round_info['end_time'], 'strftime')):
            end_time_text = self.round_info['end_time'].strftime('%Y-%m-%d %H:%M')
            end_time_value.setText(end_time_text)
        
        end_time_value.setStyleSheet(styles.LABEL_HISTORY)
        end_time_layout.addWidget(end_time_label)
        end_time_layout.addStretch()
        end_time_layout.addWidget(end_time_value)

        close_button = QPushButton("Close")
        close_button.setStyleSheet(styles.BUTTON_CONNECT_SERIAL)
        close_button.clicked.connect(self.accept)
        
        
        main_layout.addWidget(title_label)
        main_layout.addLayout(category_layout)
        main_layout.addLayout(amount_layout)
        main_layout.addLayout(weight_layout)
        main_layout.addLayout(start_time_layout)
        main_layout.addLayout(end_time_layout)
        main_layout.addStretch() 
        main_layout.addWidget(close_button)