import dotenv
import os
from openai import OpenAI


class DeepSeekAPI:
    def __init__(self):
        dotenv.load_dotenv()
        self.API = os.getenv("API")
        self.api = OpenAI(api_key=self.API, base_url="https://api.deepseek.com")
        print(self.API)

    def first_ai(self, content):
        self.response = self.api.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
            "role": "user",
            "content": content
            }
        ],
        max_tokens=2048,
        temperature=1.3,
        stream=False
        )
        self.formated_response = self.response.choices[0].message.content.split(sep=";")

        #перевод пердложения
        self.r_sentance = self.formated_response[0]
        
        #ошибки
        faults = self.formated_response[1]
        response = {'translation': self.r_sentance, 'faults' : faults}
        return response

#главная управлялка для первого английского сообщения
    def en_first(self, sentance):
        content = f"Вот предложение на английском: {sentance}. Пожалуйста проверь это предложение на грамотность и ошибки. И переведи его на русский. Ответ напиши вот в таком формате: 'перевод;ошибки(если они есть и какие они прям напиши ; как знак разделитель между переводом и ошибками. Если нет ошибок то так и напиши - ошибок нет). Никаких дополнительных слов не надо просто перевод и ошибки если они есть.'"
        response = self.first_ai(content)
        print(response)
        return response

#главная функция для первого французского сообщения
    def fr_first(self, sentance):
        content = f"Вот предложение на французском: {sentance}. Пожалуйста проверь это предложение на грамотность и ошибки. И переведи его на русский. Ответ напиши вот в таком формате: 'перевод;ошибки(если они есть и какие они прям напиши ; как знак разделитель между переводом и ошибками. Если нет ошибок то так и напиши - ошибок нет). Никаких дополнительных слов не надо просто перевод и ошибки если они есть.'"
        response = self.first_ai(content)
        return response

    def help_to_write(self, content):
        response = self.api.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
            "role": "user",
            "content": content,
            }
        ],
        max_tokens=1024,
        temperature=1.3,
        stream=False
        )
        return response.choices[0].message.content
    
    #управлялка для помощи с правильным написанием английский(3 вариант выбора)
    def en_help_to_write(self, r_var_sent):
        content = f"Вот предложение на русском: {r_var_sent}. Пожалуйста переведи его на английский язык грамотно. В ответе напиши просто перевод без лишних слов."
        return self.help_to_write(content)
    
    #управлялка для помощи с правильным написанием французский(3 вариант выбора)
    def fr_help_to_write(self, r_var_sent):
        content = f"Вот предложение на русском: {r_var_sent}. Пожалуйста переведи его на французский язык грамотно. В ответе напиши просто перевод без лишних слов."
        return self.help_to_write(content)
    
    def come_up_with_sentence(self, word):
        content = f'Привет! Придумай пожалуйста предложение на английском языке. В этом предложении обязательно должно быть это слово - {word}. А также ты можешь использовать любые из слов которые соответствуют уровню А1, предложения должны быть небольшими. В ответе напиши только это предложение.'
        response = self.api.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
            "role": "user",
            "content": content,
            }
        ],
        max_tokens=1024,
        temperature=1.3,
        stream=False
        )
        return response.choices[0].message.content
    
    def check_interm(self, user_input, ai_sent):
        content = f'Пользователю были даны слова и он должен был составить вот такое предложение - {ai_sent}. Вот как пользователь составил предложение и потом перевел его на русский: {user_input}. Проверь грамматическую правильность предложения и то привильно ли это переведено на русский. В ответе просто напиши есть ли ошибки и если да то какие'
        response = self.api.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
            "role": "user",
            "content": content,
            }
        ],
        max_tokens=1024,
        temperature=1.3,
        stream=False
        )
        unformated = response.choices[0].message.content
        format = unformated.replace('*', '')
        formated = format.replace('#', '')
        return formated