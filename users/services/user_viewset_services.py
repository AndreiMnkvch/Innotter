import json
import os
from dotenv import load_dotenv

load_dotenv()

import pika
from django.db.models import QuerySet, Count, Subquery
from rest_framework.request import Request

from core.models import Post
from users.models import User


def block_all_user_pages(pages: QuerySet) -> None:
    pages.update(is_blocked_forever=True)

def unblock_all_user_pages(pages: QuerySet) -> None:
    pages.update(is_blocked_forever=False)

def check_to_block_pages(request: Request) -> bool:
    return request.data.get("is_blocked")

def block_user_pages_service(user: User, request: Request) -> None:
    if "is_blocked" in request.data.keys():
        pages = user.pages.all()
        if check_to_block_pages(request):
            block_all_user_pages(pages)
        else:
            unblock_all_user_pages(pages)


def statistics_service(user):

    posts_count = user.pages.aggregate(Count('posts'))
    followers_count = user.pages.aggregate(Count('followers'))
    pages = user.pages.all()
    likes_count = Post.objects.filter(page__in=pages).aggregate(Count('likes'))
    stats = {"posts_count": posts_count, "followers_count": followers_count, "likes_count": likes_count}

    print('stats to be sent: ', stats)


    connection = pika.BlockingConnection(parameters=pika.URLParameters(os.getenv('RABBITMQ_BROKER_URL')))
    print('connection: ', connection)
    channel = connection.channel()
    channel.queue_declare(queue='statistics_publish', durable=True)
    print('channel', channel)
    channel.basic_publish(exchange='',
                          body=json.dumps(stats),
                          routing_key='statistics_publish',
                          properties=pika.BasicProperties(
                              delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                          ))
    print('msg published!!!')
    connection.close()