from app.database.models import async_session, User, Category, Card
from sqlalchemy import select


async def add_card(name, description, price, image, category_id):
    async with async_session() as session:
        card = session.add(Card(name=name, description=description, price=price, image=image, category_id=category_id))
        await session.commit()


async def get_category_to_card(cat_id):
    async with async_session() as session:
        return await session.scalar(select(Category).where(Category.id==cat_id))
    

async def get_category():
    async with async_session() as session:
        return await session.scalars(select(Category))
    

async def get_cards(category):
    async with async_session() as session:
        return await session.scalars(select(Card).where(Card.category_id == category))
    

async def get_card(card_id):
    async with async_session() as session:
        return await session.scalar(select(Card).where(Card.id == card_id))
