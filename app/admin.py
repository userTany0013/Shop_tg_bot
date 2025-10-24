from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.admin as kb
from app.database.requests.admin import get_category_to_card, add_card, get_card


admin = Router()



@admin.callback_query(F.data == 'back')
@admin.message(CommandStart())
async def menu(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await event.answer('Выберите пункт меню', reply_markup=kb.admin_menu)
    else:
        await event.answer(text='Вы вернулись')
        await event.message.delete()
        await event.message.answer('Выберите пункт меню', reply_markup=kb.admin_menu)


@admin.callback_query(F.data == 'no')
@admin.message(F.text == 'добавить товар')
async def set_card(event: Message | CallbackQuery, state: FSMContext):
    if isinstance(event, Message):
        await event.answer('Введите информацию о таваре в формате:\nname|description|prise')
        await state.set_state('data_for_card')
    else:
        await event.answer(text='Вы вернулись')
        await event.message.delete()
        await event.message.answer('Введите информацию о таваре в формате:\nname|description|prise')
        await state.set_state('data_for_card')

@admin.message(StateFilter('data_for_card'))
async def data_to_card(message: Message, state: FSMContext):
    await state.update_data(name=message.text.split('|')[0],
                             description=message.text.split('|')[1],
                             price=message.text.split('|')[2])
    await state.set_state('image')
    await message.answer('Отправьте фото тавара')


@admin.message(F.photo, StateFilter('image'))
async def image_to_card(message: Message, state: FSMContext):
    image_id = message.photo[-1].file_id
    await state.update_data(image=image_id)
    await state.set_state('category_to_card')
    await message.answer('Выберите категорию', reply_markup= await kb.category_for_card())


@admin.callback_query(F.data.startswith('tocardcategory_'), StateFilter('category_to_card'))
async def cards(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(category_id=callback.data.split('_')[1])
    data = await state.get_data()
    cat = await get_category_to_card(data['category_id'])
    await callback.message.answer_photo(photo=data['image'],
                                         caption=f'Информация верна?:\n{cat.name}\n{data['name']}\n{data['description']}\n{data['price']}',
                                           reply_markup=await kb.confirm())


@admin.callback_query(F.data == 'data_yes')
async def save_data(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        name=data['name']
        description=data['description']
        price=data['price']
        image=data['image']
        category_id=data['category_id']
        await add_card(name=name, description=description, price=price, image=image, category_id=category_id)
        await callback.message.answer('Товар добавлен')


@admin.callback_query(F.data == 'all_categories')
@admin.message(F.text == 'Данные о товаре')
async def data(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await event.answer('Все товары:', reply_markup= await kb.catigories_all_cards())
    else:
        await event.answer()
        await event.message.delete()
        await event.message.answer('Все товары:', reply_markup= await kb.catigories_all_cards())


@admin.callback_query(F.data.startswith('allcategory_'))
async def cards_all(callback: CallbackQuery):
    await callback.answer()
    cat_id = callback.data.split('_')[1]
    await callback.message.edit_text('Выберите товар', reply_markup= await kb.cards_all(cat_id))


@admin.callback_query(F.data.startswith('allcard_'))
async def cards_info(callback: CallbackQuery):
    await callback.answer()
    card_id = callback.data.split('_')[1]
    card = await get_card(card_id)
    await callback.message.delete()
    await callback.message.answer_photo(photo=card.image,
                             caption=f'{card.name}\n\n{card.description}\n\n{card.price} RUB')
