import requests
from bs4 import BeautifulSoup
import json

with open('links.json', 'r', encoding='utf-8') as f:
    links = json.load(f)

counter = 0
dictionary = {}

for link in links:
    # Добавим обработку возможных ошибок HTTP (например, 404, 500)
    try:
        response = requests.get(link, timeout=10) # Добавлен timeout для надежности
        response.raise_for_status() # Вызывает HTTPError для плохих статусов (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе {link}: {e}")
        continue # Переходим к следующей ссылке

    # Если статус 200 (OK), продолжаем парсинг
    soup = BeautifulSoup(response.text, 'html.parser')
    
    h1 = soup.find('h1')
    if not h1:
        print(f"Пропускаем {link}: не найден h1")
        continue
    word = h1.get_text(strip=True)
    dictionary[word] = {}

    # --- Место, где у вас ошибка: Убедитесь, что здесь есть проверка! ---
    defdiv = soup.find('div', class_='t_inline_en')
    if not defdiv: # <--- ЭТА ПРОВЕРКА КРИТИЧНА!
        print(f"Пропускаем {link} (слово '{word}'): не найден основной перевод div")
        continue # Если основной перевод не найден, нет смысла продолжать для этого слова
    defin = defdiv.get_text(strip=True) # Добавлено strip=True для чистоты
    dictionary[word][defin] = {}
    # -------------------------------------------------------------------

    # Находим все части речи (h4)
    parts_of_speech = soup.find_all('h4', class_='pos_item_link')
    for h4 in parts_of_speech:
        ps = h4.get_text(separator=';', strip=True)
        # Убедитесь, что 'defin' ключ существует перед попыткой добавить в него 'ps'
        # Это также подразумевает, что 'word' ключ существует
        if word not in dictionary:
            dictionary[word] = {defin: {}}
        elif defin not in dictionary[word]:
            dictionary[word][defin] = {}
        dictionary[word][defin][ps] = []

        # Ищем контейнер с примерами, который идет СРАЗУ ПОСЛЕ h4
        examples_container = h4.find_next_sibling('div', class_='tr')
        
        if examples_container:
            # Находим ВСЕ блоки с примерами внутри этого контейнера
            example_blocks = examples_container.find_all('div', class_='ex')
            
            all_examples_for_pos = []
            for text_block in example_blocks:
                tp = text_block.get_text(separator='?', strip=True)
                elems = tp.split('?')
                
                i = 0
                # Используем безопасный цикл
                while i + 1 < len(elems) and len(all_examples_for_pos) < 3: # Добавлено ограничение на 3 примера
                    eng_part = elems[i].strip()
                    # Проверяем, есть ли тире и следующий элемент для русского перевода
                    rus_part = ""
                    if i + 1 < len(elems) and elems[i+1].strip() == '—':
                         if i + 2 < len(elems):
                            rus_part = elems[i+2].strip()
                            i += 3 # Пропускаем Eng, '—', Rus
                         else: # Если тире есть, но русского перевода нет, берем следующий как русский
                             rus_part = elems[i+1].strip()
                             i += 2 # Пропускаем Eng, Rus
                    else: # Если тире нет, следующий элемент - сразу русский
                        rus_part = elems[i+1].strip()
                        i += 2 # Пропускаем Eng, Rus
                    
                    example = f"{eng_part} — {rus_part}" if rus_part else eng_part
                    all_examples_for_pos.append(example)
                    
                    # Проверяем, нужно ли остановить цикл, если уже набрали 3 примера
                    if len(all_examples_for_pos) >= 3:
                        break
            
            # Обновляем словарь только если есть defin и ps
            if word in dictionary and defin in dictionary[word] and ps in dictionary[word][defin]:
                dictionary[word][defin][ps] = all_examples_for_pos

    counter += 1
    print(f"{counter}: Обработана ссылка {link}")

with open('new_dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=4)

print("Готово!")