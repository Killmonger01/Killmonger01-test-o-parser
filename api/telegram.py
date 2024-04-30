import asyncio

from .constans import bot


def send_telegram_message(products):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_send_telegram_message(products))
    loop.close()


async def async_send_telegram_message(products):
    await bot.send_message(722541015, f'Задача на парсинг товаров с сайта Ozon завершена. Сохранено: {len(products)} товаров')
