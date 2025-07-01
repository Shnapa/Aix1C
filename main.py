import os
import json
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from outlook_reader import get_unread_emails
from google.generativeai.types import content_types

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")

employee_data_path = "testing.xlsx"
df = pd.read_excel(employee_data_path)

table_text = df.to_string(index=False)

emails = get_unread_emails()
results = []

for email in emails:
    full_prompt = f"""
Ти є помічником служби логістики одягу.

Ось службовий лист:
From: {email['from']}
Subject: {email['subject']}
Body:
{email['body']}

Дані про працівників з таблиці:
{table_text}

Проаналізуй лист і таблицю разом, і дай відповідь:
- Що конкретно запитують?
- Чи можна відповісти на це на основі таблиці?
- Якщо так — сформулюй готову відповідь.
- Якщо ні — поясни чому.
"""

    try:
        response = model.generate_content(full_prompt)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Gemini error: {str(e)}"

    results.append({
        "email_data": email,
        "gemini_analysis": reply
    })

with open("gemini_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Аналітика у gemini_results.json")
