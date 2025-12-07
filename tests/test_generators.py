import pytest
from src.generators import filter_by_currency
from src.generators import transaction_descriptions
from src.generators import card_number_generator



class TestFilterByCurrency:
    """Тесты для функции filter_by_currency"""

    def test_filter_usd_transactions(self, transactions_fixture):
        """Тест фильтрации транзакций в USD"""
        usd_transactions = list(filter_by_currency(transactions_fixture, "USD"))
        assert len(usd_transactions) == 2  # В фикстуре должно быть 2 транзакции в USD
        for transaction in usd_transactions:
            assert transaction["operationAmount"]["currency"]["name"] == "USD"

    def test_filter_rub_transactions(self, transactions_fixture) -> None:
        """Тест фильтрации транзакций в RUB"""
        rub_transactions = list(filter_by_currency(transactions_fixture, "RUB"))
        assert len(rub_transactions) == 1  # В фикстуре должна быть 1 транзакция в RUB
        for transaction in rub_transactions:
            assert transaction["operationAmount"]["currency"]["name"] == "RUB"

    def test_empty_transaction_list(self) -> None:
        """Тест с пустым списком транзакций"""
        result = list(filter_by_currency([], "USD"))
        assert len(result) == 0

    def test_case_sensitivity(self, transactions_fixture) -> None:
        """Тест чувствительности к регистру"""
        result_lower = list(filter_by_currency(transactions_fixture, "usd"))
        result_upper = list(filter_by_currency(transactions_fixture, "USD"))
        assert len(result_lower) == 0  # "usd" в нижнем регистре не должно найти
        assert len(result_upper) == 2

    @pytest.mark.parametrize("currency,expected_count", [
        ("USD", 2),
        ("RUB", 1),
        ("GBP", 0),
    ])
    def test_parametrized_filter(self, transactions_fixture, currency, expected_count) -> None:
        """Параметризованный тест для разных валют"""
        result = list(filter_by_currency(transactions_fixture, currency))
        assert len(result) == expected_count
        for transaction in result:
            assert transaction["operationAmount"]["currency"]["name"] == currency


class TestTransactionDescriptionsWithFixtures:
    """Тесты с использованием фикстур"""

    def test_with_fixture_transactions(self, sample_transactions1) -> None:
        """Тест с фикстурой из conftest.py"""
        result = list(transaction_descriptions(sample_transactions1))
        expected = ['Покупка', 'Продажа', 'Перевод']
        assert result == expected

    def test_with_empty_fixture(self, empty_transactions1) -> None:
        """Тест с пустой фикстурой"""
        result = list(transaction_descriptions(empty_transactions1))
        assert result == []

    def test_with_mixed_fixture(self, mixed_transactions) -> None:
        """Тест со смешанной фикстурой"""
        result = list(transaction_descriptions(mixed_transactions))
        expected = ['Покупка в магазине', 'Оплата интернета']
        assert result == expected

    """Тесты """
    def test_empty_list(self) -> None:
        """Тест с пустым списком транзакций"""
        result = list(transaction_descriptions([]))
        assert result == []

    """Тест с параметризацией """


@pytest.mark.parametrize('transactions, expected', [
    ([], []),
    ([{'description': 'Test'}], ['Test']),
    ([{'desc': 'Test'}], []),
    ([
        {'description': 'A'},
        {'description': 'B'},
        {'description': 'C'}
    ], ['A', 'B', 'C']),
    ([
        {'description': 'A'},
        {'not_desc': 'B'},
        {'description': 'C'}
    ], ['A', 'C']),
])
def test_parametrized_transactions(transactions, expected) -> None:
    """Параметризованные тесты для различных случаев"""
    result = list(transaction_descriptions(transactions))
    assert result == expected


class TestCardNumberGenerator:
    """Тесты для генератора номеров карт"""

    def test_generator_returns_iterator(self) -> None:
        """Проверка, что функция возвращает итератор"""
        result = card_number_generator(1, 5)
        assert hasattr(result, '__iter__')
        assert hasattr(result, '__next__')

    def test_single_card_number(self) -> None:
        """Проверка генерации одного номера карты"""
        generator = card_number_generator(1, 1)
        result = list(generator)

        assert len(result) == 1
        assert result[0] == "0000 0000 0000 0001"

    def test_edge_cases(self, edge_case_ranges) -> None:
        """Тест граничных случаев"""
        for start, end in edge_case_ranges:
            generator = card_number_generator(start, end)
            result = list(generator)

            # Проверяем количество элементов
            expected_count = max(0, end - start + 1)
            assert len(result) == expected_count

            if result:  # Если есть элементы
                # Проверяем формат первого элемента
                assert len(result[0]) == 19  # 16 цифр + 3 пробела
                assert result[0].count(' ') == 3
