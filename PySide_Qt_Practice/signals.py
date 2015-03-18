import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Zerobox(QSpinBox):
    zero = 0
    def __init__(self):
        super().__init__()

        self.valueChanged.connect(self.iszero)

    def iszero(self):
        if self.value() is 0:
            self.zero += 1
            self.emit(SIGNAL('zero(int)'), self.zero)

class Form(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.dial = QDial()
        self.dial.setNotchesVisible(True)

        self.spinbox = Zerobox()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.spinbox)
        self.layout.addWidget(self.dial)

        self.dial.valueChanged.connect(self.spinbox.setValue)
        self.spinbox.valueChanged.connect(self.dial.setValue)
        self.connect(self.spinbox, SIGNAL('zero(int)'), self.announce)

        self.setLayout(self.layout)
        self.setWindowTitle("signal")

    def announce(self, num):
        print('occurence of zero is ' + str(num) + ' times')

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()