import asyncio

from demo.bot import Bot
from ownlittleworld.celery import app


@app.task
def run_bot():
    config = {}
    bot = Bot(config)

    asyncio.run(bot.run())
