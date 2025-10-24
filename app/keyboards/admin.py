from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.admin import get_category, get_cards


admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='добавить товар')],
    [KeyboardButton(text='Данные о товаре')]
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


async def catigories_all_cards():
    keyboard = InlineKeyboardBuilder()
    all_catigories = await get_category()
    for categoru in all_catigories:
        keyboard.add(InlineKeyboardButton(text=categoru.name,
                                           callback_data=f'allcategory_{categoru.id}'))
    return keyboard.adjust(2).as_markup()


async def cards_all(category):
    keyboard = InlineKeyboardBuilder()
    all_cards = await get_cards(category)
    for card in all_cards:
        keyboard.row(InlineKeyboardButton(text=f'{card.name} | {card.price} RUB',
                                           callback_data=f'allcard_{card.id}'))
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='all_categories'))
    return keyboard.as_markup()
