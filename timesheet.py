import json


with open("table.json", "r", encoding='utf-8') as my_file:
    mp = json.loads(my_file.read())

def table(mp):
    cnt = 0
    sheet = [mp['subject']['name']]
    for i in range(len(mp['lessons'])):
        if 'grades' in str(mp['lessons'][i]):
            date = mp['lessons'][i]['date']
            theme = mp['lessons'][i]['name']
            grade = mp['lessons'][i]['grades'][0]['grade']['short_name']
            if date not in sheet[1:]:
                sheet.append({date: [grade, theme]})
            else:
                sheet[date] = [sheet[date][0] + '/' + grade, theme]
            cnt += 1
    return(sheet)


# print(*table(mp))