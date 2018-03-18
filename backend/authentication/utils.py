import requests


def login_check(token=None, host=None):
    url = 'http://' + host + '/api/user/'
    payload = {"token": token}
    r = requests.post(url, json=payload)
    flag = True if r.json()['flag'] == 1 else False
    return flag, r.json()['id']
