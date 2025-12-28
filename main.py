"""
Пример использования модуля для чтения финансовых операций.
"""

from src.file_handlers import read_csv_file, read_excel_file


def main():
    try:
        # Чтение CSV файла
        csv_transactions = read_csv_file('data/transactions.csv')
        print(f"Прочитано {len(csv_transactions)} транзакций из CSV")

        # Чтение Excel файла
        excel_transactions = read_excel_file('data/transactions_excel.xlsx')
        print(f"Прочитано {len(excel_transactions)} транзакций из Excel")

        # Вывод первой транзакции из каждого файла
        if csv_transactions:
            print("\nПервая транзакция из CSV:")
            print(csv_transactions[0])

        if excel_transactions:
            print("\nПервая транзакция из Excel:")
            print(excel_transactions[0])

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()