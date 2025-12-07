import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:
    """Тесты для маркировки номера карты"""


@pytest.mark.parametrize("card_number,expected", [
    ("7000792289606361", "7000 79** **** 6361"),
    ("1111222233334444", "1111 22** **** 4444")
    ])
def test_get_mask_card_number(card_number, expected):
    """Тестирование числового ввода"""
    result = get_mask_card_number(card_number)
    assert result == expected


def test_none_input():
    """Тестирование None ввода"""
    assert get_mask_card_number("None") == "None"


def test_empty_string():
    """Тестирование пустой строки"""
    assert get_mask_card_number("") == ""


def test_card_numbers_with_spaces(card_numbers_with_spaces):
    """Тестирование номеров с различным количеством пробелов"""
    for card_number, expected_mask in card_numbers_with_spaces:
        result = get_mask_card_number(card_number)
        assert result == expected_mask


def test_get_mask_card_number_standard():
    """Тест стандартного номера карты"""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_card_number_different_length():
    """Тест номера карты разной длины"""
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number("1111222233334444") == "1111 22** **** 4444"


def test_get_mask_card_number_minimal():
    """Тест минимального номера карты"""
    assert get_mask_card_number("1234") == "1234"


def test_16_digit_card_mask(sample_card_numbers, expected_masked_results):
    """Тест маскирования стандартной 16-значной карты"""
    card_number = sample_card_numbers["visa_16"]
    expected = expected_masked_results["visa_16"]
    result = get_mask_card_number(card_number)
    assert result == expected


def test_15_digit_amex_mask(sample_card_numbers, expected_masked_results):
    """Тест маскирования 15-значной American Express"""
    card_number = sample_card_numbers["amex_15"]
    expected = expected_masked_results["amex_15"]
    result = get_mask_card_number(card_number)
    assert result == expected


def test_get_mask_card_number_single_digit():
    """Тест одной цифры"""
    card_number = "1"
    result = get_mask_card_number(card_number)
    assert result == "1"


def test_get_mask_card_number_numeric_input():
    """Тест числового ввода (не строки)"""
    card_number = 1234567890123456
    result = get_mask_card_number(card_number)
    assert result == "1234 56** **** 3456"


def test_get_mask_card_number_preserves_spaces():
    """Тест, что пробелы в правильных местах сохраняются"""
    card_number = "1111222233334444"
    result = get_mask_card_number(card_number)
    # Проверяем, что пробелы на позициях 4, 9, 14 сохраняются
    assert result[4] == " "
    assert result[9] == " "
    assert result[14] == " "


@pytest.mark.parametrize("short_card_number", [
        "1234",
        "123456",
        "12345678",
        "123456789012",  # 12 цифр
        "12345678901234",  # 14 цифр
])
def test_short_card_numbers(short_card_number):
    """Тестирование коротких номеров карт"""
    result = get_mask_card_number(short_card_number)
    # Для коротких номеров проверяем, что функция не падает
    # и возвращает что-то осмысленное
    assert isinstance(result, str)


@pytest.mark.parametrize("long_card_number", [
        "12345678901234567890",  # 20 цифр
        "123456789012345678901234567890",  # 30 цифр
    ])
def test_long_card_numbers(long_card_number):
    """Тестирование длинных номеров карт"""
    result = get_mask_card_number(long_card_number)
    assert isinstance(result, str)
    # Проверяем, что функция обрабатывает длинные номера без ошибок


def test_special_characters():
    """Тестирование строки со специальными символами"""
    result = get_mask_card_number("1234-5678-9012-3456")
    # Функция должна обработать это, убрав не-цифровые символы
    assert isinstance(result, str)


class TestGetMaskAccount:
    """Тесты для маскировки аккаунта"""


def test_account_number_and_expected_pairs(account_number_and_expected):
    """Тестирование с предопределенными парами вход-выход"""
    for account_number, expected_mask in account_number_and_expected:
        result = get_mask_account(account_number)
        assert result == expected_mask


@pytest.mark.parametrize("account,expected", [
    ("1234", "**1234"),
    ("12", "**12"),
    ("", "**"),
    ])
def test_short_accounts(account, expected):
    """Тест коротких номеров счетов"""
    result = get_mask_account(account)
    assert result == expected


def test_account_with_spaces():
    """Тест номера счета с пробелами"""
    account = "1234 5678 9012 3456"
    result = get_mask_account(account)
    assert result == "**3456"


def test_empty_string1():
    """Тест пустой строки"""
    result = get_mask_account("")
    assert result == "**"


def test_single_character():
    """Тест одного символа"""
    result = get_mask_account("1")
    assert result == "**1"


def test_get_mask_account_standard():
    """Тест стандартного случая с полным номером счета"""
    assert get_mask_account("12345678901234567890") == "**7890"


def test_account_number_with_spaces():
    """Тест номера счета с пробелами"""
    account = "1234 5678 9012 3456 7890"
    expected = "**7890"
    assert get_mask_account(account) == expected


def test_account_with_mixed_spaces():
    """Тест номера счета с разным количеством пробелов"""
    account = "  1234  5678  9012  3456  7890  "
    expected = "**7890"
    assert get_mask_account(account) == expected


def test_large_account_number():
    """Тест очень длинного номера счета"""
    account = "1234567890123456789012345678901234567890"
    expected = "**7890"
    assert get_mask_account(account) == expected
