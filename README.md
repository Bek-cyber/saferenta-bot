# SafeRenta — Telegram-бот для проверки договоров аренды

## 🚀 Быстрый старт

### 1. Клонируй репозиторий и перейди в папку:

```bash
git clone <repo-url>
cd saferenta-bot

2. Создай и активируй виртуальное окружение:
bash
Копировать
Редактировать
python3 -m venv venv
source venv/bin/activate
3. Установи зависимости:
bash
Копировать
Редактировать
pip install -r requirements.txt
4. Укажи токен Telegram-бота:
Создай файл .env и добавь:

ini
Копировать
Редактировать
BOT_TOKEN=your-telegram-bot-token
Или экспортируй переменную вручную:

bash
Копировать
Редактировать
export BOT_TOKEN=your-telegram-bot-token
5. Запусти бота:
bash
Копировать
Редактировать
python main.py

📦 Стек
Python 3.8+

Aiogram 3.x

Telegram Bot API

🛡️ Дисклеймер
Бот предоставляет только автоматизированный предварительный анализ. Не является юридической консультацией. За действия, предпринятые пользователем, ответственность не несут авторы.