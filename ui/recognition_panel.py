from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStyledItemDelegate, QHBoxLayout, QLabel, QPushButton, QComboBox, QScrollArea
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from datetime import datetime
from . import styles
from .history_dialog import HistoryDialog

class ItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(50)
        return size


class RecognitionPanel(QWidget):
    category_selected = pyqtSignal(str)
    start_clicked = pyqtSignal()
    done_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    resume_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()
    round_info_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_round = 1
        self.is_running = False
        self.is_paused = False
        self.round_history = []
        self._reset_current_round_data()
        self._setup_ui()

    def _setup_ui(self):
        title_label = QLabel("Recognition Panel")
        title_label.setStyleSheet(styles.LABEL_STATUS)

        select_section = self._create_selection_section()
        control_section = self._create_control_section()
        history_section = self._create_history_section()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(10)
        main_layout.addLayout(select_section)  
        main_layout.addSpacing(20)
        main_layout.addLayout(control_section)  
        main_layout.addSpacing(10)
        main_layout.addLayout(history_section)  

    def _create_selection_section(self):

        layout = QHBoxLayout()

        self.round_label = QLabel(f"Round {self.current_round}")
        self.round_label.setAlignment(Qt.AlignCenter)
        self.round_label.setStyleSheet(styles.ROUND_LABEL)
        self.round_label.setFixedHeight(50) 

        self.category_selector = QComboBox()
        self.category_selector.addItems([])
        self.category_selector.setItemDelegate(ItemDelegate())
        self.category_selector.setStyleSheet(styles.COMBOBOX_PORT_SELECTOR)
        self.category_selector.currentTextChanged.connect(self.category_selected.emit)
        self.category_selector.setFixedHeight(50)
        
        layout.addWidget(self.round_label)
        layout.addWidget(self.category_selector)

        return layout
    
    def _create_control_section(self):

        layout = QVBoxLayout()
        
        main_buttons_layout = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(styles.BUTTON_CONNECT_SERIAL)
        self.start_button.setFixedHeight(50)
        self.start_button.clicked.connect(self._on_start_clicked)

        self.done_button = QPushButton("Done")
        self.done_button.setStyleSheet(styles.BUTTON_CONNECT_SERIAL)
        self.done_button.setFixedHeight(50)
        self.done_button.clicked.connect(self._on_done_clicked)
        self.done_button.setEnabled(False)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet(styles.BUTTON_ZERO_TARE)
        self.reset_button.setFixedHeight(50)
        self.reset_button.clicked.connect(self._on_reset_clicked)

        main_buttons_layout.addWidget(self.start_button)
        main_buttons_layout.addWidget(self.done_button)
        main_buttons_layout.addWidget(self.reset_button)

        pause_resume_layout = QHBoxLayout()

        self.pause_button = QPushButton("Pause")
        self.pause_button.setStyleSheet(styles.BUTTON_CONNECT_SERIAL)
        self.pause_button.setFixedHeight(50)
        self.pause_button.clicked.connect(self._on_pause_clicked)
        self.pause_button.setEnabled(False)

        self.resume_button = QPushButton("Resume")
        self.resume_button.setStyleSheet(styles.BUTTON_CONNECT_SERIAL)
        self.resume_button.setFixedHeight(50)
        self.resume_button.clicked.connect(self._on_resume_clicked)
        self.resume_button.setEnabled(False)

        pause_resume_layout.addWidget(self.pause_button)
        pause_resume_layout.addWidget(self.resume_button)

        self.count_label_text = QLabel("Items Recognized")
        self.count_label_text.setAlignment(Qt.AlignCenter)
        self.count_label_text.setStyleSheet("font-size: 16px; color: #666; font-family: 'Arial'; font-weight: bold;")

        self.count_label = QLabel("0")
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet("font-size: 40px; font-weight: bold; color: #2C3E50; font-family: 'Arial';")
        
        layout.addLayout(main_buttons_layout)
        layout.addSpacing(20)
        layout.addLayout(pause_resume_layout)
        layout.addSpacing(20)
        layout.addWidget(self.count_label_text)
        layout.addWidget(self.count_label)

        return layout
    
    def _create_history_section(self):
        layout = QVBoxLayout()
        
        history_label = QLabel("Round History:")
        history_label.setStyleSheet(styles.LABEL_STATUS)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(100)
        
        self.history_widget = QWidget()
        self.history_layout = QHBoxLayout(self.history_widget)
        self.history_layout.setAlignment(Qt.AlignLeft)
        
        scroll_area.setWidget(self.history_widget)
        
        layout.addWidget(history_label)
        layout.addWidget(scroll_area)
        
        return layout
    
    def _on_start_clicked(self):
        self.is_running = True
        self.current_round_data['start_time'] = datetime.now()
        self.start_button.setEnabled(False)
        self.done_button.setEnabled(True)
        self.pause_button.setEnabled(True)
        self.category_selected.emit(self.category_selector.currentText())
        self.start_clicked.emit()

    def _on_done_clicked(self):
        self.is_running = False
        self.is_paused = False

        self.current_round_data['end_time'] = datetime.now()
        self.current_round += 1
        self.round_label.setText(f"Round {self.current_round}")

        self.start_button.setEnabled(True)
        self.done_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)

        self.done_clicked.emit()
        QTimer.singleShot(100, self._process_history_after_done)

    def _process_history_after_done(self):
        round_info = {
            'round': self.current_round - 1,
            'category': self.category_selector.currentText(),
            'total_amount': self.current_round_data['total_amount'],
            'total_weight': self.current_round_data['total_weight'],
            'start_time': self.current_round_data['start_time'],
            'end_time': self.current_round_data['end_time']
        }
        self.round_history.append(round_info)
        self._update_history_display(round_info)
        self._reset_current_round_data()

    def _reset_current_round_data(self):
        self.current_round_data = {
            'total_amount': 0,
            'total_weight': 0.0,
            'start_time': None,
            'end_time': None
        }

    def _on_reset_clicked(self):
        self.current_round = 1
        self.round_label.setText(f"Round {self.current_round}")
        self.round_history.clear()

        for i in reversed(range(self.history_layout.count())):
            child = self.history_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        self.is_running = False
        self.is_paused = False
        self.start_button.setEnabled(True)
        self.done_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)
        self.count_label.setText("0")
        
        self.reset_clicked.emit()
        
    def _on_pause_clicked(self):
        self.is_paused = True
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(True)
        self.pause_clicked.emit()

    def _on_resume_clicked(self):
        self.is_paused = False
        self.pause_button.setEnabled(True)
        self.resume_button.setEnabled(False)
        self.resume_clicked.emit()

    def _update_history_display(self, round_info):
        button = QPushButton(f"R{round_info['round']}: {round_info['category']}")
        button.setStyleSheet(styles.BUTTON_HISTORY)
        button.clicked.connect(lambda: self._show_round_info(round_info))
        self.history_layout.addWidget(button)

    def _show_round_info(self, round_info):
        dialog = HistoryDialog(round_info, self)
        dialog.exec_()

    def update_current_round_data(self, amount=None, weight=None):
        if amount is not None:
            self.current_round_data['total_amount'] = amount
        if weight is not None:
            self.current_round_data['total_weight'] = weight

    def get_current_round_data(self):
        return self.current_round_data.copy()
    
    def get_current_round(self):
        return self.current_round

    def get_selected_category(self):
        return self.category_selector.currentText()

    def is_recognition_running(self):
        return self.is_running and not self.is_paused

    def update_count(self, count: int):
        self.count_label.setText(str(count))

    def update_category_options(self, categories: list):
        self.category_selector.clear()
        self.category_selector.addItems(categories)