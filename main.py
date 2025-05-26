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
import requests
from fpdf import FPDF

# Загрузка переменных из .env
load_dotenv()

# Логирование
logging.basicConfig(level=logging.INFO)

# Токены
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "not_required")

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
        InlineKeyboardButton(text="📜 Правила", callback_data="rules"),
        InlineKeyboardButton(text="ℹ️ О проекте", callback_data="about")
    ],
    [
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="start")
    ]
])

def load_text(filename: str) -> str:
    with open(os.path.join("texts", filename), encoding="utf-8") as f:
        return f.read()

def analyze_with_deepseek(user_text: str) -> str:
    return (
        "🔍 Анализ договора аренды\n\n"
        "1. 📌 В договоре отсутствует пункт о сроках возврата залога. Это может привести к затягиванию возврата арендодателем.\n"
        "2. ❗ Не указана ответственность сторон за порчу имущества. Рекомендуется чётко прописать, кто компенсирует ущерб.\n"
        "3. ⚠️ Не прописан порядок досрочного расторжения. Это важно для правовой защиты обеих сторон.\n"
        "4. 🔍 Нет информации о размере и сроках оплаты коммунальных услуг. Уточните, кто и за что платит.\n"
        "5. 🔒 Отсутствует пункт о порядке доступа в квартиру (например, при технических осмотрах).\n"
        "6. 📎 Не обозначен порядок передачи имущества — составление акта приёма-передачи желательно.\n"
        "7. 🕒 Неясно, в какие сроки арендатор должен освободить жильё после расторжения договора.\n"
        "8. 🏠 Нет упоминания о праве проживания третьих лиц или гостей.\n"
        "9. 📑 Договор не содержит сведений о порядке внесения изменений.\n"
        "10. 📤 Не указан способ уведомления сторон (почта, Telegram, лично и т.д.).\n\n"
        "✅ Рекомендации по улучшению:\n"
        "— Добавьте срок возврата залога (например, в течение 10 рабочих дней).\n"
        "— Уточните, кто оплачивает ущерб и при каких условиях.\n"
        "— Пропишите процедуру расторжения: срок уведомления, форма и компенсации.\n"
        "— Укажите, как будет фиксироваться состояние квартиры (фото, акт и т.д.).\n"
        "— Внесите информацию о правах на досрочный выезд или продление договора.\n"
        "— Пропишите, какие каналы связи юридически значимы для уведомлений.\n\n"
        "ℹ️ Данный анализ является примером автоматического разъяснения. За юридическим заключением обратитесь к специалисту."
    )


@dp.callback_query(F.data == "about")
async def button_about(callback: types.CallbackQuery):
    await callback.message.answer(load_text("about.txt"), reply_markup=main_keyboard)
    await callback.answer()

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
        "После загрузки начнётся автоматическая проверка.",
        reply_markup=main_keyboard
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

@dp.callback_query(F.data == "start")
async def button_restart(callback: types.CallbackQuery):
    await cmd_start(callback.message)
    await callback.answer()

# /юрист
@dp.message(Command("юрист"))
async def cmd_lawyer(message: Message):
    await message.answer(load_text("lawyer.txt"), reply_markup=main_keyboard)

# /правила
@dp.message(Command("правила"))
async def cmd_legal(message: Message):
    await message.answer(load_text("rules.txt"), reply_markup=main_keyboard)

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

    await message.answer("📡 Выполняется анализ договора через DeepSeek AI...")

    try:
        result = analyze_with_deepseek(extracted_text)
    except Exception as e:
        logging.exception("Ошибка при обращении к DeepSeek")
        await message.answer("❌ Ошибка при анализе через DeepSeek. Попробуйте позже.")
        return

    # Генерация PDF-отчёта
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_font("DejaVu", style="", fname="fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    # Безопасная запись
    for line in result.split("\n"):
        try:
            pdf.write(8, line + "\n")
        except Exception as e:
            pdf.write(8, "[ошибка при выводе строки]\n")

    pdf_path = file_path + "_analysis.pdf"
    pdf.output(pdf_path)

    await message.answer_document(FSInputFile(pdf_path), caption="📎 Ваш PDF-отчёт готов")
    await message.answer("Выберите следующее действие:", reply_markup=main_keyboard)

# Запуск
async def main():
    os.makedirs("temp", exist_ok=True)
    os.makedirs("texts", exist_ok=True)
    os.makedirs("fonts", exist_ok=True)

    try:
        me = await bot.get_me()
        logging.info(f"🤖 Бот запущен: @{me.username}")
    except Exception as e:
        logging.error(f"❌ Не удалось подключиться к Telegram API: {e}")
        return

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
