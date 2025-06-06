from fastapi import FastAPI
from confluent_kafka import Consumer, KafkaException
import json
import threading
import asyncio

app = FastAPI()

# Конфигурация Kafka Consumer
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'fastapi-group',
    'auto.offset.reset': 'earliest',  # Читать с начала
}

consumer = Consumer(**conf)
consumer.subscribe(['test_topic'])  # Подписываемся на топик

def consume_messages():
    while True:
        msg = consumer.poll(1.0)  # Таймаут 1 сек
        if msg is None:
            continue
        if msg.error():
            print(f"Ошибка: {msg.error()}")
        else:
            value = json.loads(msg.value().decode('utf-8'))
            print(f"Получено сообщение: {value}")

# Запуск потребителя в отдельном потоке
thread = threading.Thread(target=consume_messages, daemon=True)
thread.start()

@app.get("/")
async def root():
    return {"message": "Consumer работает в фоне"}
