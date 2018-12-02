from Yui import Yui
import asyncio
import common.Logger as logger
from common.Store import store
from common.VK.VKLongPoll import VKLongPoll
from utils import load_config

import db.Loader

async def call():
    load_config()
    await db.Loader.load()

    global bot
    bot = Yui()

    bot_longpoll = VKLongPoll(bot)

    current_group_id = await bot_longpoll.request("groups.getById")
    bot_longpoll.group_id = current_group_id.response[0]['id']
    store.config.group_id = current_group_id.response[0]['id']

    await store.call_on_init_handlers()
    logger.Nlog("Приступаю к приёму сообщений!")
    await bot_longpoll.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(call())
    except(KeyboardInterrupt):
        bot.say_goodbye()
        exit()