import os
from unittest.mock import Mock, patch

from src.external_api import convert_to_rubles


def test_convert_to_rubles_rub():
    """Тест для транзакции в рублях."""
    transaction = {"amount": 1000, "currency": "RUB"}
    result = convert_to_rubles(transaction)
    assert result == 1000.0


def test_convert_to_rubles_unsupported_currency():
    """Тест для неподдерживаемой валюты."""
    transaction = {"amount": 100, "currency": "GBP"}
    result = convert_to_rubles(transaction)
    assert result == 100.0


@patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
@patch('requests.get')
def test_convert_to_rubles_usd_success(mock_get):
    """Тест успешной конвертации USD."""
    # Мокаем ответ API
    mock_response = Mock()
    mock_response.json.return_value = {
        "rates": {"RUB": 75.5},
        "success": True
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    transaction = {"amount": 100, "currency": "USD"}
    result = convert_to_rubles(transaction)

    # Проверяем, что результат конвертирован
    assert result == 7550.0  # 100 * 75.5
    mock_get.assert_called_once()


@patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
@patch('requests.get')
def test_convert_to_rubles_eur_success(mock_get):
    """Тест успешной конвертации EUR."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "rates": {"RUB": 85.0},
        "success": True
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    transaction = {"amount": 50, "currency": "EUR"}
    result = convert_to_rubles(transaction)

    assert result == 4250.0  # 50 * 85.0


@patch('requests.get')
def test_convert_to_rubles_api_error(mock_get):
    """Тест при ошибке API."""
    mock_get.side_effect = Exception("API error")

    transaction = {"amount": 100, "currency": "USD"}
    result = convert_to_rubles(transaction)
    assert result == 0.0


def test_convert_to_rubles_no_api_key():
    """Тест при отсутствии API ключа."""
    if 'API_KEY' in os.environ:
        del os.environ['API_KEY']

    transaction = {"amount": 100, "currency": "USD"}
    result = convert_to_rubles(transaction)
    assert result == 100.0


def test_convert_to_rubles_missing_amount():
    """Тест при отсутствии суммы."""
    transaction = {"currency": "RUB"}
    result = convert_to_rubles(transaction)
    assert result == 0.0
