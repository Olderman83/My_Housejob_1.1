import csv
import pandas as pd
from typing import List, Dict, Any


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
        Читает финансовые операции из CSV-файла."""
    transactions = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                # Преобразуем данные к правильным типам
                transaction = {
                    'id': int(row['id']),
                    'state': row['state'],
                    'date': row['date'],
                    'amount': float(row['amount']),
                    'currency_name': row['currency_name'],
                    'currency_code': row['currency_code'],
                    'from': row['from'] if row['from'] else None,
                    'to': row['to'],
                    'description': row['description']
                }
                transactions.append(transaction)

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except KeyError as e:
        raise ValueError(f"Отсутствует обязательное поле в CSV файле: {e}")
    except ValueError as e:
        raise ValueError(f"Ошибка преобразования данных: {e}")

    return transactions


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из Excel файла."""

    try:
        # Читаем Excel файл с помощью pandas
        df = pd.read_excel(file_path, engine='openpyxl')

        # Преобразуем DataFrame в список словарей
        transactions = []

        for _, row in df.iterrows():
            transaction = {
                'id': int(row['id']),
                'state': str(row['state']),
                'date': str(row['date']),
                'amount': float(row['amount']),
                'currency_name': str(row['currency_name']),
                'currency_code': str(row['currency_code']),
                'from': str(row['from']) if pd.notna(row['from']) else None,
                'to': str(row['to']),
                'description': str(row['description'])
            }
            transactions.append(transaction)

        return transactions

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except KeyError as e:
        raise ValueError(f"Отсутствует обязательная колонка в Excel файле: {e}")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel файла: {e}")
