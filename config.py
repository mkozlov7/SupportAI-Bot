import os
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Конфігурація
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Токен бота
GROUP_ID = os.getenv('GROUP_ID')  # ID групи, якщо потрібно
openai_api_key = os.getenv('OPENAI_API_KEY')