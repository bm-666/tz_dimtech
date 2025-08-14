from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from src.models.account_model import AccountModel

class AccountRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_user_id(self, user_id: int) -> ScalarResult[AccountModel]:
        stmt = (
            select(AccountModel).where(AccountModel.user_id == user_id)
        )
        return await self.session.scalars(stmt)

    async def find_by_id_user_id_pair(self, find_id: int, user_id: int) -> AccountModel | None:
        stmt = (
            select(AccountModel).where(
    AccountModel.id == find_id,
                AccountModel.user_id==user_id
            )
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def create(self, account: AccountModel) -> AccountModel:
        self.session.add(account)
        await self.session.flush()
        return account

    async def update_balance_delta(self, account_id: int, balance: float) -> None:
        stmt = (
            update(AccountModel)
            .where(AccountModel.id==account_id)
            .values(balance=AccountModel.balance + balance)
            .returning(AccountModel.id)
        )
        return await self.session.scalar(stmt)