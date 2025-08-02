import json
from datetime import datetime, timedelta

import aio_pika

from ..auth_middleware import get_user_primary_email
from ..settings import settings
from .manager import scheduler


async def send_task_to_rabbitmq(task_data: dict):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue('notifier', durable=True)
    message = aio_pika.Message(body=json.dumps(task_data).encode())
    await channel.default_exchange.publish(message, routing_key=queue.name)
    await connection.close()


async def schedule_notification(
    task_title: str, due_date: datetime, notify_at: timedelta, user_id: str
):
    run_time = due_date - notify_at

    user_email = await get_user_primary_email(user_id=user_id)

    scheduler.add_job(
        send_notification_job,
        trigger='date',
        run_date=run_time,
        args=[task_title, notify_at, user_email],
        replace_existing=True,
    )


async def send_notification_job(
    task_title: str, notify_at: timedelta, user_email: str
):
    await send_task_to_rabbitmq({
        'title': f'{task_title}',
        'email': f'{user_email}',
        'notify_at': f'{notify_at}',
    })
