import asyncio
from typing import Dict, Any

from django.conf import settings

from demo.bot import Bot
from ownlittleworld.celery import app


@app.task
def run_bot(config: Dict[str, Any]):
    config['base_url'] = settings.SITE_URL
    bot = Bot(config)

    asyncio.run(bot.run())
