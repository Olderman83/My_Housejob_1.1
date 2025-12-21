import json
import logging
import os
from typing import Any, Dict, List

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными о транзакциях.
            Если файл пустой, содержит не список или не найден, возвращается пустой список.
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        # Проверяем, не пустой ли файл
        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл пустой: {file_path}")
            return []

        # Читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные - список
        if not isinstance(data, list):
            logger.warning(f"Файл содержит не список: {file_path}")
            return []

        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []
