from app.database.models import async_session, User, Category, Card
from sqlalchemy import select, update


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            return False
        return True if user.name  else False
    

async def update_user(tg_id, name, phone):
    async with async_session() as session:
        await session.execute(
            update(User).where(tg_id == tg_id).values(name=name, phone_number=phone)
            )
        await session.commit()


async def add_card(name, description, price, image, category_id):
    async with async_session() as session:
        session.add(Card(name=name, description=description, price=price, image=image, category_id=category_id))
        await session.commit()

    
async def get_user(tg_id):
        async with async_session() as session:
            return await session.scalar(select(User).where(User.tg_id==tg_id))


async def get_category():
    async with async_session() as session:
        return await session.scalars(select(Category))
    

async def get_category_to_card(cat_id):
    async with async_session() as session:
        return await session.scalar(select(Category).where(Category.id==cat_id))
    

async def get_cards(category):
    async with async_session() as session:
        return await session.scalars(select(Card).where(Card.category_id == category))


async def get_card(card_id):
    async with async_session() as session:
        return await session.scalar(select(Card).where(Card.id == card_id))
    


