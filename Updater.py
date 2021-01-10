from json import loads
from requests import session
from config import VERSION_URL, VERSION_FILE
from utils import getUrl


def getCurrentVersion():
    with open(VERSION_FILE, 'r') as f:
        info = f.read()
        info = loads(info)
        return info


def getNewestVersion():
    s = session()
    s.keep_alive = False
    info = getUrl(VERSION_URL)
    info = loads(info.text)
    return info


def hasNewVersion():
    current = getCurrentVersion()
    # TODO
    return current
    try:
        newest = getNewestVersion()
        if float(current['Version']) < float(newest['Version']):
            return newest
    except Exception as e:
        print(e)
    return None

