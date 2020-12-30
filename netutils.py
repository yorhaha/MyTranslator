# import requests
import json
from config import *
from random import randint
from requests import get as requestsGet
from requests import post as requestsPost
from hashlib import md5

def baiduTrans(text, lang_from, lang_to):
    if DEBUG_FLAG:
        print('baidu_trans(', text, lang_from, lang_to, ')')
        print('BAIDU_APPID = ', settings.BAIDU_APPID)
        print('BAIDU_SECRET = ', settings.BAIDU_SECRET)
    salt = randint(1e3, 1e6)
    sign = settings.BAIDU_APPID + text + str(salt) + settings.BAIDU_SECRET
    sign = md5(sign.encode()).hexdigest()
    res = requestsPost(
        url=BAIDU_URL,
        data={
            "q": text,
            "from": BAIDU_LANGUAGES[lang_from],
            "to": BAIDU_LANGUAGES[lang_to],
            "appid": settings.BAIDU_APPID,
            "salt": salt,
            "sign": sign
        }
    )
    if DEBUG_FLAG:
        print({
            "q": text,
            "from": BAIDU_LANGUAGES[lang_from],
            "to": BAIDU_LANGUAGES[lang_to],
            "appid": settings.BAIDU_APPID,
            "salt": salt,
            "sign": sign
        })
    if not res.ok:
        return None
    res_dict = json.loads(res.text)
    if res_dict.get("error_code"):
        return None
    answer = ''
    for e in res_dict["trans_result"]:
        answer += e['dst']
        answer += '\n'
    answer = answer[:-1]
    return answer

def googleTrans(text, langFrom, langTo):
    if DEBUG_FLAG:
        print('Using Google Method')
    res = requestsGet(
        url=GOOGLE_URL,
        params={
            "client": "gtx",
            "dt": "t",
            "dj": "1",
            "ie": "UTF-8",
            "sl": GOOGLE_LANGUAGES[langFrom],
            "tl": GOOGLE_LANGUAGES[langTo],
            "q": text
        }
    )
    if not res.ok:
        return None
    sentences = json.loads(res.text)["sentences"]
    answer = ''
    for sen in sentences:
        answer += sen["trans"]
        answer += '\n'
    answer = answer[:-1]
    return answer

def youdaoTrans(text, langFrom, langTo, isSentence=True):
    if DEBUG_FLAG:
        print({
            "doctype": "json",
            "type": YOUDAO_LANGUAGES[langFrom] + '2' + YOUDAO_LANGUAGES[langTo],
            'i': text
        })
    transType = 'AUTO2' + YOUDAO_LANGUAGES[langTo]
    if langFrom != 'Auto':
        transType = YOUDAO_LANGUAGES[langFrom] + '2' + YOUDAO_LANGUAGES[langTo]
    res = requestsGet(
        url=YOUDAO_URL,
        params={
            "doctype": "json",
            "type": transType,
            'i': text
        }
    )
    if not res.ok:
        return None
    res = json.loads(res.text)
    if DEBUG_FLAG:
        print(res)
    errorCode = res["errorCode"]
    if errorCode != 0:
        return None
    translateResult = res["translateResult"]
    answer = ""
    for sen in translateResult:
        for s in sen:
            answer += s["tgt"]
        answer += "\n"
    answer = answer[:-1]
    return answer

def translateText(text, trans_method, lang_from, lang_to):
    if text is None:
        return None
    if text == "":
        return ""
    
    if DEBUG_FLAG:
        print('translateText(', text, trans_method, lang_from, lang_to, ')')

    if trans_method == 'Google':
        return googleTrans(text, lang_from, lang_to)
    elif trans_method == 'Baidu':
        return baiduTrans(text, lang_from, lang_to)
    elif trans_method == 'Youdao':
        return youdaoTrans(text, lang_from, lang_to)
    return None

