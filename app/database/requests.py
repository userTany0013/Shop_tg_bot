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
