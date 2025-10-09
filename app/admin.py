from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.database.requests import set_card


admin = Router()



@admin.message(F.chat.id == -1002980866420 , CommandStart)
async def menu(message: Message):
    await message.answer('Выберите пункт меню', reply_markup=kb.admin_menu)


@admin.message(F.chat.id == -1002980866420 , F.text == 'Добавить товар')
async def set_card(message: Message, state: FSMContext):
    await message.answer('Введите информацию о таваре в формате:\nname|description|prise')
    await state.set_state('data_for_card')

@admin.message(F.chat.id == -1002980866420, StateFilter('data_for_card'))
async def data_to_card(message: Message, state: FSMContext):
    await state.update_data(name=message.text.split('|')[0],
                             description=message.text.split('|')[1],
                             price=message.text.split('|')[2])
    await state.set_state('image')
    await message.answer('Отправьте фото тавара')


@admin.message(F.chat.id == -1002980866420, F.photo, StateFilter('image'))
async def image_to_card(message: Message, state: FSMContext):
    image_id = message.photo[-1].file_id
    await state.update_data(image=image_id)
    await state.set_state('category')
    await message.answer('Выберите категорию', reply_markup= await kb.category_for_card)


@admin.callback_query(F.chat.id == -1002980866420, F.data.startswith('category_'), StateFilter('category'))
async def cards(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(category_id=callback.data.split('_')[1])
    data = await state.get_data()
    card = await set_card(data)
    await callback.message.answer(photo=card.image, caption=f'Информация верна?:\n{card.name}\n{card.description}\n{card.price}\n{card.category_id}')



