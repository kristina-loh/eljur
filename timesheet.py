import json


with open("table.json", "r", encoding='utf-8') as my_file:
    mp = json.loads(my_file.read())

def table(mp):
    cnt = 0
    sheet = [[mp['subject']['name']]]
    for i in range(len(mp['lessons'])):
        if 'grades' in str(mp['lessons'][i]):
            date = dict(mp['lessons'][i])['date']
            theme = dict(mp['lessons'][i])['name']
            grade = dict(mp['lessons'][i])['grades'][0]['grade']['short_name']
            sheet.append([date, grade])
            cnt += 1
    return(sheet)


# print(table(mp)[2][0])