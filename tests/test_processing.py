import pytest
from src.processing import filter_by_state, sort_by_date
from typing import List, Dict, Any
from datetime import date

class TestFilterByState:
    """Тесты для функции filter_by_state"""

    def test_empty_list(self, empty_transactions: List[Dict[str, Any]]):
        """Тест с пустым списком транзакций"""
        result = filter_by_state(empty_transactions)
        assert result == []

    def test_only_executed_transactions(
            self,
            only_executed_transactions: List[Dict[str, Any]]
    ):
        """Тест, когда все транзакции уже в нужном состоянии"""
        result = filter_by_state(only_executed_transactions, "EXECUTED")

        # Должны вернуться все транзакции
        assert len(result) == len(only_executed_transactions)
        assert result == only_executed_transactions


def test_only_canceled_transactions(
    only_canceled_transactions: List[Dict[str, Any]]
    ):
    """Тест с транзакциями только в одном состоянии (не EXECUTED)"""
    result = filter_by_state(only_canceled_transactions)
    assert result == []


@pytest.mark.parametrize("state,expected_ids", [
    ("EXECUTED", [1, 3, 5]),  # тест по умолчанию
    ("PENDING", [2]),  # тест для PENDING
    ("CANCELED", [4]),  # тест для CANCELED
    ("EXECUTED", [1, 3, 5]),  # явное указание EXECUTED
])
def test_filter_by_different_states(sample_transactions, state, expected_ids):
    """Тестирование фильтрации по разным состояниям"""
    result = filter_by_state(sample_transactions, state)
    result_ids = [transaction["id"] for transaction in result]
    assert result_ids == expected_ids


def test_filter_non_existing_state(sample_transactions):
    """Тест фильтрации с несуществующим state"""
    result = filter_by_state(sample_transactions, "COMPLETED")

    assert len(result) == 0
    assert result == []


def test_empty_input():
    """Тест с пустым списком на входе"""
    result = filter_by_state([])

    assert len(result) == 0
    assert result == []


class TestSortByDate:
    """Тесты для функции sort_by_date"""

    def test_sort_descending_default(self, sample_dict_list):
        """Тест сортировки по убыванию (по умолчанию)"""
        result = sort_by_date(sample_dict_list)

        # Проверяем, что список отсортирован по убыванию дат
        expected_dates = [date(2023, 3, 20), date(2023, 2, 10), date(2023, 1, 15),
                          date(2023, 1, 1), date(2022, 12, 5)]

        assert [item["date"] for item in result] == expected_dates

    def test_sort_descending_default1(self):
        """Тест сортировки по убыванию (по умолчанию)"""
        data = [
            {"date": "2023-01-01", "name": "item1"},
            {"date": "2023-03-01", "name": "item2"},
            {"date": "2023-02-01", "name": "item3"}
        ]

        result = sort_by_date(data)
        expected_dates = ["2023-03-01", "2023-02-01", "2023-01-01"]

        assert [item["date"] for item in result] == expected_dates

    def test_sort_ascending(self):
        """Тест сортировки по возрастанию"""
        data = [
            {"date": "2023-03-01", "name": "item1"},
            {"date": "2023-01-01", "name": "item2"},
            {"date": "2023-02-01", "name": "item3"}
        ]

        result = sort_by_date(data, reverse=False)
        expected_dates = ["2023-01-01", "2023-02-01", "2023-03-01"]

        assert [item["date"] for item in result] == expected_dates

    @pytest.mark.parametrize("reverse,expected_order", [
        (True, ["2023-03-01", "2023-02-01", "2023-01-01"]),  # по убыванию
        (False, ["2023-01-01", "2023-02-01", "2023-03-01"]),  # по возрастанию
    ])
    def test_sort_order(self, reverse, expected_order):
        """Тестирование правильности порядка сортировки"""
        dict_list = [
            {"date": "2023-01-01", "name": "A"},
            {"date": "2023-03-01", "name": "B"},
            {"date": "2023-02-01", "name": "C"}
        ]

        result = sort_by_date(dict_list, reverse)
        actual_order = [item["date"] for item in result]

        assert actual_order == expected_order

