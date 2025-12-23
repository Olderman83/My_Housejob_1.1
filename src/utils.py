import json
import logging
import os
from typing import Any, Dict, List


# Настройка логирования
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/utils.log', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

logger.info(f"Успешно вычислена сумма")
logger.error(f"Произошла ошибка: ValueError")


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
