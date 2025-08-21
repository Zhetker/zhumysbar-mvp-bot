import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("❌ Токен бота не найден! Добавь его в .env или переменные окружения.")

# Логирование
logging.basicConfig(level=logging.INFO)
logging.info("🚀 Бот запускается...")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Ключевые слова для проверки вакансий
KEYWORDS = ["вакансия", "нужен", "требуется", "работа", "грузчик", "склад", "фабрика", "стройка"]

@dp.message_handler(content_types=types.ContentType.TEXT)
async def check_message(message: types.Message):
    text = message.text.lower()

    if any(word in text for word in KEYWORDS):
        await message.reply("✅ Ваша вакансия принята. Спасибо!")
    else:
        await message.reply(
            "⚠️ Пожалуйста, оформите вакансию по шаблону:\n\n"
            "📍 Кто нужен\n📅 Когда\n🕗 Время\n💰 Оплата\n📞 Контакт"
        )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
