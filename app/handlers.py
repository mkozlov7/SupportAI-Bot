from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.chat_action import ChatActionSender

import os
import openai
import logging
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.openai import OpenAI

# Завантаження API ключа OpenAI
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')
Settings.llm = OpenAI(model="gpt-4o-mini")

import app.keyboards as kb

router = Router()

# FSM (Finite State Machine) для керування станами
class KnowledgeBaseState(StatesGroup):
    waiting_for_question = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAOXZznjmyOfujf4QWbB4Z0wjSHF4pUAAh4LAAIX9rFLa-mlP7CO5uk2BA')
    await message.answer(f'{message.from_user.first_name}, привіт. Я віртуальний помічник по документації SalesWorks',
                         reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Тут може бути якийсь help')

@router.message(Command('adminpanel'))
async def adminpanel(message: Message):
    await message.answer('Тут може бути панель адміністратора для налаштувань бота')

@router.message(F.text == 'Запит до бази знань')
async def knowledge_base_start(message: Message, state: FSMContext):
    await message.answer("Напишіть ваше питання:",
                         reply_markup=kb.knoKnowledgebase)
    await state.set_state(KnowledgeBaseState.waiting_for_question)

@router.message(KnowledgeBaseState.waiting_for_question)
async def knowledge_base_process_question(message: Message, state: FSMContext):
    if message.text == 'Повернутися в головне меню':
        await message.answer("Ви повернулися в головне меню.", reply_markup=kb.main)
        await state.clear()
        return
    try:
        # Текст запиту від користувача
        user_query = message.text

        # Додавання технічного повідомлення
        technical_message = (
            "Ти - інтелектуальний помічник, який допомагає працівникам SoftServe Business Systems " 
                "працювати зі специфікаціями імпорту-експорту. "
            "Дай відповідь на наступне запитання, використовуючи лише дані, наведені в джерелах нижче. " 
            "Для табличної інформації поверни її у вигляді html-таблиці. Не повертай у форматі markdown. "
            "Якщо ти не можеш відповісти, використовуючи наведені нижче джерела, скажи, що не знаєш. "
            "Відповідь має бути такою мовою, якою було задане питання."
                )
        
        # Об'єднання технічного повідомлення із запитом
        combined_query = f"{technical_message}\n\n{user_query}"

        # Завантаження індексу LLamaIndex
        storage_context = StorageContext.from_defaults(persist_dir='./storage')
        index = load_index_from_storage(storage_context)
        query_engine = index.as_query_engine()

        # Відображення статусу "друкує"
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        # Запит до LLamaIndex
            response = query_engine.query(user_query)

        # Відповідь користувачеві
        reply_text = f"Ось, що я знайшов:\n{response}"
        await message.reply(reply_text)
        
        # Пересилання відповіді у групу
        group_id = os.getenv('GROUP_ID')  # ID групи
        # Forward запиту користувача до групи
        forwarded_message = await message.forward(chat_id=group_id)

                # Відправка відповіді у вигляді reply_message в групі
        await message.bot.send_message(
            chat_id=group_id,
         #   text=f"Користувач запитав: {message.text}\n\n{reply_text}"
            text=reply_text,
            reply_to_message_id=forwarded_message.message_id  # Робимо відповідь на переслане повідомлення
        )

    except Exception as e:
        # Повідомлення про помилку
        await message.answer(f"Виникла помилка: {str(e)}")
  #  finally:
   #     await state.clear()  # Скидаємо стан  


@router.message()
async def answer(message: types.Message):
    await message.reply('Я ще не розумію цю команду. Спробуй Запит до бази знань')        