from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os
import uuid

load_dotenv()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # render_template - визуальный шаблон


# code
@app.route('/', methods=['POST'])
def index_post():

    # Чтение значения из формы
    original_text = request.form['text']
    target_language = request.form['language']

    # Загрузка значения из файла.env

    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Указываем, что хотим перевести и API
    # версия (3.0) и целевой язык
    path = '/translate?api-version=3.0'

    # Добавляем параметр целевого языка
    target_language_parameter = '&to=' + target_language

    # Создаём полный URL
    constructed_url = endpoint + path + target_language_parameter

    # Настроем информацию заголовка, которая включает наши ключи подписки
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Создаем тело запроса с текстом, который будет переведён
    body = [{'text': original_text}]

    # делаем запрос, исмользующий метод пост
    translator_request = requests.post(
        constructed_url, headers=headers, json=body)

    # Получаем ответ от json
    translator_response = translator_request.json()

    #Получаем перевод
    translated_text = translator_response[0]['translations'][0]['text']

    # Вызываем шаблон рендера, передав ему переведённый текст
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )


