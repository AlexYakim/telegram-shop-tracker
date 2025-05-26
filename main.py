import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher


load_dotenv()
TOKEN = getenv("BOT_TOKEN")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")
