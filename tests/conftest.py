from datetime import date
from typing import Any, Dict, List

import pytest


@pytest.fixture
def card_numbers_with_spaces() -> Any:
    """Фикстура для номеров с различным количеством пробелов"""
    return [("70007922 89606361", "7000 79** **** 6361"),
            ("70 00 79 22 89 60 63 61", "7000 79** **** 6361"),
            ("7000 7922 8960 6361", "7000 79** **** 6361")]


@pytest.fixture
def account_number_and_expected() -> Any:
    """Фикстура с парами (номер счета, ожидаемая маска)"""
    return [
        ("12345678901234567890", "**7890"),
        ("1234 5678 9012 3456 7890", "**7890"),
        ("  12345678901234567890  ", "**7890"),
        (12345678901234567890, "**7890"),
        ("00001111222233334444", "**4444"),
        ("9999", "**9999"),
    ]


@pytest.fixture
def card_data() -> Any:
    """Фикстура с тестовыми данными карт"""
    return {
        "visa_classic": "Visa Classic 1234567812345678",
        "mastercard_platinum": "MasterCard Platinum 5678123456781234",
        "mir_debit": "Мир Дебетовая 9876543210987654",
        "account": "Счет 12345678901234567890",
        "visa_gold": "Visa Gold 1111222233334444"
    }


@pytest.fixture
def expected_masked_data() -> Any:
    """Фикстура с ожидаемыми результатами маскирования"""
    return {
        "visa_classic": "Visa Classic 1234 56** **** 5678",
        "mastercard_platinum": "MasterCard Platinum 5678 12** **** 1234",
        "mir_debit": "Мир Дебетовая 9876 54** **** 7654",
        "account": "Счет**7890",
        "visa_gold": "Visa Gold 1111 22** **** 4444"
            }


@pytest.fixture
def sample_date_1() -> Any:
    """Фикстура с примером даты"""
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def sample_date_3() -> Any:
    """Фикстура с датой с однозначными числами"""
    return "2024-01-01T00:00:00.000000"


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком транзакций"""
    return []


@pytest.fixture
def only_executed_transactions() -> List[Dict[str, Any]]:
    """Фикстура только с выполненными транзакциями"""
    return [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "EXECUTED", "amount": 200},
        {"id": 3, "state": "EXECUTED", "amount": 300},
    ]


@pytest.fixture
def only_canceled_transactions() -> List[Dict[str, Any]]:
    """Фикстура только с отмененными транзакциями"""
    return [
        {"id": 1, "state": "CANCELED", "amount": 100},
        {"id": 2, "state": "CANCELED", "amount": 200},
    ]


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
            {"id": 1, "state": "EXECUTED", "amount": 100},
            {"id": 2, "state": "PENDING", "amount": 200},
            {"id": 3, "state": "EXECUTED", "amount": 300},
            {"id": 4, "state": "CANCELED", "amount": 400},
            {"id": 5, "state": "EXECUTED", "amount": 500},
        ]


@pytest.fixture
def sample_dict_list() -> Any:
    """Фикстура предоставляет тестовые данные для сортировки по дате"""
    return [
        {"date": date(2023, 1, 15), "name": "Item A", "value": 10},
        {"date": date(2023, 3, 20), "name": "Item B", "value": 20},
        {"date": date(2023, 2, 10), "name": "Item C", "value": 30},
        {"date": date(2022, 12, 5), "name": "Item D", "value": 40},
        {"date": date(2023, 1, 1), "name": "Item E", "value": 50},
    ]


@pytest.fixture
def sample_card_numbers() -> Any:
    """Фикстура с тестовыми номерами карт"""
    return {
        "visa_16": "4000123456789010",
        "mastercard_16": "5500000000000004",
        "amex_15": "341234567890123",
        "visa_19": "4000123456789012345",
        "with_spaces": "4000 1234 5678 9010",
        "short": "123456789012",
        "very_short": "12345678"
    }


@pytest.fixture
def expected_masked_results() -> Any:
    """Фикстура с ожидаемыми результатами маскирования"""
    return {
        "visa_16": "4000 12** **** 9010",
        "mastercard_16": "5500 00** **** 0004",
        "amex_15": "3412 34** **** 123",
        "visa_19": "4000 1234 5678 9012 345",
        "with_spaces": "4000 12** **** 9010",
        "short": "1234 56** **12",
        "very_short": "1234 5678"
    }


@pytest.fixture
def edge_case_card_numbers() -> Any:
    """Фикстура с граничными случаями"""
    return {
        "0000000000000000": "0000 00** **** 0000",
        "9999999999999999": "9999 99** **** 9999",
        "1234": "1234",  # короткий номер
        "12345678901234567890": "1234 56** **** 5678 7890",  # длинный номер
    }


"Фикстуры для генераторов"


@pytest.fixture
def transactions_fixture() -> Any:
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "RUB",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
                },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        }]


"Для transaction_descriptions"


@pytest.fixture
def sample_transactions1() -> Any:
    """Фикстура с обычными транзакциями"""
    return [
        {'id': 1, 'description': 'Покупка', 'amount': 100, 'currency': 'RUB'},
        {'id': 2, 'description': 'Продажа', 'amount': 200, 'currency': 'USD'},
        {'id': 3, 'description': 'Перевод', 'amount': 50, 'currency': 'EUR'},
    ]


@pytest.fixture
def empty_transactions1() -> Any:
    """Фикстура с пустым списком транзакций"""
    return []


@pytest.fixture
def mixed_transactions() -> Any:
    """Фикстура со смешанными транзакциями (с description и без)"""
    return [
        {'id': 1, 'amount': 100},
        {'id': 2, 'description': 'Покупка в магазине', 'amount': 200},
        {'id': 3, 'amount': 300, 'date': '2024-01-01'},
        {'id': 4, 'description': 'Оплата интернета', 'amount': 400},
    ]


"Фикстуры для card_number_generator"


@pytest.fixture
def edge_case_ranges() -> Any:
    """Фикстура для граничных случаев"""
    return [
        (0, 9999),  # Много чисел
        (9999999999990000, 9999999999999999),  # Конец диапазона
        (-100, 100),  # С отрицательными числами
    ]
