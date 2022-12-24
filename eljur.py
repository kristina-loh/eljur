
import collections.abc
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
import requests
from hyper.contrib import HTTP20Adapter
import json
import datetime

from timesheet import table

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


url = 'https://shk24.ru/api/v1/auth/login'

session = requests.session()

header={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://shk24.ru/auth/login',
    'Content-type': 'application/json',
    }
payload={
     'phone': '9131706807',
     'password': 'pup624txx',
     'remember': True,
}


r = session.post(url, json=payload)
with open('login.json', 'w', encoding='utf-8') as file:
    json.dump(r.json(), file, indent=2, ensure_ascii=False)
#print(r.json())

login = json.loads(r.text)


token = login['accessToken']

user_id = login['user']['id']

print(user_id)

mx = 0


lessons = session.get('https://shk24.ru/api/v1/students/' + str(user_id) + '/performance', auth = BearerAuth(token))
lessons = lessons.json()
dates = set()
grades = []
for i in range(len(lessons[0]['loads'])):
    print(lessons[0]['loads'][i]['id'])
    data = session.get('https://shk24.ru/api/v1/students/' + str(user_id) + '/loads/' + str(lessons[0]['loads'][i]['id']), auth=BearerAuth(token))
    mx_id = str(lessons[0]['loads'][i]['id'])
    with open('table.json', 'w', encoding='utf-8') as file:
        json.dump(data.json(), file, indent=2, ensure_ascii=False)
    t = table(data.json())
    for i in range(1, len(table(data.json())) - 1):
        dates.add(t[i][0])
    grades.append(t)
dates = list(dates)
dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in dates]
dates.sort()
dates = ['Предмет\Дата'] + [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
grades_list = [dates]
grades_list += [['*' for i in range(len(dates))] for i in range(len(grades))]

# for i in range(1, len(dates) - 1):
#     for j in range(1, len(grades) - 1):
#         for k in range()


for i in range(1, len(dates)):
    for j in range(len(grades)):
        name_subject = grades[j][0]
        if not(name_subject in grades_list):
            if name_subject[0] == 'Основы безопасности и жизнедеятельности':
                name_subject[0] = 'ОБЖ'
            elif name_subject[0] == 'Проектная деятельность':
                name_subject[0] = 'ПД'
            grades_list[j + 1][0] = name_subject[0]
        for k in range(1, len(grades[j])):
            grade_and_date = grades[j][k]
            date = grade_and_date[0]
            grade = grade_and_date[1]
            if date in grades_list[0]:
                grades_list[j + 1][grades_list[0].index(date)] = grade

f = open('test.txt', 'w', encoding='utf-8')
for i in grades_list:
    f.write(' '.join(i) + '\n') 
f.close()


