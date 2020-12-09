from PyQt5 import QtCore, QtGui, QtWidgets
from config import *
from netutils import *
from utils import *
from childWindows import HelpWindow, SettingsWindow
from threading import Thread
import sys

class TranslateThread(QtCore.QObject):
    overSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=None, **kwargs)
    
    @QtCore.pyqtSlot(str, str, str)
    def startTrans(self, srcText, lang_from, lang_to):
        if DEBUG_FLAG:
            print("startTrans(", srcText, lang_from, lang_to, ")")
        if srcText == "":
            self.overSignal.emit("")
            return
        try:
            dstText = translateText(srcText, settings["Method"], lang_from, lang_to)
            self.overSignal.emit(dstText)
        except Exception as ex:
            if DEBUG_FLAG:
                print(str(ex))
            self.overSignal.emit("")

class TransArea(QtWidgets.QWidget):
    def __init__(self, title, auto, parent=None):
        super(TransArea, self).__init__(parent)
        
        self.language = QtWidgets.QComboBox()
        self.textArea = QtWidgets.QTextEdit()
        self.title = QtWidgets.QLabel(text=title)

        self.keys = LANGUAGE_LIST[:]
        if not auto:
            self.keys.remove("Auto")

        self.initUI()
    
    def initUI(self):
        self.textArea.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        scrollBar = QtWidgets.QScrollBar()
        self.textArea.setVerticalScrollBar(scrollBar)
        self.textArea.setAcceptRichText(False)
        self.setMinimumWidth(400)

        self.language.addItems(self.keys)

        titleArea = QtWidgets.QHBoxLayout()
        titleArea.addWidget(self.title)
        titleArea.addWidget(self.language)
        titleArea.addStretch(1)

        self.bottomArea = QtWidgets.QHBoxLayout()

        transArea = QtWidgets.QVBoxLayout()
        transArea.addLayout(titleArea)
        transArea.addWidget(self.textArea)
        transArea.addLayout(self.bottomArea)

        self.setLayout(transArea)


class MainWindow(QtWidgets.QMainWindow):
    requestTransSignal = QtCore.pyqtSignal(str, str, str)
    def __init__(self):
        super().__init__()

        self.srcArea = TransArea(title=hint.original, auto=True)
        self.dstArea = TransArea(title=hint.target, auto=False)

        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)

        self.transTimer = QtCore.QTimer()
        self.transTimer.setSingleShot(True)
        self.translateThread = QtCore.QThread()
        self.innerThread = TranslateThread()

        self.wordNumLabel = QtWidgets.QLabel()
        self.autoCopyBox = QtWidgets.QCheckBox(hint.autoCopy)

        self.initUI()
        self.initConnections()
        self.srcArea.textArea.setFocus()
    
    def updateWordNumLabel(self):
        self.wordNumLabel.setText("{}/{}".format(
            len(self.srcArea.textArea.toPlainText()),
            MAX_WORD
        ))
    
    def initSrcArea(self):
        self.updateWordNumLabel()
        self.srcArea.language.setCurrentIndex(self.srcArea.keys.index(settings['LangFrom']))
        self.srcArea.bottomArea.addWidget(self.wordNumLabel)

        copyButton = QtWidgets.QPushButton(hint.copy)
        copyButton.clicked.connect(lambda: self.copyButtonClicked(self.srcArea.textArea.toPlainText()))
        clearButton = QtWidgets.QPushButton(hint.clear)
        clearButton.clicked.connect(self.clearButtonClicked)

        self.srcArea.bottomArea.addStretch(1)
        self.srcArea.bottomArea.addWidget(clearButton)
        self.srcArea.bottomArea.addWidget(copyButton)
    
    def initDstArea(self):
        self.dstArea.language.setCurrentIndex(self.dstArea.keys.index(settings['LangTo']))
        copyButton = QtWidgets.QPushButton(hint.copy)
        copyButton.clicked.connect(lambda: self.copyButtonClicked(self.dstArea.textArea.toPlainText()))

        self.autoCopyBox.setChecked(settings['AutoCopy'])
        self.autoCopyBox.stateChanged.connect(self.autoCopyChanged)
        self.dstArea.bottomArea.addStretch(1)
        self.dstArea.bottomArea.addWidget(self.autoCopyBox)
        self.dstArea.bottomArea.addWidget(copyButton)
    
    def initToolbar(self):
        toolbar = self.addToolBar(hint.settings)
        toolbar.setMovable(False)

        settingsAction = QtWidgets.QAction(QtGui.QIcon('res/settings.png'), '&Settings', self)
        settingsAction.triggered.connect(self.openSettings)
        toolbar.addAction(settingsAction)

        helpAction = QtWidgets.QAction(QtGui.QIcon('res/help.png'), '&Help', self)
        helpAction.triggered.connect(self.openHelp)
        toolbar.addAction(helpAction)
    
    def initUI(self):
        self.initSrcArea()
        self.initDstArea()
        self.initToolbar()

        hSpliter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        hSpliter.addWidget(self.srcArea)
        hSpliter.addWidget(getVLine())
        hSpliter.addWidget(self.dstArea)

        mainVBox = QtWidgets.QVBoxLayout()
        mainVBox.addWidget(hSpliter)

        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(mainVBox)

        self.resize(1200, 800)
        self.setWindowTitle('Translate')
        self.setWindowIcon(QtGui.QIcon('./res/translate.png'))
        self.setFont(QtGui.QFont('Microsoft YaHei', 10))
        moveCenter(self)

    def initConnections(self):
        self.srcArea.language.currentIndexChanged.connect(self.setSrcLanguage)
        self.dstArea.language.currentIndexChanged.connect(self.setDstLanguage)
        self.srcArea.textArea.textChanged.connect(self.textChanged)
        self.transTimer.timeout.connect(self.translate)
        
        self.requestTransSignal.connect(self.innerThread.startTrans)
        self.innerThread.overSignal.connect(self.updateDstArea)
        self.innerThread.moveToThread(self.translateThread)
        self.translateThread.start()
    
    @QtCore.pyqtSlot(int)
    def setSrcLanguage(self, i):
        settings['LangFrom'] = self.srcArea.keys[i]
        self.updateWordNumLabel()
        self.textChanged()

    @QtCore.pyqtSlot(int)
    def setDstLanguage(self, i):
        settings['LangTo'] = self.dstArea.keys[i]
        self.translate()
    
    @QtCore.pyqtSlot(str)
    def copyButtonClicked(self, text):
        copyText(text)
        self.srcArea.textArea.setFocus()
    
    @QtCore.pyqtSlot()
    def clearButtonClicked(self):
        self.srcArea.textArea.clear()
        self.srcArea.textArea.setFocus()
    
    @QtCore.pyqtSlot()
    def translate(self):
        if DEBUG_FLAG:
            print('Start translate')
        srcText = self.srcArea.textArea.toPlainText()
        srcText = deleteExtraSpace(srcText)
        if srcText == "":
            return
        self.requestTransSignal.emit(srcText, settings['LangFrom'], settings['LangTo'])
        if isChinese(srcText) and len(srcText) > MAX_ZH_CHAR:
            self.statusbar.showMessage(hint.translating + hint.tooManyContent)
        self.statusbar.showMessage(hint.translating)
    
    @QtCore.pyqtSlot(str)
    def updateDstArea(self, dstText):
        if DEBUG_FLAG:
            print('updateDstArea(', dstText, ')', len(dstText))
        if dstText != "":
            self.dstArea.textArea.setText(dstText)
            self.statusbar.showMessage(hint.succeed)
            if settings['AutoCopy']:
                QtWidgets.QApplication.clipboard().setText(dstText)
        else:
            self.statusbar.showMessage(hint.failed)
    
    @QtCore.pyqtSlot()
    def textChanged(self):
        srcText = self.srcArea.textArea.toPlainText()
        if len(srcText) > MAX_WORD:
            srcText = srcText[:MAX_WORD]
            self.srcArea.textArea.setText(srcText)
            self.statusbar.showMessage(hint.exceed)
        self.updateWordNumLabel()
        self.transTimer.start(settings['TranlateDelay'])
    
    @QtCore.pyqtSlot()
    def autoCopyChanged(self):
        settings['AutoCopy'] = not settings['AutoCopy']
        self.srcArea.textArea.setFocus()
    
    @QtCore.pyqtSlot()
    def openSettings(self):
        settingsWindow = SettingsWindow()
        settingsWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        settingsWindow.exec()
    
    @QtCore.pyqtSlot()
    def openHelp(self):
        helpWindow = HelpWindow()
        helpWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        helpWindow.exec()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())