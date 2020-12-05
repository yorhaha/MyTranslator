# import requests
import json
from config import *
from random import randint
from requests import get as requestsGet
# from hashlib import md5

# def baidu_trans(text, lang_from, lang_to):
#     salt = randint(1e3, 1e6)
#     sign = BAIDU_APPID + text + str(salt) + BAIDU_SECRET
#     sign = md5(sign.encode()).hexdigest()
#     res = requests.post(
#         url=BAIDU_URL,
#         data={
#             "q": text,
#             "from": LANGUAGES[lang_from],
#             "to": LANGUAGES[lang_to],
#             "appid": BAIDU_APPID,
#             "salt": salt,
#             "sign": sign
#         }
#     )
#     if not res.ok:
#         return None
#     res_dict = json.loads(res.text)
#     if res_dict.get("error_code"):
#         return None
#     answer = ''
#     for e in res_dict["trans_result"]:
#         answer += e['dst']
#         answer += '\n'
#     answer = answer[:-1]
#     return answer

def googleTrans(text, langFrom, langTo):
    res = requestsGet(
        url=GOOGLE_URL,
        params={
            "client": "gtx",
            "dt": "t",
            "dj": "1",
            "ie": "UTF-8",
            "sl": LANGUAGES[langFrom],
            "tl": LANGUAGES[langTo],
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


def translateText(text, trans_method, lang_from, lang_to):
    if text is None or Method is None:
        return None
    if text == "":
        return ""
    if trans_method == Method.BAIDU:
        return googleTrans(text, lang_from, lang_to)
    return None

