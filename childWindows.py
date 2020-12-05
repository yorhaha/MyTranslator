from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from config import *
from utils import moveCenter
import copy

class HelpWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        mainVBox = QtWidgets.QVBoxLayout()
        firstLabel = QtWidgets.QLabel()
        hbox = QtWidgets.QHBoxLayout()
        okButton = QtWidgets.QPushButton(hint.yes)
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addStretch(1)

        firstLabel.setText(hint.helpContent)
        firstLabel.setOpenExternalLinks(True)
        firstLabel.setAlignment(QtCore.Qt.AlignCenter)
        okButton.clicked.connect(self.close)

        mainVBox.addWidget(firstLabel)
        mainVBox.addLayout(hbox)

        self.setLayout(mainVBox)

        self.resize(400, 200)
        self.setWindowTitle(hint.help)
        self.setWindowIcon(QtGui.QIcon('./res/translate.png'))
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        self.setFont(QtGui.QFont('Microsoft YaHei', 10))
        moveCenter(self)

class SettingsWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setLanguageLabel = QtWidgets.QLabel(hint.setLanguage)
        self.setLanguageBox = QtWidgets.QComboBox()
        self.setDelayLabel = QtWidgets.QLabel(hint.setDelay)
        self.setDelayBox = QtWidgets.QComboBox()
        self.cancelButton = QtWidgets.QPushButton(hint.cancel)
        self.saveButton = QtWidgets.QPushButton(hint.save)
        self.needReloadLabel = QtWidgets.QLabel(hint.needReload)

        self.newSettings = dict(DEFAULT_SETTINGS)
        for key in list(DEFAULT_SETTINGS.keys()):
            self.newSettings[key] = settings[key]

        self.initComboBox()
        self.initButtons()
        self.initUI()
    
    def initComboBox(self):
        self.setLanguageBox.addItems(LANGUAGE_VERSIONS)
        self.setLanguageBox.setCurrentIndex(LANGUAGE_VERSIONS.index(settings['LanguageVersion']))
        self.setLanguageBox.currentIndexChanged.connect(self.changeLanguageVersion)

        self.setDelayBox.addItems([str(e) for e in DELAY_LIST])
        self.setDelayBox.setCurrentIndex(DELAY_LIST.index(settings['TranlateDelay']))
        self.setDelayBox.currentIndexChanged.connect(self.changeTranslateDelay)
    
    def initButtons(self):
        self.cancelButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self.saveSettings)
    
    @QtCore.pyqtSlot()
    def saveSettings(self):
        for key in list(DEFAULT_SETTINGS.keys()):
            settings[key] = self.newSettings[key]
        settings.writeSettings()
        self.close()
    
    @QtCore.pyqtSlot(int)
    def changeLanguageVersion(self, i):
        self.newSettings['LanguageVersion'] = LANGUAGE_VERSIONS[i]
    
    @QtCore.pyqtSlot(int)
    def changeTranslateDelay(self, i):
        self.newSettings['TranlateDelay'] = DELAY_LIST[i]
    
    def initUI(self):
        hBox = QtWidgets.QHBoxLayout()
        vBox= QtWidgets.QVBoxLayout()

        gridBox = QtWidgets.QGridLayout()
        gridBox.addWidget(self.setLanguageLabel, 0, 0)
        gridBox.addWidget(self.setLanguageBox, 0, 1)
        gridBox.addWidget(self.needReloadLabel, 0, 2)
        gridBox.addWidget(self.setDelayLabel, 1, 0)
        gridBox.addWidget(self.setDelayBox, 1, 1)
        gridBox.setColumnStretch(0, 1)
        gridBox.setColumnStretch(1, 2)

        hBox2 = QtWidgets.QHBoxLayout()
        hBox2.addStretch(1)
        hBox2.addWidget(self.cancelButton)
        hBox2.addWidget(self.saveButton)

        hBox.addStretch(1)
        vBox.addLayout(gridBox)
        vBox.addLayout(hBox2)
        hBox.addLayout(vBox)
        hBox.addStretch(1)

        self.setLayout(hBox)

        self.resize(600, 300)
        self.setWindowTitle(hint.settings)
        self.setWindowIcon(QtGui.QIcon('./res/settings.png'))
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        self.setFont(QtGui.QFont('Microsoft YaHei', 10))
        moveCenter(self)