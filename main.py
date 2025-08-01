import asyncio

from create_bot import bot, dp
from handlers.category import router as categories_router
from handlers.comment import router as comments_router
from handlers.finish import router as finish_router
from handlers.flavor import router as flavors_router
from handlers.rating import router as ratings_router
from handlers.start import router as start_router
from handlers.variant import router as variants_router


def register_routers():
    dp.include_router(start_router)
    dp.include_router(categories_router)
    dp.include_router(variants_router)
    dp.include_router(flavors_router)
    dp.include_router(ratings_router)
    dp.include_router(comments_router)
    dp.include_router(finish_router)


async def start_bot():
    pass


async def main():
    register_routers()
    dp.startup.register(start_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
