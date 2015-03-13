import sys, time
from PySide.QtCore import *
from PySide.QtGui import *


app = QApplication(sys.argv)
due = QTime.currentTime()
try:
    message = "Alert"
    #print(len(sys.argv))
    if len(sys.argv) < 2:
        raise ValueError
    hour, minute = sys.argv[1].split(':')
    due = QTime(int(hour), int(minute))
    if not due.isValid():
        raise ValueError
    if len(sys.argv) > 2:
        message = ' '.join(sys.argv[2:])
    pass
except ValueError:
    message = 'Usage is Hour:Minute message(optional)'

while QTime.currentTime() < due:
    time.sleep(10)

lable = QLabel('<font color=red size=30><b>' + message + '</b></font>')
lable.setWindowFlags(Qt.SplashScreen)
lable.show()

QTimer.singleShot(20000, app.quit)
app.exec_()