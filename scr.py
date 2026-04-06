from aiokafka import AIOKafkaConsumer
import asyncio

async def consume():
    consumer = AIOKafkaConsumer(
        'category.events',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Получено: {msg.value.decode('utf-8')}")
    finally:
        await consumer.stop()

asyncio.run(consume())