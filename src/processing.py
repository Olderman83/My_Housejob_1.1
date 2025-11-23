from typing import List, Dict, Any


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Функция принимает список словарей и опционально значение для ключа "state" (по умолчанию
    'EXECUTED'). Возвращает новый список словарей, содержащий только те словари, у которых ключ
    "state" соответствует указанному значению"""

    filtered_list = []
    for transaction in transactions:
        if transaction ["state"] == state:
            filtered_list.append(transaction)
    return filtered_list


def sort_by_date(dict_list: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Функция принимает список словарей и необязательный параметр, задающий порядок сортировки
    (по умолчанию — убывание). Возвращает новый список, отсортированный по дате"""
    return sorted(dict_list, key=lambda x: x["date"], reverse=reverse)
