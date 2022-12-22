import collections.abc
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
import requests
from hyper.contrib import HTTP20Adapter
import json

def data_dump():

    class BearerAuth(requests.auth.AuthBase):
        def __init__(self, token):
            self.token = token
        def __call__(self, r):
            r.headers["authorization"] = "Bearer " + self.token
            return r


    url = 'https://shk24.ru/api/v1/auth/login'

    session = requests.session()

    session.mount(url, HTTP20Adapter())
    header={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://shk24.ru/auth/login',
    'Content-Length': '63',
    'Content-type': 'application/json',
        }
    payload={
     'phone': '9832655739',
     'password': 'mamasha228',
     'remember': True,
    }


    r = session.post(url, json=payload)
    with open('login.json', 'w', encoding='utf-8') as file:
        json.dump(r.json(), file, indent=2, ensure_ascii=False)

    login = json.loads(r.text)
    token = login['accessToken']
    data = session.get('https://shk24.ru/api/v1/students/1646/loads/1240', auth=BearerAuth(token))

    with open('table.json', 'w', encoding='utf-8') as file:
        json.dump(data.json(), file, indent=2, ensure_ascii=False)

def table(mp):
    cnt = 0
    sheet = [[mp['subject']['name']]]
    for i in range(len(mp['lessons'])):
        if 'grades' in str(mp['lessons'][i]):
            date = dict(mp['lessons'][i])['date']
            theme = dict(mp['lessons'][i])['name']
            grade = dict(mp['lessons'][i])['grades'][0]['grade']['short_name']
            sheet.append([grade])
            #cnt += 1
    #sheet.append(cnt)
    return(sheet)
