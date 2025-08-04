from datetime import date
from sqlalchemy import select, update, delete, desc,insert
from app.DB.models import async_session, User,Birhtday,Title
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

def connect(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            async with session.begin():
                try:
                    return await func(session, *args, **kwargs)
                except SQLAlchemyError:
                    raise
    return inner

@connect
async def set_user(session, tg_id: int) -> User:
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        user = User(tg_id=tg_id)
        session.add(user)
        await session.flush()
    return user

@connect
async def set_title(session,title_user: str,owner_id: int):
    new_title = Title(title_user=title_user,owner_id=owner_id)
    session.add(new_title)
    await session.commit()
    return new_title

@connect
async def get_title(session: AsyncSession, owner_id: int) -> list[dict]:
    result = await session.execute(
        select(
            Title.id,
            Title.title_user,
            Title.owner_id
        ).where(
            Title.owner_id == owner_id
        )
    )
    return [dict(row) for row in result.mappings()]
@connect
async def set_bir(session,name: str, birth_date: date, owner_id: int):
    new_bir = Birhtday(name_user=name,birth_date=birth_date,owner_id=owner_id)
    session.add(new_bir)
    await session.commit()
    return new_bir


@connect
async def get_users(session):
    result = await session.scalars(select(User))
    return result.all()

@connect
async def get_birthdays(session: AsyncSession, owner_id: int) -> list[dict]:
    result = await session.execute(
        select(
            Birhtday.id,
            Birhtday.name_user,
            Birhtday.birth_date
        ).where(Birhtday.owner_id == owner_id)
    )
    return [dict(row) for row in result.mappings()]