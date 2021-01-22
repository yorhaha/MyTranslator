from PyQt5.QtCore import QSettings
from os import path
from hint import getHint
from utils import decrypt

BAIDU_URL = "https://fanyi-api.baidu.com/api/trans/vip/translate"
GOOGLE_URL = "http://translate.google.cn/translate_a/single"
YOUDAO_URL = "http://fanyi.youdao.com/translate"

VERSION_URL = "https://raw.github.com/blueice-thu/MyTranslator/master/VersionInfo.json"

DEBUG_FLAG = False

DELAY_LIST = [1000, 1500, 2000, 2500, 3000, 4000]

TRANSLATE_METHOD = ['Google', 'Baidu', 'Youdao']
LANGUAGE_LIST = ["Auto", "Chinese", "English", "Japanese", "Traditional Chinese"]
LANGUAGE_VERSIONS = ['Chinese', 'English']

INI_FILE = 'MyTranslator.ini'
VERSION_FILE = 'VersionInfo.json'
HISTORY_FILE = 'history.txt'

THEME_LIST = ['Default', 'Ubuntu', 'ElegantDark', 'Aqua', 'ManjaroMix', 'DarkOrange']

WORK_PATH = path.dirname(path.abspath(__file__)).replace("\\", '/')

MAX_ZH_CHAR = 2000
MAX_WORD = 6000

DEFAULT_SETTINGS = {
    "LanguageVersion": 'Chinese',
    "LangFrom": "Auto",
    "LangTo": "Chinese",
    "TranlateDelay": 1500,
    "AutoTrans": True,
    "AutoCopy": True,
    "CheckUpdate": False,
    "BaiduAppid": "",
    "BaiduSecret": "",
    "Method": "Google",
    'Theme': "Default",
    'TopWindow': False
}


class Settings(dict):
    BAIDU_APPID = ''
    BAIDU_SECRET = ''

    def __init__(self, item):
        super().__init__(item)
        if not path.exists(INI_FILE) or not path.isfile(INI_FILE):
            with open(INI_FILE, 'w') as f:
                pass
            self.settingFile = QSettings(INI_FILE, QSettings.IniFormat)
            self.writeSettings()
        else:
            self.settingFile = QSettings(INI_FILE, QSettings.IniFormat)
            self.readSettings()

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.settingFile.setValue(key, value)

    def writeSettings(self):
        for k, v in self.items():
            self.settingFile.setValue(k, v)

    def readSettings(self):
        for key in list(DEFAULT_SETTINGS.keys()):
            self[key] = self.settingFile.value(key)
        self.convert()

    def convert(self):
        self['TranlateDelay'] = int(self['TranlateDelay'])
        self['AutoTrans'] = True if self['AutoTrans'] == 'true' else False
        self['AutoCopy'] = True if self['AutoCopy'] == 'true' else False
        self['CheckUpdate'] = True if self['CheckUpdate'] == 'true' else False
        self['TopWindow'] = True if self['TopWindow'] == 'true' else False
        self.BAIDU_APPID = decrypt(self['BaiduAppid'])
        self.BAIDU_SECRET = decrypt(self['BaiduSecret'])


settings = Settings(DEFAULT_SETTINGS)
if DEBUG_FLAG:
    print(settings)

GOOGLE_LANGUAGES = {
    "Auto": "auto",
    "Chinese": "zh_CN",
    "English": "en",
    "Japanese": "ja",
    "Traditional Chinese": "zh_TW"
}

BAIDU_LANGUAGES = {
    "Auto": "auto",
    "Chinese": "zh",
    "English": "en",
    "Japanese": "jp",
    "Traditional Chinese": "cht"
}

YOUDAO_LANGUAGES = {
    "Auto": "AUTO",
    "English": "EN",
    "Chinese": "ZH_CN",
    "Japanese": "JA"
}

hint = getHint(settings['LanguageVersion'])
