from src.api.auth.services.auth_api_service import AuthAPIService
from src.api.auth.services.jwt_service import JWTService
from src.config import config
from src.helpers.db import SessionManagerHelper
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import  AsyncSession

session_manager = SessionManagerHelper(
    url=config.get_async_postgres_url_connection()
)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.get_async_session() as session:
        yield session

async def get_auth_service() -> AuthAPIService:
    async with get_session() as session:
        return AuthAPIService(session)
def get_jwt_service() -> JWTService:
    return JWTService()
