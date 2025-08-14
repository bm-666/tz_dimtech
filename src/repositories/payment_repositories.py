from sqlalchemy import select, ScalarResult

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.payment_model import PaymentModel


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_user_id(self, user_id: int) -> ScalarResult[PaymentModel]:
        stmt = (
            select(PaymentModel).where(PaymentModel.user_id == user_id)
        )
        return await self.session.scalars(stmt)

    async def find_by_transaction_id(self, transaction_id: str) -> PaymentModel | None:
        stmt = (
            select(PaymentModel).where(PaymentModel.transaction_id == transaction_id)
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def create(self, payment: PaymentModel) -> PaymentModel:
        self.session.add(payment)
        await self.session.flush()
        return payment