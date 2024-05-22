from View.UI_V5 import MyMainWindow
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
window = MyMainWindow()
window.move(180, 30)
window.show()

sys.exit(app.exec_())
