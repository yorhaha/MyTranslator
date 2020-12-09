from PyQt5.QtWidgets import QFrame, QDesktopWidget, QApplication
from base64 import b64encode, b64decode

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

def isChinese(text):
    for ch in text:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def encrypt(text):
    if text == '':
        return ''
    text = text[::-1]
    text = text[0::2] + text[1::2]
    text = text * 3
    text = b64encode(text.encode()).decode()
    return text

def decrypt(text):
    if text == '':
        return ''
    text = b64decode(text.encode()).decode()
    text = text[0:(len(text) // 3)]
    if len(text) % 2 == 1:
        text += ' '
    halfLength = len(text) // 2
    text1 = text[:halfLength]
    text2 = text[halfLength:]
    text = ''
    for (i, j) in zip(text1, text2):
        text = text + i + j
    if text[-1] == ' ':
        text = text[:-1]
    text = text[::-1]
    return text
