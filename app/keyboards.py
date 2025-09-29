from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'),
      KeyboardButton(text='Контакты')]
],
resize_keyboard=True,
input_field_placeholder='Выберите пункт меню'
)


async def client_name(name):
    return ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=name)]
],
resize_keyboard=True,
input_field_placeholder='Введите имя'
)


async def client_phone():
    return ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поделиться контактом', request_contact=True)]
],
resize_keyboard=True,
input_field_placeholder='Введите номер'
)
