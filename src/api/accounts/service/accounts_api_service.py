from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from src.api.accounts.accounts_response import AccountResponseSchema
from src.services.account_service import AccountService
from src.schemas.account_schemas import AccountReadSchema


class AccountsApiService:
    def __init__(self, session: AsyncSession):
        self.account_service = AccountService(session)

    async def get_accounts_by_user_id(self, user_id: int) -> list[AccountResponseSchema]:
        accounts = await self.account_service.get_accounts_by_user_id(user_id=user_id)
        return [
            AccountResponseSchema.model_validate(account)
            for account in accounts
        ]