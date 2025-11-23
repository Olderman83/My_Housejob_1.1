from typing import List, Dict, Any
from datetime import datetime

def filter_by_state(transactions, state = "EXECUTED") -> list:
    """Фильтрует список словарей по значению ключа "state" """
    filtered_list = []
    for transaction in transactions:
        if transaction.get("state") == state:
            filtered_list.append(transaction)
    return filtered_list






