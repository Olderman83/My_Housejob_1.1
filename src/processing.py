from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.

    :param transactions: Список транзакций
    :param state: Статус для фильтрации (по умолчанию "EXECUTED")
    :return: Отфильтрованный список транзакций
    """
    filtered_transactions = []

    for transaction in transactions:
        # Проверяем наличие ключа 'state' в транзакции
        if "state" in transaction and transaction["state"] == state:
            filtered_transactions.append(transaction)

    return filtered_transactions


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    :param transactions: Список транзакций
    :param reverse: Флаг обратной сортировки (по умолчанию True - по убыванию)
    :return: Отсортированный список транзакций
    """
    # Фильтруем транзакции, у которых есть дата
    transactions_with_date = [t for t in transactions if "date" in t]

    # Сортируем по дате
    sorted_transactions = sorted(
        transactions_with_date,
        key=lambda x: x["date"],
        reverse=reverse
    )

    # Добавляем транзакции без даты в конец
    transactions_without_date = [t for t in transactions if "date" not in t]

    return sorted_transactions + transactions_without_date
