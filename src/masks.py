import json
import logging
import os
from typing import Any, Dict, List


# Настройка логирования
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/utils.log', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

logger.info(f"Успешно вычислена сумма")
logger.error(f"Произошла ошибка: ValueError")


def get_mask_card_number(card_number: str) -> str:
    """Возвращает маску банковской карты:XXXX XX** **** XXXX"""
    card_number_str = str(card_number).replace(" ", "")
    parts = [card_number_str[i : i + 4] for i in range(0, len(card_number_str), 4)]
    masked = " ".join(parts)
    masked_list = list(masked)

    for i in range(len(masked_list)):
        if 7 <= i <= 13 and masked_list[i] != " ":
            masked_list[i] = "*"
    return "".join(masked_list)


def get_mask_account(account_number: str) -> str:
    """Возвращает маску банковского счета в формате:**ХХХХ"""
    account_number_str = str(account_number).replace(" ", "")
    return "**" + account_number_str[-4:]
