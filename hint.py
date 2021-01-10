ChineseHelpContent = '''
    百度提供免费的翻译服务，你可以注册以获得 APPID 和 Secret: <br/><br/>
    <a href='https://api.fanyi.baidu.com/product/11'>注册百度翻译 API</a><br/><br/>
    欢迎访问我的 Github: <br/><br/>
    <a href='https://github.com/blueice-thu/MyTranslator'>Github</a>
    &nbsp;
    <a href='https://blueice-thu.github.io'>GitPage</a>
'''
EnglishHelpContent = '''
    Baidu provides free translation server. Get APPID and Secret here: <br/><br/>
    <a href='https://api.fanyi.baidu.com/product/11'>Register Baidu API</a><br/><br/>
    Welcome to visit my Github: <br/><br/>
    <a href='https://github.com/blueice-thu/MyTranslator'>Github</a>
    &nbsp;
    <a href='https://blueice-thu.github.io'>GitPage</a>
'''

HintSet = {
    'original':     ['原文',                'Original'],
    'target':       ['译文',                'Translation'],
    'translate':    ['翻译',                'Translate'],
    'copy':         ['复制',                'Copy'],
    'clear':        ['清空',                'Clear'],
    'autoTrans':    ['自动翻译',            'Auto Translate'],
    'autoCopy':     ['自动复制',            'Auto Copy'],
    'settings':     ['设置',                'Settings'],
    'needReload':   ['(重启生效)',          '(Need reload)'],
    'help':         ['帮助',                'Help'],
    'update':       ['更新',                'Update'],
    'top':          ['置顶',                'Top'],
    'setTop':       ['置顶',                'Top'],
    'cancelTop':    ['取消置顶',             'Top'],
    'yes':          ['确定',                'OK'],
    'exceed':       ['超过最大字数',        'Exceed the maximum word'],
    'translating':  ['翻译中……',            'Translating ... ...'],
    'succeed':      ['成功',                'Succeed'],
    'failed':       ['失败',                'Failed'],
    'setLanguage':  ['语言: ',              'Language: '],
    'setDelay':     ['翻译延迟/ms: ',       'Translate Delay (ms): '],
    'setTheme':     ['主题: ',              'Theme: '],
    'method':       ['翻译引擎: ',          'Translate Method: '],
    'baiduAppId':   ['百度翻译AppID: ',     'Baidu AppID: '],
    'baiduSecret':  ['百度翻译密钥: ',      'Baidu Secret: '],
    'write':        ['填写',                'Write'],
    'cancel':       ['取消',                'Cancel'],
    'save':         ['保存',                'Save'],
    'methodList':   [['谷歌', '百度', '有道'], ['Google', 'Baidu', 'Youdao']],
    'tooManyContent': ['字符过多，可能影响翻译效果', 'Too many characters and effect reduced'],
    'updateDetected': ['检测到新版本：', 'New version detected: '],
    'updateInfo': ['更新日志：', 'Update Info: '],
    'helpContent': [ChineseHelpContent, EnglishHelpContent]
}

def getHint(language):
    default = 0
    if language == 'Chinese':
        default = 0
    elif language == 'English':
        default = 1
    for key in HintSet.keys():
        HintSet[key] = HintSet[key][default]
    return HintSet
