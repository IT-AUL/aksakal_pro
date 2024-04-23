from openai import OpenAI
from config import API_KEY

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1")


def ask_question(question):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system",
             "content": "Ты стражник, из средневековой Казани. Отвечай только на русском."
                        "Ты будешь отвечать на вопросы странника, который спрашивает тебя о Казани."
                        "Говори кратко, информативно и в духе средневековья."
                        "На грубые вопросы отвечай грубо."
                        "На вопросы не относящиеся к Казани не отвечай."
                        "Если тебе будут задавать вопросы не на русском или татарском, говори, что не понимаешь."},
            {"role": "user", "content": question},
        ]
    )
    return response.choices[0].message.content
