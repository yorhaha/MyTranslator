from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QFrame, QDesktopWidget, QApplication

def getVLine():
    devideLine = QFrame()
    devideLine.setFrameShape(QFrame.VLine)
    devideLine.setMaximumWidth(1)
    return devideLine

def getHLine():
    devideLine = QFrame()
    devideLine.setFrameShape(QFrame.HLine)
    devideLine.setMaximumHeight(1)
    return devideLine

def moveCenter(window):
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())

def deleteExtraSpace(srcText):
    result = ''
    srcList = srcText.strip().split('\n')
    srcList = [e.strip() for e in srcList if len(e.strip()) > 0]
    for e in srcList:
        result += e
        result += '\n'
    result = result[:-1]
    return result

def copyText(text):
    QApplication.clipboard().setText(text)