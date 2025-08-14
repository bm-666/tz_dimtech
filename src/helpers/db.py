from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,

)
from typing import AsyncGenerator
from contextlib import asynccontextmanager


class SessionManagerHelper:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            expire_on_commit: bool = False,


    ):
        self.engine: AsyncEngine = create_async_engine(
            url,
            echo=echo
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=expire_on_commit
        )

    @asynccontextmanager
    async def _get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()


    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._get_session() as session:
            yield session