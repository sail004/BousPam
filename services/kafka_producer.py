from fastapi import FastAPI
from pydantic import BaseModel
from confluent_kafka import Producer
import json
import asyncio

app = FastAPI()

# Конфигурация Kafka Producer
conf = {
    'bootstrap.servers': 'localhost:9092',  # Адрес Kafka-брокера
}

producer = Producer(**conf)


class Message(BaseModel):
    topic: str
    key: str | None = None
    value: dict  # Тело сообщения


@app.post("/send-message/")
async def send_message(message: Message):
    # Сериализация данных в JSON (или любой другой формат)
    value = json.dumps(message.value).encode('utf-8')

    # Отправка сообщения в Kafka
    producer.produce(
        topic=message.topic,
        key=message.key,
        value=value,
        callback=lambda err, msg: print(f"Сообщение отправлено: {msg}") if not err else print(f"Ошибка: {err}")
    )

    # Ожидание доставки
    producer.flush()

    return {"status": "Сообщение отправлено в Kafka"}
