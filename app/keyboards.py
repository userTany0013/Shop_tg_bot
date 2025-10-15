from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_category, get_cards


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


async def client_iocation():
    return ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поделиться локацией', request_location=True)]
],
resize_keyboard=True,
input_field_placeholder='Введите адрес'
)



async def catigories():
    keyboard = InlineKeyboardBuilder()
    all_catigories = await get_category()
    for categoru in all_catigories:
        keyboard.add(InlineKeyboardButton(text=categoru.name,
                                           callback_data=f'category_{categoru.id}'))
    return keyboard.adjust(2).as_markup()
    

async def cards(category):
    keyboard = InlineKeyboardBuilder()
    all_cards = await get_cards(category)
    for card in all_cards:
        keyboard.row(InlineKeyboardButton(text=f'{card.name} | {card.price} RUB',
                                           callback_data=f'card_{card.id}'))
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='categories'))
    return keyboard.as_markup()


async def back(cat_id, card_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Купить', callback_data=f'buy_{card_id}')],
        [InlineKeyboardButton(text='Назад', callback_data='categories')]
    ])


async def address(card_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='да', callback_data='yes')],
        [InlineKeyboardButton(text='нет, ввести вручную', callback_data=f'buy_{card_id}')]
    ])


admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='добавить товар'),
     KeyboardButton(text='Изменить товар')],
    [KeyboardButton(text='Данные о товаре'),
     KeyboardButton(text='Данные о клиенте')]
],
resize_keyboard=True,
input_field_placeholder='Выберите пункт меню')


async def category_for_card():
    keyboard = InlineKeyboardBuilder()
    all_catigories = await get_category()
    for categoru in all_catigories:
        keyboard.add(InlineKeyboardButton(text=categoru.name,
                                           callback_data=f'tocardcategory_{categoru.id}'))
    return keyboard.adjust(2).as_markup()


async def confirm():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='да', callback_data='data_yes')],
        [InlineKeyboardButton(text='нет, ввести заново', callback_data='no')],
        [InlineKeyboardButton(text='нет, вернуться в меню', callback_data='back')]
    ])
