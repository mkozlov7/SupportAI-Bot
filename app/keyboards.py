from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup (keyboard=[
    [KeyboardButton(text='Запит до бази знань')],
    [KeyboardButton(text='Залишити заявку по функціоналу SWE'),KeyboardButton(text='Контакти')]
],
            #resize_keyboard=True,
            input_field_placeholder='Що будемо робити?')

knoKnowledgebase = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Повернутися в головне меню')]])
                                       
