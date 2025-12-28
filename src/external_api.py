import logging
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    """
    try:
        # Получаем сумму и валюту
        amount = transaction.get('amount', 0)
        currency = transaction.get('currency', 'RUB')

        # Если уже в рублях, возвращаем как есть
        if currency == 'RUB':
            return float(amount)

        # Проверяем поддерживаемые валюты
        if currency not in ['USD', 'EUR']:
            logger.warning(f"Неподдерживаемая валюта: {currency}")
            return float(amount)

        # Получаем API ключ
        api_key = os.getenv('API_KEY')
        api_url = os.getenv('API_URL')

        if not api_key:
            logger.error("API ключ не найден. Проверьте файл .env")
            return float(amount)

        # Получаем курс валюты
        headers = {"apikey": api_key}
        params = {"to": "RUB", "from": currency, "amount": amount}

        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            rate = data['rates'].get('RUB')

            if rate:
                # Конвертируем сумму
                converted_amount = float(amount) * rate
                logger.info(f"Конвертировано {amount} {currency} в {converted_amount:.2f} RUB")
                return converted_amount
            else:
                logger.error(f"Не удалось получить курс для {currency}")
                return float(amount)

        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе к API: {e}")
            return float(amount)
        except KeyError as e:
            logger.error(f"Ошибка в структуре ответа API: {e}")
            return float(amount)

    except Exception as e:
        logger.error(f"Неожиданная ошибка при конвертации: {e}")
        return 0.0
