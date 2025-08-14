from fastapi import APIRouter, Depends

from src.api.dependencies import get_payment_api_service
from src.api.payments.payment_requests import PaymentCreateRequest
from src.api.payments.service.payments_api_service import PaymentApiService

payments_router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


@payments_router.post(
    "/webhook",
    response_model=None,
    summary="Обработка входящего webhook от платёжной системы",
    description="""
    Принимает данные о платеже от внешней платёжной системы и передаёт их 
    в сервис для проверки подписи, валидации и записи в базу данных.

    Ожидаемые поля:
    - `transaction_id` — уникальный идентификатор транзакции (UUID)
    - `amount` — сумма платежа
    - `user_id` — ID пользователя
    - `account_id` — ID счёта пользователя
    - `signature` — подпись для проверки подлинности
    """
)
async def webhook(
        payment: PaymentCreateRequest,
        service: PaymentApiService = Depends(get_payment_api_service)
):
    await service.create_payment(payment)

    return {"status": "success"}
