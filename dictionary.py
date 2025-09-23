import json
from googletrans import Translator
import asyncio
from deepseek import DeepSeekAPI

ai = DeepSeekAPI()

async def main():
    translator = Translator()

    with open('dic.json', 'r') as f:
        file = json.load(f)

    with open('definitions.json', 'r', encoding='UTF-8') as ff:
        rdl = json.load(ff)

    def_dict = {}

    for word in file.keys():
        def_dict[word] = {}
        def_dict[word]['transcription'] = 'транскрибция'
        for p_s in file[word].keys():
            def_dict[word][p_s] = {}
            for defin in file[word][p_s].keys():
                defin.strip()
                value = file[word][p_s][defin]
                rd = rdl.pop(0)
                def_dict[word][p_s][rd] = value
                

    with open('dict.json', 'w', encoding='UTF-8') as fp:
        json.dump(def_dict, fp, indent=4, ensure_ascii=False)

async def create_words_list():
    with open('new_dictionary.json', 'r', encoding='UTF-8') as d:
        data = json.load(d)
    
    words_l = []

    for word in list(data.keys()):
        words_l.append(word)
    
    with open('words_list.json', 'w', encoding='UTF-8') as wl:
        json.dump(words_l, wl, ensure_ascii=False)

async def add_transcription():
    with open('new_dictionary.json', 'r', encoding='UTF-8') as d:
        data = json.load(d)

    for word in list(data.keys()):
        data[word]['транскрипция'] = 'транскрипция'
    
    with open('new_dictionary.json', 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)


asyncio.run(add_transcription())