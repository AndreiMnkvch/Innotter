import pika
from dotenv import load_dotenv


def publish(message, routing_key) -> None:

    parameters = pika.URLParameters('amqp://rabbitmq:rabbitmq@rabbitmq:5672')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(
        exchange='topic', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange="topic",
        routing_key=routing_key,
        body=str(message),
        properties=pika.BasicProperties(
            content_type='text/plain',
            delivery_mode=pika.DeliveryMode.Transient
        )
    )
    connection.close()
