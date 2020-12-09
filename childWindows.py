from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QLineEdit
from PyQt5.QtGui import QFont, QIcon
from config import *
from utils import moveCenter, encrypt, decrypt

class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        mainVBox = QVBoxLayout()
        firstLabel = QLabel()
        hbox = QHBoxLayout()
        okButton = QPushButton(hint.yes)
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addStretch(1)

        firstLabel.setText(hint.helpContent)
        firstLabel.setOpenExternalLinks(True)
        firstLabel.setAlignment(Qt.AlignCenter)
        okButton.clicked.connect(self.close)

        mainVBox.addWidget(firstLabel)
        mainVBox.addLayout(hbox)

        self.setLayout(mainVBox)

        self.resize(400, 200)
        self.setWindowTitle(hint.help)
        self.setWindowIcon(QIcon('./res/translate.png'))
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setFont(QFont('Microsoft YaHei', 10))
        moveCenter(self)

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setLanguageLabel = QLabel(hint.setLanguage)
        self.setLanguageBox = QComboBox()
        self.needReloadLabel = QLabel(hint.needReload)
        self.setDelayLabel = QLabel(hint.setDelay)
        self.setDelayBox = QComboBox()
        self.setMethodLabel = QLabel(hint.method)
        self.setMethodBox = QComboBox()
        self.baiduAppidLabel = QLabel(hint.baiduAppId)
        self.baiduAppidInput = QLineEdit()
        self.baiduSecretLabel = QLabel(hint.baiduSecret)
        self.baiduSecretInput = QLineEdit()
        self.cancelButton = QPushButton(hint.cancel)
        self.saveButton = QPushButton(hint.save)

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
        self.baiduSecretInput.setEchoMode(QLineEdit.Password)
        self.baiduAppidInput.setText(decrypt(settings['BaiduAppid']))
        self.baiduSecretInput.setText(decrypt(settings['BaiduSecret']))
    
    def initButtons(self):
        self.cancelButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self.saveSettings)
    
    pyqtSlot()
    def saveSettings(self):
        settings.BAIDU_APPID = self.baiduAppidInput.text()
        settings.BAIDU_SECRET = self.baiduSecretInput.text()
        self.newSettings['BaiduAppid'] = encrypt(settings.BAIDU_APPID)
        self.newSettings['BaiduSecret'] = encrypt(settings.BAIDU_SECRET)
        for key in list(DEFAULT_SETTINGS.keys()):
            settings[key] = self.newSettings[key]
        settings.writeSettings()
        self.close()
    
    pyqtSlot(int)
    def changeLanguageVersion(self, i):
        self.newSettings['LanguageVersion'] = LANGUAGE_VERSIONS[i]
    
    pyqtSlot(int)
    def changeTranslateDelay(self, i):
        self.newSettings['TranlateDelay'] = DELAY_LIST[i]
    
    pyqtSlot(int)
    def changeMethod(self, i):
        self.newSettings['Method'] = TRANSLATE_METHOD[i]
    
    def initUI(self):
        hBox = QHBoxLayout()
        vBox= QVBoxLayout()

        gridBox = QGridLayout()
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

        hBox2 = QHBoxLayout()
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
        self.setWindowIcon(QIcon('./res/settings.png'))
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setFont(QFont('Microsoft YaHei', 10))
        moveCenter(self)