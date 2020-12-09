from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from config import *
from utils import moveCenter, encrypt, decrypt

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
        self.needReloadLabel = QtWidgets.QLabel(hint.needReload)
        self.setDelayLabel = QtWidgets.QLabel(hint.setDelay)
        self.setDelayBox = QtWidgets.QComboBox()
        self.setMethodLabel = QtWidgets.QLabel(hint.method)
        self.setMethodBox = QtWidgets.QComboBox()
        self.baiduAppidLabel = QtWidgets.QLabel(hint.baiduAppId)
        self.baiduAppidInput = QtWidgets.QLineEdit()
        self.baiduSecretLabel = QtWidgets.QLabel(hint.baiduSecret)
        self.baiduSecretInput = QtWidgets.QLineEdit()
        self.cancelButton = QtWidgets.QPushButton(hint.cancel)
        self.saveButton = QtWidgets.QPushButton(hint.save)

        self.newSettings = dict(DEFAULT_SETTINGS)
        for key in list(DEFAULT_SETTINGS.keys()):
            self.newSettings[key] = settings[key]

        self.initComboBox()
        self.initLineEdit()
        self.initButtons()
        self.initUI()
    
    def initComboBox(self):
        self.setLanguageBox.addItems(LANGUAGE_VERSIONS)
        self.setLanguageBox.setCurrentIndex(LANGUAGE_VERSIONS.index(settings['LanguageVersion']))
        self.setLanguageBox.currentIndexChanged.connect(self.changeLanguageVersion)

        self.setDelayBox.addItems([str(e) for e in DELAY_LIST])
        self.setDelayBox.setCurrentIndex(DELAY_LIST.index(settings['TranlateDelay']))
        self.setDelayBox.currentIndexChanged.connect(self.changeTranslateDelay)

        self.setMethodBox.addItems([hint.methodList[i] for i in range(len(TRANSLATE_METHOD))])
        self.setMethodBox.setCurrentIndex(TRANSLATE_METHOD.index(settings['Method']))
        self.setMethodBox.currentIndexChanged.connect(self.changeMethod) # TODO
    
    def initLineEdit(self):
        self.baiduSecretInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.baiduAppidInput.setText(decrypt(settings['BaiduAppid']))
        self.baiduSecretInput.setText(decrypt(settings['BaiduSecret']))
    
    def initButtons(self):
        self.cancelButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self.saveSettings)
    
    @QtCore.pyqtSlot()
    def saveSettings(self):
        settings.BAIDU_APPID = self.baiduAppidInput.text()
        settings.BAIDU_SECRET = self.baiduSecretInput.text()
        self.newSettings['BaiduAppid'] = encrypt(settings.BAIDU_APPID)
        self.newSettings['BaiduSecret'] = encrypt(settings.BAIDU_SECRET)
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
    
    @QtCore.pyqtSlot(int)
    def changeMethod(self, i):
        self.newSettings['Method'] = TRANSLATE_METHOD[i]
    
    def initUI(self):
        hBox = QtWidgets.QHBoxLayout()
        vBox= QtWidgets.QVBoxLayout()

        gridBox = QtWidgets.QGridLayout()
        gridBox.addWidget(self.setLanguageLabel, 0, 0)
        gridBox.addWidget(self.setLanguageBox, 0, 1)
        gridBox.addWidget(self.needReloadLabel, 0, 2)
        gridBox.addWidget(self.setDelayLabel, 1, 0)
        gridBox.addWidget(self.setDelayBox, 1, 1)
        gridBox.addWidget(self.setMethodLabel, 2, 0)
        gridBox.addWidget(self.setMethodBox, 2, 1)
        gridBox.addWidget(self.baiduAppidLabel, 3, 0)
        gridBox.addWidget(self.baiduAppidInput, 3, 1)
        gridBox.addWidget(self.baiduSecretLabel, 4, 0)
        gridBox.addWidget(self.baiduSecretInput, 4, 1)
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