from PySide.QtGui import *
from PySide.QtCore import *
import sys

class Form(QDialog):
    def __init__(self):
        super().__init__()

        self.textbox = QTextEdit()
        self.create = QPushButton("Create")
        self.openbutton = QPushButton("Open")
        self.savebutton = QPushButton("Save")
        self.closebutton = QPushButton("Close")


        layout = QVBoxLayout()
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout1.addWidget(self.textbox)
        layout2.addWidget(self.create)
        layout2.addWidget(self.openbutton)
        layout2.addWidget(self.savebutton)
        layout2.addWidget(self.closebutton)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        self.textbox.clearFocus()
        self.setLayout(layout)
        self.setWindowTitle("Text Editor")

        self.create.clicked.connect(self.focus)
        self.openbutton.clicked.connect(self.openfun)
        self.closebutton.clicked.connect(self.closefun)
        self.savebutton.clicked.connect(self.savefun)
        self.textbox.setDisabled(True)
        self.textbox.setStyleSheet("QTextEdit { background-color: rgb(196, 196, 196) }")

    def openfun(self):
        file = QFileDialog.getOpenFileName(self, 'Select File', dir = '/', filter = 'Text files(*.txt)')
        if file[0]:
            fp = open(file[0], 'r')
            str = fp.read()
            self.textbox.setText(str)
            fp.close()

    def savefun(self):
        file = QFileDialog.getSaveFileName(self, 'Select File', dir = '/', filter = 'Text files(*.txt)')

    def closefun(self):
        self.close()

    def focus(self):
        self.textbox.setDisabled(False)
        self.textbox.setStyleSheet("QTextEdit { background-color: rgb(255, 255, 255) }")
        self.str = self.textbox.toPlainText()
        pass

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
