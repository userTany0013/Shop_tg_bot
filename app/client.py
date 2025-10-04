from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.database.requests import set_user, update_user, get_card


client = Router()


@client.message(CommandStart())
async def start_bot(message: Message, state: FSMContext):
    is_user = await set_user(message.from_user.id)
    if not is_user:
        await message.answer('Welcome in Bot!, Register:',
                             reply_markup=await kb.client_name(message.from_user.first_name))
        await state.set_state('reg_name')
    else:
        await message.answer('Welcome in Bot!', reply_markup=kb.menu)


@client.message(StateFilter('reg_name'))
async def get_reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await state.set_state('reg_phone')
    await message.answer('Введите номер телефона',
                         reply_markup= await kb.client_phone())
    

@client.message(F.contact, StateFilter('reg_phone'))
async def get_reg_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()
    await update_user(message.from_user.id, data['name'], data['phone'])
    await message.answer('Register', reply_markup=kb.menu)
    await state.clear()


@client.message(StateFilter('reg_phone'))
async def get_reg_phone_text(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    await update_user(message.from_user.id, data['name'], data['phone'])
    await message.answer('Register', reply_markup=kb.menu)
    await state.clear()


@client.callback_query(F.data == 'categories')
@client.message(F.text == 'Каталог')
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


@client.message(F.photo)
async def photo_id(message: Message):
    await message.answer(message.photo[-1].file_id)