from test2 import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = MainWindow()
    run.show()
    sys.exit(app.exec_())
