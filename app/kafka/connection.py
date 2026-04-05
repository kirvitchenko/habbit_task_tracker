from aiokafka import AIOKafkaProducer

from app.core.config import KAFKA_HOST, KAFKA_PORT


async def create_kafka_connection() -> AIOKafkaProducer:
    kafka = AIOKafkaProducer(bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}")
    await kafka.start()
    return kafka


async def close_kafka_client(kafka: AIOKafkaProducer):
    await kafka.stop()
