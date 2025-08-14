import hashlib
import logging
from src.schemas.payment_schemas import PaymentCreateSchema
from src.utils.utils import get_concatenate_values

logger = logging.getLogger(__name__)


class SignatureService:
    """
    Сервис для генерации и проверки цифровой подписи платежа.

    Подпись формируется по формуле:
    {account_id}{amount}{transaction_id}{user_id}{secret_key}
    с последующим хэшированием через SHA-256.
    """

    def create_signature(self, payment: PaymentCreateSchema, secret_key: str) -> str:
        """
        Создает цифровую подпись для объекта платежа.

        :param payment: объект платежа
        :param secret_key: секретный ключ, известный только серверу
        :return: хэш SHA-256 в виде строки
        """
        # Объединяем значения платежа в строку и добавляем секретный ключ
        raw_signature = get_concatenate_values(payment) + secret_key
        logger.debug("📝 Сырая строка для подписи: %s", raw_signature)

        # Возвращаем SHA-256 хэш в шестнадцатеричном виде
        signature = hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()
        logger.debug("🔑 Сформированная подпись: %s", signature)

        return signature

