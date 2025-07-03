import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Ініціалізація клієнта OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

        print("Отримано код одиниці:", unit_code)

        prompt = f"Дай детальний аналіз одиниці з кодом {unit_code}."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти експерт з аналізу виробничих одиниць."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=600
        )

        reply = response.choices[0].message.content
        print("Відповідь GPT:", reply)

        return jsonify({"result": reply})

    except Exception as e:
        print("Виняток:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
