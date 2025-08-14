class IncorrectSignatureError(Exception):
    def __init__(self):
        super().__init__("Неверная подпись")

class TransactionDuplicateError(Exception):
    def __init__(self, transaction_id: str):
        super().__init__(f"Транзакция {transaction_id} уже проходила")