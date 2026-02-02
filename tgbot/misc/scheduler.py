import logging
from datetime import datetime, timedelta

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def send_reminder_message(bot:Bot, days:int, user_id):
    if days == 14:
        text = f"Напоминаю, что через 2 недели у вас запланировано обучение Трансцендентальной Медитации"
    elif days == 7:
        text = f"Напоминаю, что через 1 неделю у вас запланировано обучение Трансцендентальной Медитации"

    else:
        text = f"Напоминаю, завтра у вас запланировано обучение Трансцендентальной Медитации"

    await bot.send_message(user_id,
                           text)

async def schedule_reminder_message(scheduler:AsyncIOScheduler, user_id, date, bot:Bot):
    two_weeks = date - timedelta(days=14)
    week = date - timedelta(days=7)
    day = date - timedelta(days=1)
    test = datetime.now() + timedelta(seconds=40)
    scheduler.add_job(
        send_reminder_message,
        trigger='date',
        args=(bot, 14, user_id),
        next_run_time=two_weeks,
        misfire_grace_time=30
    )

    scheduler.add_job(
        send_reminder_message,
        trigger='date',
        args=(bot, 7, user_id),
        next_run_time=week,
        misfire_grace_time=30

    )

    scheduler.add_job(
        send_reminder_message,
        trigger='date',
        args=(bot, 1, user_id),
        next_run_time=day,
        misfire_grace_time=30
    )

    # scheduler.add_job(
    #     send_reminder_message,
    #     trigger='date',
    #     args=(bot, 1, user_id),
    #     next_run_time=test
    # )


async def scheduler_for_all_users(all_data, scheduler, bot):
    for record in all_data:
        if record['Дата Обучения']:
            date = datetime.strptime(record['Дата Обучения'], "%d.%m.%Y").date()
            user_id = record['telegram_id']
            await schedule_reminder_message(scheduler, user_id, date, bot)

