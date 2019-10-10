import asyncio
from typing import Dict, Any

from django.conf import settings

from demo.bot import Bot
from ownlittleworld.celery import app


@app.task
def run_bot(config: Dict[str, Any]):
    config['base_url'] = settings.SITE_URL
    bot = Bot(config)

    # safe because asyncio.run calls `new_event_loop`
    # we only need to remember to explicitly pass event loop using `get_running_loop`
    asyncio.run(bot.run())
