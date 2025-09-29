from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.database.requests import set_user, update_user


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

