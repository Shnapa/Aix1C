import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import openai
from requests.auth import HTTPBasicAuth

load_dotenv()

app = Flask(__name__, static_folder='../frontend')
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("API ключ не знайдений в .env файлі")

UNIT_API_URL = "http://213.169.83.165/spezod/hs/UnitAPI/GetUnitInfo"
UNIT_API_USER = os.getenv("UNIT_API_USER", "obmen")
UNIT_API_PASS = os.getenv("UNIT_API_PASS", "obmen")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(app.static_folder, path)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        unit_data = request.get_json()
        unit_code = str(unit_data.get("code")).strip()

        if not unit_code:
            return jsonify({"error": "Не вказано код одиниці"}), 400
        
        print(f"Отримано код одиниці: {unit_code}")

        external_api_url = f"{UNIT_API_URL}/{unit_code}"

        print(f"Запит до зовнішнього API: {external_api_url}")

        external_response = requests.get(external_api_url, auth=HTTPBasicAuth(UNIT_API_USER, UNIT_API_PASS))

        print(f"Статус код відповіді зовнішнього API: {external_response.status_code}")
        print(f"Тіло відповіді: {external_response.text}")

        if external_response.status_code != 200:
            return jsonify({"error": "Не вдалося отримати інформацію з зовнішнього API"}), 500

        try:
            unit_info = external_response.json()
            print(f"Інформація про одиницю: {unit_info}")
        except Exception as e:
            print(f"Помилка при перетворенні відповіді на JSON: {e}")
            return jsonify({"error": "Помилка при перетворенні відповіді на JSON"}), 500

        if 'error' in unit_info and unit_info['error'] == 'Not found':
            return jsonify({"error": "Одиницю не знайдено"}), 404

        prompt = f"""
                Проаналізуй наступну одиницю товару та надай чітку та структуровану інформацію. Ось її характеристики: {unit_info}.

                1. Опиши загальну інформацію про товар, включаючи:
                - Імена людей кому вона належить і належала.
                - Модель товару (назва, кольори, розміри).
                - Тривалість використання, чи перебував товар в оренді, та скільки часу він не зберігався.
                - Кількість обслуговувань товару.
                - Статус товару (зберігання, обслуговування тощо)

                2. Оціни фінансові аспекти:
                - Вартість товару за цінником.
                - Вартість компенсації та викупу, та їх відсоткове співвідношення до вартості товару.

                3. Проаналізуй інформацію з документації:
                - Які основні події у житті товару (передача в оренду, повернення, обслуговування)?
                - За яким договором і кому належить товар?

                4. Дай рекомендації щодо стану товару та подальших дій:
                - Оцінка стану товару після використання.
                - Чи є підстави для викупу товару або продовження оренди?

                Надай чітку і структуровану відповідь.
                """


        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=600
        )

        reply = response['choices'][0]['message']['content'].strip()
        print(f"Відповідь GPT: {reply}")

        return jsonify({"result": reply})

    except Exception as e:
        print(f"Виникла помилка: {str(e)}")
        return jsonify({"error": f"Виникла помилка: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
