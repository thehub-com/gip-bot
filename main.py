import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username

    # пробуем создать пользователя
    supabase.table("users").upsert({
        "tg_id": tg_id,
        "username": username,
        "gip": 0
    }).execute()

    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton(
            text="🛒 Открыть маркетплейс",
            web_app=types.WebAppInfo(url="https://example.com")  # временно
        )
    )

    await message.answer(
        "👋 Добро пожаловать в **GIP — GOCK Interaction Points**\n\n"
        "💠 Здесь ты сможешь:\n"
        "• зарабатывать GIP\n"
        "• покупать подарки и NFT\n"
        "• оформлять профиль\n\n"
        "👇 Открывай маркет:",
        reply_markup=kb,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
