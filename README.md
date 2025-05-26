# SafeRenta — Telegram-бот для анализа договоров аренды 🏠

**SafeRenta** — это Telegram-бот, который:
- принимает PDF/DOCX-договор аренды,
- анализирует документ (в режиме mock),
- формирует отчёт в виде PDF с рекомендациями.

🧠 Архитектура:
- Telegram Bot API + Aiogram 3
- Генерация PDF с fpdf2 + DejaVuSans (поддержка emoji)
- Готов к подключению DeepSeek или OpenAI

## 🚀 Быстрый старт

### 1. Клонируйте проект

```bash
git clone https://github.com/ваш_логин/safeRenta-bot.git
cd safeRenta-bot
2. Установите зависимости
bash
Копировать
Редактировать
pip install -r requirements.txt
3. Создайте .env на основе шаблона
bash
Копировать
Редактировать
cp .env.example .env
Добавьте ваш токен Telegram-бота:

env
Копировать
Редактировать
BOT_TOKEN=ваш_токен_бота
DEEPSEEK_API_KEY=не используется (можно оставить пустым)
4. Убедитесь, что файл шрифта есть
Копировать
Редактировать
fonts/DejaVuSans.ttf
Скачать можно отсюда: https://dejavu-fonts.github.io/Download.html

5. Запустите бота
bash
Копировать
Редактировать
python main.py
📦 Структура проекта
bash
Копировать
Редактировать
.
├── main.py
├── fonts/                  # Шрифт для PDF
├── texts/                  # Текстовые шаблоны (о проекте, правила, юрист)
├── .env                    # Токены (не добавлять в Git)
├── .env.example
├── requirements.txt
└── README.md

📄 Лицензия
MIT