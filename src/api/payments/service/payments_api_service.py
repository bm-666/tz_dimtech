import logging
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.account_schemas import AccountCreateSchema
from src.services.account_service import AccountService
from src.config import config
from src.api.payments.payment_requests import PaymentCreateRequest
from src.schemas.payment_schemas import PaymentReadSchema, PaymentCreateSchema
from src.services.payment_service import PaymentService
from src.api.payments.service.signature_service import SignatureService

logger = logging.getLogger(__name__)


class PaymentApiService:
    """
    Сервис для обработки платежей, получаемых через вебхуки.

    Основные задачи:
    - Проверка корректности подписи
    - Предотвращение дублирования транзакций
    - Создание/поиск счета пользователя
    - Обновление баланса
    - Сохранение информации о платеже
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация сервиса платежей.

        :param session: асинхронная сессия SQLAlchemy
        """
        self.session = session
        self.payment_service = PaymentService(session)
        self.account_service = AccountService(session)
        self.signature_service = SignatureService()

    async def create_payment(self, payment_request: PaymentCreateRequest) -> PaymentReadSchema:
        """
        Обрабатывает входящий webhook-платеж.

        Шаги:
        1. Проверка подписи
        2. Проверка уникальности transaction_id
        3. Получение или создание счёта
        4. Обновление баланса
        5. Сохранение платежа

        :param payment_request: объект запроса на создание платежа
        :return: данные созданного платежа
        """
        logger.info("📩 Получен webhook-платеж: %s", payment_request)

        # Преобразуем входящие данные в схему для валидации
        payment_data = PaymentCreateSchema.model_validate(payment_request)

        # 1. Проверка подписи
        expected_signature = self.signature_service.create_signature(
            payment_data, config.WEBHOOK_SECRET_KEY
        )
        if payment_request.signature != expected_signature:
            logger.warning("❌ Некорректная подпись. Ожидалось: %s, Получено: %s",
                           expected_signature, payment_request.signature)
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Подпись не действительна"
            )

        # 2. Проверка уникальности транзакции
        existing_payment = await self.payment_service.get_by_transaction_id(payment_data.transaction_id)
        if existing_payment:
            logger.warning("⚠️ Платеж с transaction_id=%s уже существует", payment_data.transaction_id)
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Данная транзакция использовалась ранее"
            )

        # 3. Получение или создание счёта пользователя
        account = await self.account_service.get_by_account_user_pair(
            account_id=payment_data.account_id,
            user_id=payment_data.user_id
        )
        if not account:
            logger.info("🏦 Создание нового счёта для пользователя ID=%s", payment_data.user_id)
            account = await self.account_service.create(AccountCreateSchema(
                balance=0.0,
                user_id=payment_data.user_id,
                id=payment_data.account_id,
            ))

        # 4. Обновление баланса счёта
        logger.info("💰 Обновление баланса счёта ID=%s на сумму %.2f", account.id, payment_data.amount)
        await self.account_service.update_balance(
            account_id=account.id,
            delta=payment_data.amount
        )

        # 5. Сохранение платежа
        new_payment = await self.payment_service.create(payment_data)
        logger.info("✅ Платеж успешно сохранен: transaction_id=%s", new_payment.transaction_id)

        return PaymentReadSchema.model_validate(new_payment)

    async def get_user_payments(self, user_id: int) -> list[PaymentReadSchema]:
        """
        Возвращает список платежей пользователя.

        :param user_id: ID пользователя
        :return: список платежей
        """
        logger.info("📜 Получение списка платежей для пользователя ID=%s", user_id)
        payments = await self.payment_service.get_by_user_id(user_id)
        return [PaymentReadSchema.model_validate(p) for p in payments]
