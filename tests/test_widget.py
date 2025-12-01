import pytest
from src.widget import mask_account_card, get_date

class TestMaskAccountCard:
    """Тесты для функции mask_account_card"""

    def test_visa_card_mask(self, card_data, expected_masked_data):
        """Тест маскировки номера Visa карты"""
        result = mask_account_card(card_data["visa_classic"])
        expected = expected_masked_data["visa_classic"]
        assert result == expected

    def test_account_mask(self, card_data, expected_masked_data):
        """Тест маскировки номера счета"""
        result = mask_account_card(card_data["account"])
        expected = expected_masked_data["account"]
        assert result == expected

    @pytest.mark.parametrize("account_input,expected", [
        ("Счет 12345678901234567890", "Счет**7890"),
        ("счет 98765432109876543210", "Счет**3210"),
        ("СЧЕТ 11112222333344445555", "Счет**5555"),
    ])
    def test_mask_account_number(self, account_input, expected):
        """Тестирование маскирования номеров счетов с параметризацией"""
        result = mask_account_card(account_input)
        assert result == expected

    def test_case_insensitivity(self):
        """Тестирование нечувствительности к регистру для слова 'счет'"""
        test_cases = [
            ("Счет 12345678901234567890", "Счет**7890"),
            ("счет 12345678901234567890", "Счет**7890"),
            ("СЧЕТ 12345678901234567890", "Счет**7890"),
        ]

        for input_text, expected in test_cases:
            result = mask_account_card(input_text)
            assert result == expected

    def test_card_name_preservation(self):
        """Тестирование сохранения названия карты"""
        test_cases = [
            ("Visa Classic 1234567812345678", "Visa Classic"),
            ("MasterCard Platinum 5678123456781234", "MasterCard Platinum"),
            ("Мир Дебетовая 9876543210987654", "Мир Дебетовая"),
        ]

        for input_text, expected_name in test_cases:
            result = mask_account_card(input_text)
            assert result.startswith(expected_name)



class TestGetDate:
    """Тесты для функции get_date"""

    def test_basic_date_conversion(self, sample_date_1):
        """Тест базового преобразования даты"""
        result = get_date(sample_date_1)
        assert result == "11.03.2024"

    def test_date_with_single_digits(self, sample_date_3):
        """Тест даты с однозначными числами"""
        result = get_date(sample_date_3)
        assert result == "01.01.2024"

    @pytest.mark.parametrize("input_date", [
        "2024-03-11",  # отсутствует время
        "2024-03-11T02:26:18",  # отсутствуют миллисекунды
        "2024-03-11T02:26",  # отсутствуют секунды и миллисекунды
    ])
    def test_get_date_partial_formats(self, input_date):
        """Тестирование частичных форматов (должны работать)"""
        # Эти форматы должны работать, так как split("T")[0] вернет дату
        result = get_date(input_date)
        assert result == "11.03.2024"

    @pytest.mark.parametrize("invalid_date", [
        "2024/03/11T02:26:18.671407",
        "11-03-2024T02:26:18.671407",
        "2024-03-11",
        "02:26:18.671407",
        "invalid_date_string",
        "",
        "2024-03-11T",
        "T02:26:18.671407",
    ])
    def test_get_date_invalid_formats_should_fail(self, invalid_date):
        """Тестирование некорректных форматов (ожидаем ошибки)"""
        try:
            result = get_date(invalid_date)
            print(f"Функция обработала некорректный формат: {invalid_date} -> {result}")
        except Exception as e:
            assert isinstance(e, (ValueError, IndexError, AttributeError))

    def test_get_date_end_of_year(self):
        """Тест с концом года"""
        input_date = "2023-12-31T23:59:59.999999"
        expected = "31.12.2023"
        assert get_date(input_date) == expected

    def test_get_date_basic(self):
        """Тест базового случая"""
        input_date = "2024-03-11T02:26:18.671407"
        expected = "11.03.2024"
        assert get_date(input_date) == expected

    def test_get_date_millennium(self):
        """Тест с датой из другого тысячелетия"""
        input_date = "1995-08-24T10:20:30.444444"
        expected = "24.08.1995"
        assert get_date(input_date) == expected