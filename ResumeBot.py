import asyncio
import logging

from aiogram import Dispatcher
from aiogram.dispatcher.fsm.storage.redis import RedisStorage

from bata import all_data
from handlers import start_hand, testcase_handler, checklist_handler, bugreport_handler

log = logging.getLogger(__name__)
log.addHandler(logging.FileHandler('logfile.log'))


async def main():
    data = all_data()
    bot = data.get_bot()
    storage = RedisStorage.from_url(data.redis_url)
    dp = Dispatcher(storage)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    log.error("Starting bot")

    dp.include_router(start_hand.router)
    dp.include_router(testcase_handler.router)
    dp.include_router(checklist_handler.router)
    dp.include_router(bugreport_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
