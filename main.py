import os
import sys
from typing import Any, Dict, List, Optional

from src.bank_operations import process_bank_operations, process_bank_search
from src.file_handlers import read_csv_file, read_excel_file
from src.processing import filter_by_state, sort_by_date
from src.utils import read_json_file
from src.widget import get_date, mask_account_card

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def get_file_choice() -> tuple:
    """Получает выбор файла от пользователя."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Ваш выбор: ").strip()
        if choice in ["1", "2", "3"]:
            break
        print("Пожалуйста, введите 1, 2 или 3")

    file_types = {
        "1": ("json", "operations.json"),
        "2": ("csv", "transactions.csv"),
        "3": ("xlsx", "transactions_excel.xlsx")
    }

    file_type, default_file = file_types[choice]
    print(f"Для обработки выбран {file_type.upper()}-файл.")

    return file_type, default_file


def get_status_filter() -> str:
    """Получает статус фильтрации от пользователя."""
    available_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(available_statuses)}")
        status = input("Статус: ").strip().upper()

        if status in available_statuses:
            print(f"Операции отфильтрованы по статусу '{status}'")
            return status
        else:
            print(f"Статус операции '{status}' недоступен.")


def get_sort_preferences() -> tuple:
    """Получает настройки сортировки от пользователя."""
    sort_by_date_choice = None
    while True:
        sort_by_date_input = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()
        if sort_by_date_input in ["да", "нет"]:
            sort_by_date_choice = sort_by_date_input == "да"
            break
        print("Пожалуйста, введите 'Да' или 'Нет'")

    sort_order = None
    if sort_by_date_choice:
        while True:
            sort_order_input = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
            if sort_order_input in ["по возрастанию", "по убыванию"]:
                sort_order = sort_order_input
                break
            print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")

    return sort_by_date_choice, sort_order


def get_currency_filter() -> bool:
    """Получает настройку фильтрации по валюте от пользователя."""
    while True:
        currency_filter = input("\nВыводить только рублевые транзакции? Да/Нет: ").strip().lower()
        if currency_filter in ["да", "нет"]:
            return currency_filter == "да"
        print("Пожалуйста, введите 'Да' или 'Нет'")


def get_search_filter() -> Optional[str]:
    """Получает строку для поиска в описании от пользователя."""
    while True:
        search_choice = input(
            "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
        if search_choice in ["да", "нет"]:
            break
        print("Пожалуйста, введите 'Да' или 'Нет'")

    if search_choice == "да":
        search_string = input("Введите строку для поиска в описании: ").strip()
        return search_string if search_string else None

    return None


def filter_transactions_by_currency(transactions: List[Dict[str, Any]], rub_only: bool) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по валюте."""
    if not rub_only:
        return transactions

    filtered = []
    for transaction in transactions:
        currency = transaction.get('operationAmount', {}).get('currency', {}).get('code', '')
        if currency == 'RUB':
            filtered.append(transaction)

    return filtered


def display_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Выводит транзакции в отформатированном виде."""
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for i, transaction in enumerate(transactions, 1):
        print(f"Транзакция #{i}")
        date = get_date(transaction.get('date', ''))
        description = transaction.get('description', '')

        # Маскировка данных карты/счета
        from_info = transaction.get('from', '')
        to_info = transaction.get('to', '')

        if from_info:
            masked_from = mask_account_card(from_info)
        else:
            masked_from = "Не указано"

        masked_to = mask_account_card(to_info) if to_info else "Не указано"

        amount_info = transaction.get('operationAmount', {})
        amount = amount_info.get('amount', '0')
        currency = amount_info.get('currency', {}).get('code', '')

        print(f"{date} {description}")

        if from_info:
            print(f"Отправитель: {masked_from}")
        if to_info:
            print(f"Получатель: {masked_to}")

        print(f"Сумма: {amount} {currency}")
        print("-" * 50 + "\n")


def main() -> None:
    """Основная функция программы."""
    # Получаем выбор файла
    file_type, filename = get_file_choice()

    # Создаем папку data если её нет
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"\nСоздана папка '{data_dir}'. Пожалуйста, добавьте туда файлы с транзакциями:")
        print("1. operations.json - для JSON формата")
        print("2. transactions.csv - для CSV формата")
        print("3. transactions_excel.xlsx - для Excel формата")
        print("\nПосле добавления файлов перезапустите программу.")
        return

    file_path = os.path.join(data_dir, filename)

    # Читаем файл
    try:
        if file_type == "json":
            transactions = read_json_file(file_path)
        elif file_type == "csv":
            transactions = read_csv_file(file_path)
        else:  # xlsx
            transactions = read_excel_file(file_path)

        if transactions is None:
            print(f"\nФайл {filename} пуст или не содержит транзакций.")
            return

        print(f"\nУспешно прочитано {len(transactions)} транзакций из файла {filename}")

    except FileNotFoundError:
        print(f"\nФайл {filename} не найден в папке {data_dir}.")
        print(f"Пожалуйста, убедитесь что файл существует по пути: {os.path.abspath(file_path)}")
        return
    except Exception as e:
        print(f"\nОшибка при чтении файла: {e}")
        return

    if not transactions:
        print("\nФайл не содержит транзакций или пуст.")
        return

    # Фильтрация по статусу
    status = get_status_filter()
    filtered_transactions = filter_by_state(transactions, status)
    print(f"После фильтрации по статусу осталось {len(filtered_transactions)} транзакций")

    # Настройки сортировки
    sort_by_date_choice, sort_order = get_sort_preferences()
    if sort_by_date_choice:
        reverse = sort_order == "по убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, reverse)
        print(f"Транзакции отсортированы по дате ({sort_order})")

    # Фильтрация по валюте
    rub_only = get_currency_filter()
    filtered_transactions = filter_transactions_by_currency(filtered_transactions, rub_only)
    if rub_only:
        print(f"После фильтрации по рублевым транзакциям осталось {len(filtered_transactions)} транзакций")

    # Поиск по описанию
    search_string = get_search_filter()
    if search_string:
        filtered_transactions = process_bank_search(filtered_transactions, search_string)
        print(f"После поиска по слову '{search_string}' осталось {len(filtered_transactions)} транзакций")

    # Вывод результатов
    print("\n" + "=" * 50)
    print("РАСПЕЧАТЫВАЮ ИТОГОВЫЙ СПИСОК ТРАНЗАКЦИЙ...")
    print("=" * 50)
    display_transactions(filtered_transactions)

    # Дополнительно: подсчет категорий
    if filtered_transactions:
        categories = list(set(t.get('description', '') for t in filtered_transactions if t.get('description')))
        if categories:
            category_counts = process_bank_operations(filtered_transactions, categories)
            print("\nСТАТИСТИКА ПО КАТЕГОРИЯМ ОПЕРАЦИЙ:")
            print("-" * 30)
            for category, count in category_counts.items():
                print(f"{category}: {count} операций")
            print("-" * 30)


if __name__ == "__main__":
    main()
