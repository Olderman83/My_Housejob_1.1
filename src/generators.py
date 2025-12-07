from typing import List, Any, Iterator

def filter_by_currency(list_transactions: list, currency: str) -> Iterator:
    """Функция принимает на вход список словарей, представляющих транзакции
и возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной"""
    for transaction in (t for t in list_transactions if t["operationAmount"]["currency"]["name"] == currency):
        yield transaction


def transaction_descriptions(list_transactions) -> Iterator:
    """Генератор принимает список словарей с транзакциями и возвращает описание каждой операции по очереди"""
    for transaction in list_transactions:
        if 'description' in transaction:
            yield transaction['description']


def card_number_generator(start: int, end: int) -> Iterator:
    """Генератор выдает номера банковских карт в формате
XXXX XXXX XXXX XXXX"""
    for number in range(start, end + 1):
        card_str = str(number).zfill(16)
        # Форматируем в группы по 4 цифры
        formatted = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        yield formatted
