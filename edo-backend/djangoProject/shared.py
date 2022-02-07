import datetime
import hashlib


def md5(str):
    return hashlib.md5(
        (str).lower().encode()
    ).hexdigest()


#метод для формирования уникального токена
def getToken(login):
    return md5((login + str(datetime.datetime.now())))