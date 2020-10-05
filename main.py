from aiogram import executor, Dispatcher
from handlers import dp
from database import Database
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from price_tracking import PriceTracking

scheduler = AsyncIOScheduler()


async def on_startup(dp: Dispatcher):
    await Database().create_pool()
    scheduler.start()


async def on_shutdown(dp: Dispatcher):
    await Database().pool.close()
    scheduler.shutdown()


scheduler.add_job(PriceTracking().run_update, 'cron', hour=21)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup,
                       on_shutdown=on_shutdown)
