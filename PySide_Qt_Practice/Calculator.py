from PySide.QtCore import *
from PySide.QtGui import *
import sys

class Form(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.browser = QTextBrowser()
        self.linedit = QLineEdit("Type Here and Press Enter")
        self.linedit.selectAll()

        widget = QVBoxLayout()
        widget.addWidget(self.browser)
        widget.addWidget(self.linedit)
        self.setLayout(widget)
        self.setWindowTitle('Calculator')
        self.linedit.setFocus()

        self.linedit.returnPressed.connect(self.uichange)
        self.linedit.returnPressed.connect(self.linedit.clear)

    def uichange(self):
        try:
            text = self.linedit.text()
            self.browser.append('%s = <b>%s</b>' % (text, eval(text)))
        except:
            self.browser.append('Enter valid expression')

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()