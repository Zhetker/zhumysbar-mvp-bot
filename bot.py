import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from rapidfuzz import fuzz

logging.basicConfig(level=logging.INFO)

API_TOKEN = "6098697507:AAE8dXizz_MviFeRwDnyEEFMNNbS1zgUSgE"
CHANNEL_ID = "@zhumys_bar"  # 🔹 замени на username или ID своего канала

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Список ключевых полей вакансии
FIELDS = ["грузчик", "нужен", "требуется", "работа", "склад", "фабрика", "стройка"]
TEMPLATE_HINT = (
    "⚠️ Пожалуйста, оформите вакансию по шаблону:\n\n"
    "📍 Кто нужен\n📅 Когда\n🕗 Время\n💰 Оплата\n📞 Контакт"
)

def check_vacancy(text: str) -> bool:
    text = text.lower()

    # 🔹 1. Проверка на ключевые слова (с опечатками)
    for word in FIELDS:
        if fuzz.partial_ratio(word, text) > 80:
            return True

    # 🔹 2. Проверка на шаблон
    has_person = any(x in text for x in ["грузчик", "водитель", "менеджер", "уборщ"])
    has_date = any(x in text for x in ["сегодня", "завтра", "понедельник", "вторник", "числа"])
    has_time = any(char.isdigit() and ":" in text or "утра" in text or "вечера" in text for char in text)
    has_money = any(x in text for x in ["тг", "₸", "тенге", "сом", "руб", "₽", "usd", "$"])
    has_contact = any(x in text for x in ["870", "+7", "тел", "whatsapp", "ватсап", "tg", "@"])

    checks = [has_person, has_date, has_time, has_money, has_contact]
    return sum(checks) >= 4

@dp.message()
async def process_message(message: types.Message):
    text = message.text or ""
    logging.info(f"Получено сообщение: {text}")

    if check_vacancy(text):
        await message.reply("✅ Ваша вакансия принята. Спасибо!")

        # 🔹 Пересылаем вакансию в канал
        try:
            await bot.send_message(CHANNEL_ID, f"📢 Новая вакансия:\n\n{text}")
            logging.info("Вакансия отправлена в канал")
        except Exception as e:
            logging.error(f"Ошибка при пересылке в канал: {e}")

    else:
        await message.reply(TEMPLATE_HINT)

async def main():
    logging.info("🚀 Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
