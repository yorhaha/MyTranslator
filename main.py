from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QObject, QThread, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QAction, \
    QPushButton, QCheckBox, QLabel, QStatusBar, QComboBox, QTextEdit, QScrollBar

from config import *
from netutils import *
from utils import *
from Updater import hasNewVersion
from childWindows import HelpWindow, SettingsWindow, UpdateWindow
import sys
from time import sleep
from threading import Thread


class TranslateThread(QObject):
    overSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @pyqtSlot(str, str, str)
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


class UpdateThread(QObject):
    overSignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @pyqtSlot()
    def checkUpdate(self):
        if DEBUG_FLAG:
            print("checkUpdate")
        newVersion = hasNewVersion()
        if newVersion:
            print('need update')
            self.overSignal.emit(newVersion)
        print('update over')


class TransArea(QWidget):
    def __init__(self, title, auto, parent=None):
        super(TransArea, self).__init__(parent)

        self.language = QComboBox()
        self.textArea = QTextEdit()
        self.title = QLabel(text=title)
        self.bottomArea = QHBoxLayout()

        self.keys = LANGUAGE_LIST[:]
        if not auto:
            self.keys.remove("Auto")

        self.initUI()

    def initUI(self):
        self.textArea.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        scrollBar = QScrollBar()
        self.textArea.setVerticalScrollBar(scrollBar)
        self.textArea.setAcceptRichText(False)
        self.setMinimumWidth(400)

        self.language.addItems(self.keys)

        titleArea = QHBoxLayout()
        titleArea.addWidget(self.title)
        titleArea.addWidget(self.language)
        titleArea.addStretch(1)

        transArea = QVBoxLayout()
        transArea.addLayout(titleArea)
        transArea.addWidget(self.textArea)
        transArea.addLayout(self.bottomArea)

        self.setLayout(transArea)


class MainWindow(QMainWindow):
    requestTransSignal = pyqtSignal(str, str, str)
    startUpdateSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.srcArea = TransArea(title=hint['original'], auto=True)
        self.dstArea = TransArea(title=hint['target'], auto=False)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.transTimer = QTimer()
        self.transTimer.setSingleShot(True)
        self.translateThread = QThread()
        self.innerTransThread = TranslateThread()
        self.updateThread = QThread()
        self.innerUpdateThread = UpdateThread()

        self.wordNumLabel = QLabel()
        self.autoTransBox = QCheckBox(hint['autoTrans'])
        self.autoCopyBox = QCheckBox(hint['autoCopy'])
        self.translateButton = QPushButton(hint['translate'])

        self.topWindow = False
        self.topAction = QAction(QIcon('res/top.png'), '&Top', self)
        self.topAction.triggered.connect(self.changeTop)

        self.initUI()
        self.loadTheme()
        self.initConnections()
        self.srcArea.textArea.setFocus()
        
        if settings['CheckUpdate']:
            self.startUpdateSignal.emit()

    def loadTheme(self, theme=None):
        if theme is None:
            theme = settings['Theme']
        self.setStyleSheet(readQss(WORK_PATH + '/themes', theme))

    def updateWordNumLabel(self):
        self.wordNumLabel.setText("{}/{}".format(
            len(self.srcArea.textArea.toPlainText()),
            MAX_WORD
        ))

    def initSrcArea(self):
        self.updateWordNumLabel()
        self.srcArea.language.setCurrentIndex(self.srcArea.keys.index(settings['LangFrom']))
        self.srcArea.bottomArea.addWidget(self.wordNumLabel)

        copyButton = QPushButton(hint['copy'])
        copyButton.clicked.connect(lambda: self.copyButtonClicked(self.srcArea.textArea.toPlainText()))
        clearButton = QPushButton(hint['clear'])
        clearButton.clicked.connect(self.clearButtonClicked)
        self.translateButton.clicked.connect(self.translate)

        self.autoTransBox.setChecked(settings['AutoTrans'])
        self.autoTransBox.stateChanged.connect(self.autoTransChanged)
        self.srcArea.bottomArea.addStretch(1)
        self.srcArea.bottomArea.addWidget(self.autoTransBox)
        self.srcArea.bottomArea.addWidget(self.translateButton)
        self.srcArea.bottomArea.addWidget(clearButton)
        self.srcArea.bottomArea.addWidget(copyButton)
        if settings['AutoTrans']:
            self.translateButton.hide()

    def initDstArea(self):
        self.dstArea.language.setCurrentIndex(self.dstArea.keys.index(settings['LangTo']))
        copyButton = QPushButton(hint['copy'])
        copyButton.clicked.connect(lambda: self.copyButtonClicked(self.dstArea.textArea.toPlainText()))
        swapButton = QPushButton(icon=QIcon('./res/swap.png'))
        swapButton.clicked.connect(self.swapSrcDst)

        self.autoCopyBox.setChecked(settings['AutoCopy'])
        self.autoCopyBox.stateChanged.connect(self.autoCopyChanged)
        self.dstArea.bottomArea.addWidget(swapButton)
        self.dstArea.bottomArea.addStretch(1)
        self.dstArea.bottomArea.addWidget(self.autoCopyBox)
        self.dstArea.bottomArea.addWidget(copyButton)

    def initToolbar(self):
        toolbar = self.addToolBar(hint['settings'])
        toolbar.setMovable(False)

        toolbar.addAction(self.topAction)

        settingsAction = QAction(QIcon('res/settings.png'), '&Settings', self)
        settingsAction.triggered.connect(self.openSettings)
        toolbar.addAction(settingsAction)

        helpAction = QAction(QIcon('res/help.png'), '&Help', self)
        helpAction.triggered.connect(self.openHelp)
        toolbar.addAction(helpAction)

    def initUI(self):
        self.initSrcArea()
        self.initDstArea()
        self.initToolbar()

        hSpliter = QSplitter(Qt.Horizontal)
        hSpliter.addWidget(self.srcArea)
        hSpliter.addWidget(getVLine())
        hSpliter.addWidget(self.dstArea)

        mainVBox = QVBoxLayout()
        mainVBox.addWidget(hSpliter)

        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(mainVBox)

        srcText, dstText = readHistory(HISTORY_FILE)
        self.srcArea.textArea.setText(srcText)
        self.dstArea.textArea.setText(dstText)

        self.resize(1200, 800)
        self.setWindowTitle('My Translator')
        self.setWindowIcon(QIcon('./res/translate.png'))
        moveCenter(self)

    def initConnections(self):
        self.srcArea.language.currentIndexChanged.connect(self.setSrcLanguage)
        self.dstArea.language.currentIndexChanged.connect(self.setDstLanguage)
        self.srcArea.textArea.textChanged.connect(self.textChanged)
        self.transTimer.timeout.connect(self.translate)

        self.requestTransSignal.connect(self.innerTransThread.startTrans)
        self.innerTransThread.overSignal.connect(self.updateDstArea)
        self.innerTransThread.moveToThread(self.translateThread)
        self.translateThread.start()

        self.startUpdateSignal.connect(self.innerUpdateThread.checkUpdate)
        self.innerUpdateThread.overSignal.connect(self.showUpdateWindow)
        self.innerUpdateThread.moveToThread(self.updateThread)
        self.updateThread.start()

    @pyqtSlot(int)
    def setSrcLanguage(self, i):
        settings['LangFrom'] = self.srcArea.keys[i]
        self.updateWordNumLabel()
        self.textChanged()

    @pyqtSlot(int)
    def setDstLanguage(self, i):
        settings['LangTo'] = self.dstArea.keys[i]
        self.translate()

    @pyqtSlot(str)
    def copyButtonClicked(self, text):
        copyText(text)
        self.srcArea.textArea.setFocus()

    @pyqtSlot()
    def swapSrcDst(self):
        print(self.dstArea.textArea.toPlainText())
        self.srcArea.textArea.setText(self.dstArea.textArea.toPlainText())
        self.dstArea.textArea.clear()

    @pyqtSlot()
    def clearButtonClicked(self):
        self.srcArea.textArea.clear()
        self.srcArea.textArea.setFocus()

    @pyqtSlot()
    def translate(self):
        if DEBUG_FLAG:
            print('Start translate')
        srcText = self.srcArea.textArea.toPlainText()
        srcText = deleteExtraSpace(srcText)
        if srcText == "":
            return
        self.requestTransSignal.emit(srcText, settings['LangFrom'], settings['LangTo'])
        if isChinese(srcText) and len(srcText) > MAX_ZH_CHAR:
            self.statusbar.showMessage(hint['translating'] + hint['tooManyContent'])
        self.statusbar.showMessage(hint['translating'])

    @pyqtSlot(str)
    def updateDstArea(self, dstText):
        if DEBUG_FLAG:
            print('updateDstArea(', dstText, ')', len(dstText))
        if dstText != "":
            self.dstArea.textArea.setText(dstText)
            writeHistory(HISTORY_FILE, self.srcArea.textArea.toPlainText(), dstText)
            self.statusbar.showMessage(hint['succeed'])
            if settings['AutoCopy']:
                QApplication.clipboard().setText(dstText)
        else:
            self.statusbar.showMessage(hint['failed'])

    @pyqtSlot()
    def textChanged(self):
        if not settings['AutoTrans']:
            return
        srcText = self.srcArea.textArea.toPlainText()
        if len(srcText) > MAX_WORD:
            srcText = srcText[:MAX_WORD]
            self.srcArea.textArea.setText(srcText)
            self.statusbar.showMessage(hint['exceed'])
        self.updateWordNumLabel()
        self.transTimer.start(settings['TranlateDelay'])

    @pyqtSlot()
    def autoCopyChanged(self):
        settings['AutoCopy'] = not settings['AutoCopy']
        self.srcArea.textArea.setFocus()

    @pyqtSlot()
    def autoTransChanged(self):
        settings['AutoTrans'] = not settings['AutoTrans']
        if settings['AutoTrans']:
            self.translateButton.hide()
        else:
            self.translateButton.show()
        self.srcArea.textArea.setFocus()

    @pyqtSlot()
    def openSettings(self):
        settingsWindow = SettingsWindow()
        settingsWindow.setWindowModality(Qt.ApplicationModal)
        settingsWindow.exec()
        self.loadTheme()

    @pyqtSlot()
    def openHelp(self):
        helpWindow = HelpWindow()
        helpWindow.setWindowModality(Qt.ApplicationModal)
        helpWindow.exec()

    @pyqtSlot(dict)
    def showUpdateWindow(self, newVersion):
        if newVersion:
            sleep(1)
            updateWindow = UpdateWindow(newVersion)
            updateWindow.setWindowModality(Qt.ApplicationModal)
            updateWindow.exec()

    def changeTop(self):
        self.topWindow = not self.topWindow
        if self.topWindow:
            self.topAction.setIcon(QIcon('./res/topped.png'))
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.statusbar.showMessage(hint['setTop'])
        else:
            self.topAction.setIcon(QIcon('./res/top.png'))
            self.setWindowFlags(Qt.Widget)
            self.statusbar.showMessage(hint['cancelTop'])
        self.show()
        self.srcArea.textArea.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
