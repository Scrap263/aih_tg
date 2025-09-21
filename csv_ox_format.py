import json

with open('clean1.csv', 'r', encoding='UTF-8') as cv:
    dictionary = {}
    examples = ['1']
    a = cv.readlines()
    f = a[:3]
    for i in f:
        d = i.split(sep=',')
        print(d[0].strip())
    for row_1 in a:
        row = row_1.split(sep=',')
        if row[0] not in dictionary:
            f = row[0].strip()
            dictionary[f] = {}
        if row[1] not in dictionary[f]:
            s = row[1].strip()
            dictionary[f][s] = {}
        if row[2] not in dictionary[f][s]:
            t = row[2].strip()
            dictionary[f][s][t] = []
        if row[3] not in dictionary[f][s][t]:
            fr = row[3].strip()
            if fr != examples[-1]:
                examples.append(fr)
                dictionary[f][s][t].append(fr)
    
with open('dictionary.json', 'w', encoding='UTF-8') as pd:
    json.dump(dictionary, pd, indent=4)