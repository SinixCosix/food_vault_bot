import asyncio

from create_bot import bot, dp
from handlers.start import start_router


async def start_bot():
    pass


async def main():
    dp.include_router(start_router)
    dp.startup.register(start_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
