from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QStyledItemDelegate,QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from category_mapping import CategoryMapping
from . import styles


class CategoryDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(35)
        return size


class CounterDisplay(QWidget):
    category_changed = pyqtSignal(str)
    reset_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.category_selector = QComboBox()
        self.category_selector.addItems(CategoryMapping.CATEGORIES)
        self.category_selector.setItemDelegate(CategoryDelegate())
        self.category_selector.setStyleSheet(styles.COMBOBOX_CATEGORY_SELECTOR)
        self.category_selector.currentTextChanged.connect(self.category_changed.emit)

        category_row = QHBoxLayout()
        category_row.addWidget(self.category_selector)

        # Total Label
        self.label_total_text = QLabel("Total")
        self.label_total_text.setAlignment(Qt.AlignCenter)
        self.label_total_text.setStyleSheet("font-size: 16px; color: #666; font-family: 'Arial';font-weight: bold;")

        self.label_total_count = QLabel("10")
        self.label_total_count.setAlignment(Qt.AlignCenter)
        self.label_total_count.setStyleSheet("""
            font-size: 80px; 
            font-weight: bold; 
            color: #2C3E50;
            font-family: 'Arial';
        """)

        self.reset_button = QPushButton("Count Reset")
        self.reset_button.setStyleSheet(styles.RESET_BUTTON)
        self.reset_button.clicked.connect(self.reset_clicked.emit)
        self.reset_button.setEnabled(True)


        # Layout
        count_section = QVBoxLayout()
        count_section.addSpacing(30)
        count_section.addLayout(category_row)
        count_section.addSpacing(10)
        count_section.addWidget(self.label_total_text)
        count_section.addWidget(self.label_total_count)
        count_section.addWidget(self.reset_button)

        self.setLayout(count_section)

    def set_count(self, count: int):
        self.label_total_count.setText(str(count))

    def get_category(self):
        return self.category_selector.currentText()