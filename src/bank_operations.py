import re
from collections import Counter
from typing import List, Dict, Any


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по заданной строке в описании с использованием регулярных выражений.
    """
    if not search:
        return data

    results = []
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for transaction in data:
        description = transaction.get('description', '')
        if pattern.search(description):
            results.append(transaction)

    return results


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций определенных категорий.
    """
    if not categories:
        return {}

    # Приводим категории к нижнему регистру для регистронезависимого сравнения
    categories_lower = [cat.lower() for cat in categories]

    # Собираем все описания операций
    descriptions = []
    for transaction in data:
        description = transaction.get('description', '')
        if description:
            descriptions.append(description.lower())

    # Фильтруем и считаем только нужные категории
    filtered_descriptions = [desc for desc in descriptions if any(cat in desc for cat in categories_lower)]

    # Создаем словарь для подсчета
    result = Counter(filtered_descriptions)

    # Преобразуем обратно к оригинальным названиям категорий
    final_result = {}
    for desc, count in result.items():
        for cat in categories:
            if cat.lower() in desc:
                if cat not in final_result:
                    final_result[cat] = 0
                final_result[cat] += count

    return final_result
