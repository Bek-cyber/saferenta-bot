from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram import F
from dotenv import load_dotenv
import asyncio
import logging
import os
import docx2txt
import fitz  # PyMuPDF
from fpdf import FPDF

# Загрузка переменных из .env
load_dotenv()

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Не указан BOT_TOKEN в переменных окружениях")

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню с кнопками
main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚀 Проверка", callback_data="check"),
        InlineKeyboardButton(text="👨‍⚖️ Юрист", callback_data="lawyer")
    ],
    [
        InlineKeyboardButton(text="📜 Правила", callback_data="rules")
    ]
])

# /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в SafeRenta — Telegram-бот для проверки договоров аренды!\n\n"
        "Здесь вы можете:\n"
        "— Загрузить договор и получить автоматический анализ\n"
        "— Получить рекомендации по улучшению условий\n"
        "— Ознакомиться с юридическим статусом сервиса\n\n"
        "Выберите действие:",
        reply_markup=main_keyboard
    )

# Обработка нажатий на кнопки
@dp.callback_query(F.data == "check")
async def button_check(callback: types.CallbackQuery):
    await callback.message.answer(
        "📤 Пожалуйста, загрузите ваш договор аренды в формате PDF или DOCX.\n"
        "После загрузки начнётся автоматическая проверка."
    )
    await callback.answer()

@dp.callback_query(F.data == "lawyer")
async def button_lawyer(callback: types.CallbackQuery):
    await cmd_lawyer(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "rules")
async def button_rules(callback: types.CallbackQuery):
    await cmd_legal(callback.message)
    await callback.answer()

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

# Обработка загруженного файла
@dp.message(F.document)
async def handle_document(message: Message):
    document = message.document
    file_path = f"temp/{document.file_unique_id}_{document.file_name}"

    # Сохраняем файл
    file = await bot.download(document)
    with open(file_path, "wb") as f:
        f.write(file.read())

    await message.answer("✅ Файл получен. Извлекаем текст договора...")

    extracted_text = ""
    if file_path.lower().endswith(".docx"):
        extracted_text = docx2txt.process(file_path)
    elif file_path.lower().endswith(".pdf"):
        with fitz.open(file_path) as doc:
            for page in doc:
                extracted_text += page.get_text()
    else:
        await message.answer("❌ Неподдерживаемый формат файла. Пожалуйста, загрузите PDF или DOCX.")
        return

    await message.answer("📡 Выполняется тестовый анализ договора (mock)...")

    result = (
        "🔍 Анализ договора (тестовый режим):\n\n"
        "— Не указана ответственность сторон при порче имущества.\n"
        "— Нет пункта о сроках возврата залога.\n"
        "— Рекомендуется добавить раздел об оплате коммунальных услуг.\n\n"
        "✅ Общая структура договора корректна, но требует уточнений."
    )

    # Генерация PDF-отчёта
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in result.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf_path = file_path + "_analysis.pdf"
    pdf.output(pdf_path)

    await message.answer_document(FSInputFile(pdf_path), caption="📎 Ваш PDF-отчёт готов")

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
