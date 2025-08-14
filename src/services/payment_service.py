from src.models import PaymentModel
from src.schemas.payment_schemas import PaymentReadSchema, PaymentCreateSchema
from src.repositories.payment_repositories import PaymentRepository
from sqlalchemy.ext.asyncio import AsyncSession


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.payment_repository = PaymentRepository(session)

    async def get_by_user_id(self, user_id: int) -> list[PaymentReadSchema]:
        payments =  await self.payment_repository.find_by_user_id(user_id)
        return [
            PaymentReadSchema.model_validate(payment)
            for payment in payments
        ]
    async def get_by_transaction_id(self, transaction_id: str) -> PaymentReadSchema | None :

        result = await self.payment_repository.find_by_transaction_id(transaction_id)
        print("Result", result)
        return PaymentReadSchema.model_validate(result) if result else None


    async def create(self, payment: PaymentCreateSchema) -> PaymentReadSchema:
        payment_model = PaymentModel(
            user_id=payment.user_id,
            amount=payment.amount,
            transaction_id=payment.transaction_id,
            account_id=payment.account_id,

        )
        new_payment = await self.payment_repository.create(payment_model)
        await self.session.commit()
        return PaymentReadSchema.model_validate(new_payment)

