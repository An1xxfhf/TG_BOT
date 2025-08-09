from sqlalchemy import ForeignKey, String, BigInteger,Date
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import settings
from typing import Annotated

engine = create_async_engine(url=settings.DB_URL_ASP,
    echo=True)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass
intpk = Annotated[int,mapped_column(primary_key=True)]
class User(Base):
    __tablename__ = 'users'
    id: Mapped[intpk]
    tg_id = mapped_column(BigInteger,unique=True)

class Birhtday(Base):
    __tablename__ = 'birthdays'
    id: Mapped[intpk]
    name_user: Mapped[str] = mapped_column(String(25),nullable=False)
    birth_date:Mapped[date] = mapped_column(Date(),nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))
class Title(Base):
    __tablename__ = 'Title'
    id: Mapped[intpk]
    title_user: Mapped[str] = mapped_column(String(50), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))







async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)