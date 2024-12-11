import os
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI

# Не забываем указать ключ к апи
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
Settings.llm = OpenAI(model="gpt-4o-mini")

# Создаем объект для работы с PDF
reader = SimpleDirectoryReader(input_dir='./data/')

# Загружаем наши документы
docs = reader.load_data()
print(f'Loaded {len(docs)} docs')