import json

with open('new_dictionary.json', 'r', encoding='utf-8') as f:
    dic = json.load(f)


new_dict = {}

for word in dic.keys():
    transcription = str(input(f'Введите транскрипцию {word} - '))
    v = list(dic[word].keys())
    transl = v[0]
    new_dict[word] = {}
    value = dic[word][transl]
    new_dict[word][transl] = value
    new_dict[word]['транскрипция'] = f'[{transcription}]'


with open('n_d.json', 'w', encoding='utf-8') as d:
    json.dump(new_dict, d, indent=4, ensure_ascii=False)