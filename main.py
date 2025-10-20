import sys
from PyQt5.QtWidgets import QApplication
from ui.ui_refactor import WeightUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WeightUI()
    w.show()
    sys.exit(app.exec_())