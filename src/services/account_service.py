from sqlalchemy.ext.asyncio import AsyncSession

from src.models import AccountModel
from src.schemas.account_schemas import AccountReadSchema, AccountCreateSchema
from src.repositories.account_repositories import AccountRepositories



class AccountService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.account_repositories = AccountRepositories(self.session)

    async def get_accounts_by_user_id(self, user_id: int) -> list[AccountReadSchema]:
        accounts =  await self.account_repositories.find_by_user_id(user_id)

        return[
            AccountReadSchema.model_validate(account)
        for account in accounts
        ]

    async def get_by_account_user_pair(self, account_id: int, user_id: int) -> AccountReadSchema | None:
        account = await self.account_repositories.find_by_id_user_id_pair(find_id=account_id, user_id=user_id)
        if account:
            return AccountReadSchema.model_validate(account)

        return None

    async def create(self, account: AccountCreateSchema) -> AccountReadSchema:
        _new_account = AccountModel(
            user_id=account.user_id,
            balance=account.balance,
        )
        if account.id:
            _new_account.id = account.id

        _new_account = await self.account_repositories.create(_new_account)

        await self.session.commit()
        return AccountReadSchema.model_validate(_new_account)

    async def update_balance(self, account_id: int, delta: float) -> None:
        await self.account_repositories.update_balance_delta(account_id, delta)
        await self.session.commit()