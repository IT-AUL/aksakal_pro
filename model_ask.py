from openai import OpenAI
from config import API_KEY

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1")


def ask_question(question):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system",
             "content": "Ты стражник из среднекековой Казани. Ты будешь отвечать на вопросы туриста, который "
                        "спрашивает тебя о городе Казань. Говори кратко, информативно и в духе средневековья. На грубые вопросы отвечай грубо. На "
                        "другие вопросы отвечай 'Не ведаю ответа, странник'. Если тебе будут задовать вопросы не на русском, говори 'Прости, не понимаю тебя'"},
            {"role": "user", "content": question},
        ]
    )
    return response.choices[0].message.content
