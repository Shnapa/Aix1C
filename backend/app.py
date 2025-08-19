import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__, static_folder='../frontend')
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("API ключ не знайдений в .env файлі")

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
        unit_code = unit_data.get("code")

        if not unit_code:
            return jsonify({"error": "Не вказано код одиниці"}), 400
        
        print(f"Отримано код одиниці: {unit_code}")

        prompt = f"Дай, будь ласка, детальний аналіз одиниці з кодом {unit_code}."

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
