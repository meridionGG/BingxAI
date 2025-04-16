import os
import json
from mistralai import Mistral
from test_trade import convert
import time

# Задайте ваш API ключ напрямую (или установите его через переменную окружения)
MISTRAL_API_KEY = ""
model = "mistral-large-latest"

# Инициализация клиента Mistral
client = Mistral(api_key=MISTRAL_API_KEY)


def call_llm(input_text):
    system_prompt = (
        "Вы являетесь торговым сигналом парсера. Преобразуйте входное сообщение в структурированный формат JSON, "
        "содержащий следующие поля: торговая пара, позиция, плечо, % от депозита, точка входа, стоп-лосс, "
        "тейк-профит, время отработки, усреднение позиции, досрочное закрытие. Если какое-либо поле отсутствует, "
        "верните null."
    )
    user_message = f"Входное сообщение: {input_text.strip()}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    # Отправляем запрос к API Mistral
    response = client.chat.complete(
        model=model,
        messages=messages,
        temperature=0.0
    )
    raw_text = response.choices[0].message.content.strip()
    try:
        parsed = json.loads(raw_text)
    except Exception as e:
        print("Ошибка при разборе JSON:", e)
        parsed = raw_text
    return parsed


if __name__ == "__main__":
    text_input = (
        "btc шорт 20х стоп лосс 86000, твх по рынку, "
        "усреднение 10% на 100$, досрочное закрытие по сигналу 'закрываемся', на 100% от депозита"
    )

    structured_signal = call_llm(text_input)
    signal = structured_signal[7:-3]
    print(signal)
    data_dict = json.loads(signal)
    print(type(data_dict))
    convert(data_dict)
    if isinstance(signal, dict):
        print(json.dumps(signal, indent=4, ensure_ascii=False))
    else:
        print(signal)