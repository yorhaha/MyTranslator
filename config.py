from PyQt5.QtCore import QSettings
from os import path
from utils import decrypt

BAIDU_URL = "https://fanyi-api.baidu.com/api/trans/vip/translate"
GOOGLE_URL = "http://translate.google.cn/translate_a/single"
YOUDAO_URL = "http://fanyi.youdao.com/translate"

DEBUG_FLAG = True

DELAY_LIST = [1000, 1500, 2000, 2500, 3000, 4000]

TRANSLATE_METHOD = ['Google', 'Baidu', 'Youdao']
LANGUAGE_LIST = ["Auto", "Chinese", "English", "Japanese", "Traditional Chinese"]
LANGUAGE_VERSIONS = ['Chinese', 'English']

INI_FILE = 'MyTranslator.ini'

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
    "BaiduAppid": "",
    "BaiduSecret": "",
    "Method": "Google",
    'Theme': "Default"
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


class Hint:
    def __init__(self, language):
        self.original = 'Original'
        self.target = 'Translation'
        self.translate = 'Translate'
        self.copy = 'Copy'
        self.clear = 'Clear'
        self.autoTrans = 'Auto Translate'
        self.autoCopy = 'Auto Copy'
        self.settings = 'Settings'
        self.needReload = '(Need reload)'
        self.help = 'Help'
        self.yes = 'OK'
        self.helpContent = '''
            Baidu provides free translation server. Get APPID and Secret here: <br/><br/>
            <a href='https://api.fanyi.baidu.com/product/11'>Register Baidu API</a><br/><br/>
            Welcome to visit my Github: <br/><br/>
            <a href='https://github.com/blueice-thu/MyTranslator'>Github</a>
            &nbsp;
            <a href='https://blueice-thu.github.io'>GitPage</a>
        '''
        self.exceed = 'Exceed the maximum word'
        self.translating = 'Translating ... ...'
        self.succeed = 'Succeed'
        self.failed = 'Failed'
        self.setLanguage = 'Language: '
        self.setDelay = 'Translate Delay (ms): '
        self.setTheme = 'Theme: '
        self.methodList = ['Google', 'Baidu', 'Youdao']
        self.method = 'Translate Method: '
        self.baiduAppId = 'Baidu AppID: '
        self.baiduSecret = 'Baidu Secret: '
        self.write = 'Write'
        self.cancel = 'Cancle'
        self.save = 'Save'
        self.tooManyContent = 'Too many characters and effect reduced'

        if language == 'Chinese':
            self.original = '原文'
            self.target = '译文'
            self.translate = '翻译'
            self.copy = '复制'
            self.clear = '清空'
            self.autoTrans = '自动翻译'
            self.autoCopy = '自动复制'
            self.settings = '设置'
            self.needReload = '(重启生效)'
            self.help = '帮助'
            self.yes = '确定'
            self.helpContent = '''
                百度提供免费的翻译服务，你可以注册以获得 APPID 和 Secret: <br/><br/>
                <a href='https://api.fanyi.baidu.com/product/11'>注册百度翻译 API</a><br/><br/>
                欢迎访问我的 Github: <br/><br/>
                <a href='https://github.com/blueice-thu/MyTranslator'>Github</a>
                &nbsp;
                <a href='https://blueice-thu.github.io'>GitPage</a>
            '''
            self.exceed = '超过最大字数'
            self.translating = '翻译中……'
            self.succeed = '成功'
            self.failed = '失败'
            self.setLanguage = '语言: '
            self.setDelay = '翻译延迟/ms: '
            self.setTheme = '主题: '
            self.methodList = ['谷歌', '百度', '有道']
            self.method = '翻译引擎: '
            self.baiduAppId = '百度翻译AppID: '
            self.baiduSecret = '百度翻译密钥: '
            self.write = '填写'
            self.cancel = '取消'
            self.save = '保存'
            self.tooManyContent = '字符过多，可能影响翻译效果'


hint = Hint(settings['LanguageVersion'])
