from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram import F
from dotenv import load_dotenv
import asyncio
import logging
import os

# Загрузка переменных из .env
load_dotenv()

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Не указан BOT_TOKEN в переменных окружениях")

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в SafeRenta — Telegram-бот для проверки договоров аренды!\n\n"
        "Здесь вы можете:\n"
        "— Загрузить договор и получить автоматический анализ\n"
        "— Получить рекомендации по улучшению условий\n\n"
        "🔎 Введите /проверка для начала или /юрист, чтобы обратиться к специалисту."
    )

# /юрист
@dp.message(Command("юрист"))
async def cmd_lawyer(message: Message):
    await message.answer(
        "👨‍⚖️ Юридическая помощь\n\n"
        "Если вам требуется персональная проверка договора аренды, разбор конкретной ситуации или правовые рекомендации — вы можете обратиться к нашему юристу.\n\n"
        "📌 О специалисте:\n"
        "✔ Опыт более 8 лет в сфере гражданского и жилищного права\n"
        "✔ Практика в работе с договорами аренды, спорами по найму, возвратом депозита\n"
        "✔ Подход на стороне арендатора: выявление рисков, защита интересов\n\n"
        "📩 Контакт: @имя_телеграм_юриста\n\n"
        "⚠️ Услуги юриста оказываются на платной основе по предварительной договорённости."
    )

# /правила
@dp.message(Command("правила"))
async def cmd_legal(message: Message):
    await message.answer(
        "📄 Правила и юридический статус\n\n"
        "Данный Telegram-бот предоставляет только предварительный автоматический анализ договора аренды и проверку объекта по открытым источникам.\n"
        "Все рекомендации носят ознакомительный характер и не являются юридической консультацией.\n\n"
        "Разработчики не несут ответственности за действия пользователей, предпринятые на основании анализа.\n"
        "Рекомендуется обратиться к квалифицированному юристу перед подписанием договора."
    )

# /проверка — начало процесса загрузки договора
@dp.message(Command("проверка"))
async def cmd_check(message: Message):
    await message.answer(
        "📤 Пожалуйста, загрузите ваш договор аренды в формате PDF или DOCX.\n"
        "После загрузки начнётся автоматическая проверка."
    )

# Обработка загруженного файла
@dp.message(F.document)
async def handle_document(message: Message):
    document = message.document
    file_path = f"temp/{document.file_unique_id}_{document.file_name}"

    # Сохраняем файл
    file = await bot.download(document)
    with open(file_path, "wb") as f:
        f.write(file.read())

    await message.answer("✅ Файл получен. Идёт предварительная проверка договора...")

    # 🔧 Заглушка: вместо реального анализа
    await message.answer("📄 Анализ завершён. В будущем здесь появится PDF-отчёт с рекомендациями.")

# Запуск
async def main():
    os.makedirs("temp", exist_ok=True)

    try:
        me = await bot.get_me()
        logging.info(f"🤖 Бот запущен: @{me.username}")
    except Exception as e:
        logging.error(f"❌ Не удалось подключиться к Telegram API: {e}")
        return

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
