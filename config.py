from PyQt5.QtCore import QSettings
from os import path

BAIDU_URL = "https://fanyi-api.baidu.com/api/trans/vip/translate"
GOOGLE_URL = "http://translate.google.cn/translate_a/single"

LANGUAGES = {
    "Auto": "auto",
    "Chinese": "zh",
    "English": "en",
    "Japanese": "jp"
}

DELAY_LIST = [1000, 1500, 2000, 2500, 3000, 4000]

LANGUAGE_VERSIONS = ['Chinese', 'English']

INI_FILE = 'MyTranslator.ini'

DEFAULT_SETTINGS = {
    "LanguageVersion": 'Chinese',
    "LangFrom": "Auto",
    "LangTo": "Chinese",
    "TranlateDelay": 1500,
    "AutoCopy": True,
    "AutoStrip": True
}

class Settings(dict):
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
        if key == 'MaxWord':
            return self.getMaxWord()
        else:
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
        self['AutoCopy'] = True if self['AutoCopy'] == 'true' else False
        self['AutoStrip'] = True if self['AutoStrip'] == 'true' else False

    def getMaxWord(self):
        if self['LanguageVersion'] == 'Chinese':
            return 2000
        else:
            return 6000

settings = Settings(DEFAULT_SETTINGS)

class Method():
    BAIDU = "Baidu"
    GOOGLE = "Google"

class Hint():
    def __init__(self, language):
        self.original = 'Original'
        self.target = 'Translation'
        self.copy = 'Copy'
        self.clear = 'Clear'
        self.autoCopy = 'Auto Copy'
        self.autoStrip = 'Auto Strip'
        self.settings = 'Settings'
        self.needReload = '(Need reload)'
        self.help = 'Help'
        self.yes = 'OK'
        self.helpContent = '''Welcome to visit my Github: <br/><br/>
            <a href='https://github.com/blueice-thu'>Github</a>
            &nbsp;
            <a href='https://blueice-thu.github.io'>GitPage</a>
        '''
        self.exceed = 'Exceed the maximum word'
        self.translating = 'Translating ... ...'
        self.succeed = 'Succeed'
        self.failed = 'Failed'
        self.setLanguage = 'Language: '
        self.setDelay = 'Translate Delay (ms)'
        self.cancel = 'Cancle'
        self.save = 'Save'
        
        if language == 'Chinese':
            self.original = '原文'
            self.target = '译文'
            self.copy = '复制'
            self.clear = '清空'
            self.autoCopy = '自动复制'
            self.autoStrip = '自动去空'
            self.settings = '设置'
            self.needReload = '(重启生效)'
            self.help = '帮助'
            self.yes = '确定'
            self.helpContent = '''欢迎访问我的 Github: <br/><br/>
                <a href='https://github.com/blueice-thu'>Github</a>
                &nbsp;
                <a href='https://blueice-thu.github.io'>GitPage</a>
            '''
            self.exceed = '超过最大字数'
            self.translating = '翻译中……'
            self.succeed = '成功'
            self.failed = '失败'
            self.setLanguage = '语言: '
            self.setDelay = '翻译延迟/ms: '
            self.cancel = '取消'
            self.save = '保存'

hint = Hint(settings['LanguageVersion'])
