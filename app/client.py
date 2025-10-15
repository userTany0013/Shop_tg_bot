from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.database.requests import set_user, update_user, get_card, get_user

import ssl
import certifi
from geopy.geocoders import Nominatim


client = Router()

stx = ssl.create_default_context(cafile=certifi.where())
geolocator = Nominatim(user_agent='TGbot_for_shop', ssl_context=stx)


@client.message(F.chat.id != -1002980866420, CommandStart())
async def start_bot(message: Message, state: FSMContext):
    is_user = await set_user(message.from_user.id)
    if not is_user:
        await message.answer('Welcome in Bot!, Register:',
                             reply_markup=await kb.client_name(message.from_user.first_name))
        await state.set_state('reg_name')
    else:
        await message.answer('Welcome in Bot!', reply_markup=kb.menu)


@client.message(F.chat.id != -1002980866420, StateFilter('reg_name'))
async def get_reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await state.set_state('reg_phone')
    await message.answer('Введите номер телефона',
                         reply_markup= await kb.client_phone())
    

@client.message(F.chat.id != -1002980866420, F.contact, StateFilter('reg_phone'))
async def get_reg_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()
    await update_user(message.from_user.id, data['name'], data['phone'])
    await message.answer('Register', reply_markup=kb.menu)
    await state.clear()


@client.message(F.chat.id != -1002980866420, StateFilter('reg_phone'))
async def get_reg_phone_text(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    await update_user(message.from_user.id, data['name'], data['phone'])
    await message.answer('Register', reply_markup=kb.menu)
    await state.clear()


@client.callback_query(F.data == 'categories')
@client.message(F.chat.id != -1002980866420, F.text == 'Каталог')
async def catalog(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await event.answer(text='Выберите катигорию:', reply_markup=await kb.catigories())
    else:
        await event.answer(text='Вы вернулись')
        await event.message.delete()
        await event.message.answer(text='Выберите катигорию:',
                                     reply_markup=await kb.catigories())


@client.callback_query(F.data.startswith('category_'))
async def cards(callback: CallbackQuery):
    await callback.answer()
    cat_id = callback.data.split('_')[1]
    await callback.message.edit_text('Выберите товар', reply_markup= await kb.cards(cat_id))


@client.callback_query(F.data.startswith('card_'))
async def cards_info(callback: CallbackQuery):
    await callback.answer()
    card_id = callback.data.split('_')[1]
    card = await get_card(card_id)
    await callback.message.delete()
    await callback.message.answer_photo(photo=card.image,
                             caption=f'{card.name}\n\n{card.description}\n\n{card.price} RUB',
                             reply_markup= await kb.back(card.category_id, card.id))


@client.callback_query(F.data.startswith('buy_'))
async def cards_info(callback: CallbackQuery, state: FSMContext):
    card_id = callback.data.split('_')[1]
    await callback.answer()
    await state.set_state('address')
    await state.update_data(card_id=card_id)
    await callback.message.answer('Введите адрес', reply_markup=await kb.client_iocation())


@client.message(F.chat.id != -1002980866420, F.location, StateFilter('address'))
async def location(message: Message, state: FSMContext):
    username = message.from_user.username
    user = await get_user(message.from_user.id)
    await state.update_data(user=user, username=username)
    data = await state.get_data()
    try:
        address = geolocator.reverse(f'{message.location.latitude}, {message.location.longitude}',
                                    exactly_one=True, language='ru', addressdetails=True)
        await state.update_data(address=address)
        card_id = data.get('card_id')
        await message.answer(f'Адрес верный?:\n{address}', reply_markup= await kb.address(card_id))
    except:
        await message.answer('Данные не отправленыб попробуйте еще раз', reply_markup=await kb.client_iocation())


@client.callback_query(F.data == 'yes')
async def sending(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    full_info = (f'{data['user'].name}\n{data['username']}\n{data['user'].tg_id}\n{data['user'].phone_number}\n{data['address']}\n{data['card_id']}')
    await callback.message.bot.send_message(-1002980866420, full_info)
    await callback.message.answer('Заказ принят', reply_markup=kb.menu)
    await state.clear()


@client.message(StateFilter('address'))
async def location(message: Message, state: FSMContext):
    data = await state.get_data()
    address = message.text
    user = await get_user(message.from_user.id)
    card_id = data.get('card_id')
    full_info = f'{user.name}\n{message.from_user.username}\n{user.tg_id}\n{user.phone_number}\n{address}\n{card_id}'
    await message.bot.send_message(-1002980866420, text=full_info)
    await message.answer('Заказ принят', reply_markup=kb.menu)
    await state.clear()
