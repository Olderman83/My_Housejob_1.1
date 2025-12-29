import pytest

from src.bank_operations import process_bank_operations, process_bank_search


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "date": "2023-01-01T12:00:00.000000",
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"code": "RUB"}
            }
        },
        {
            "id": 2,
            "description": "Перевод с карты на карту",
            "date": "2023-01-02T12:00:00.000000",
            "operationAmount": {
                "amount": "500.00",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 3,
            "description": "Оплата услуг",
            "date": "2023-01-03T12:00:00.000000",
            "operationAmount": {
                "amount": "750.00",
                "currency": {"code": "EUR"}
            }
        },
        {
            "id": 4,
            "description": "Перевод организации",
            "date": "2023-01-04T12:00:00.000000",
            "operationAmount": {
                "amount": "1200.00",
                "currency": {"code": "RUB"}
            }
        }
    ]


def test_process_bank_search(sample_transactions):
    # Поиск точного совпадения
    result = process_bank_search(sample_transactions, "Перевод")
    assert len(result) == 3

    # Поиск с регистронезависимостью
    result = process_bank_search(sample_transactions, "ОРГАНИЗАЦИИ")
    assert len(result) == 2

    # Поиск несуществующей строки
    result = process_bank_search(sample_transactions, "Несуществующая строка")
    assert len(result) == 0

    # Поиск пустой строки
    result = process_bank_search(sample_transactions, "")
    assert len(result) == 4


def test_process_bank_search_partial_match(sample_transactions):
    result = process_bank_search(sample_transactions, "карт")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_process_bank_operations(sample_transactions):
    categories = ["Перевод организации", "Оплата услуг"]
    result = process_bank_operations(sample_transactions, categories)

    assert "Перевод организации" in result
    assert result["Перевод организации"] == 2
    assert "Оплата услуг" in result
    assert result["Оплата услуг"] == 1


def test_process_bank_operations_empty_categories(sample_transactions):
    result = process_bank_operations(sample_transactions, [])
    assert result == {}


def test_process_bank_operations_case_insensitive(sample_transactions):
    categories = ["ПЕРЕВОД ОРГАНИЗАЦИИ", "оплата услуг"]
    result = process_bank_operations(sample_transactions, categories)

    assert "ПЕРЕВОД ОРГАНИЗАЦИИ" in result
    assert result["ПЕРЕВОД ОРГАНИЗАЦИИ"] == 2
    assert "оплата услуг" in result
    assert result["оплата услуг"] == 1


def test_process_bank_operations_partial_match():
    transactions = [
        {"description": "Перевод организации VK"},
        {"description": "Перевод организации Яндекс"},
        {"description": "Перевод между счетами"},
        {"description": "Оплата услуг связи"},
    ]

    categories = ["Перевод организации", "Оплата услуг"]
    result = process_bank_operations(transactions, categories)

    assert "Перевод организации" in result
    assert result["Перевод организации"] == 2
    assert "Оплата услуг" in result
    assert result["Оплата услуг"] == 1


def test_process_bank_operations_no_description():
    transactions = [
        {"id": 1},
        {"id": 2, "description": ""},
        {"id": 3, "description": None},
    ]

    categories = ["Перевод"]
    result = process_bank_operations(transactions, categories)

    assert result == {}
