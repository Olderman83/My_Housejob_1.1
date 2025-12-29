#Проект Домашняя работа.

##IT-отдел крупного банка делает новую фичу для личного кабинета клиента. 
Это виджет, который показывает несколько последних успешных банковских операций клиента.

##Проект предоставляет функции для фильтрации и сортировки банковских операций.

## Установка:

1. Клонируйте репозиторий:
'''
https://github.com/Olderman83/My_Housejob_1.1/tree/main
'''

2. Установите зависимости:
'''
pip install -r requirements.txt

##Модуль masks
Содержит функции маскировки данных кар и счетов.
"""Возвращает маску банковской карты:XXXX XX** **** XXXX"""
    card_number_str = str(card_number).replace(" ", "")

"""Возвращает маску банковского счета в формате:**ХХХХ"""
    account_number_str = str(account_number).replace(" ", "")

##Модуль widget
Принимает данные карт и возвращает с маскированным номером, и принимает строку с датой, и возвращает в 
определленом формате  
 """Принимает данные карты, возвращает строку с замаскированным номером"""

card_info_part = card_info.split()
number_part = card_info_part[-1]

 """Принимает строку с датой в формате
    "2024-03-11T02:26:18.671407" и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ" """

    split_date = date.split("T")
    date_part = split_date[0]

    year = date_part[0:4]
    month = date_part[5:7]
    day = date_part[8:10]

    return f"{day}.{month}.{year}"

##Модуль processing
Модуль принимает список словарей и возвращает список словарей имеющих ключ с сортировкой по дате
"""Функция принимает список словарей и опционально значение для ключа "state" (по умолчанию
    'EXECUTED'). Возвращает новый список словарей, содержащий только те словари, у которых ключ
    "state" соответствует указанному значению"""
 """Функция принимает список словарей и необязательный параметр, задающий порядок сортировки
    (по умолчанию — убывание). Возвращает новый список, отсортированный по дате"""
 def sort_by_date(dict_list: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
 return sorted(dict_list, key=lambda x: x["date"], reverse=reverse)

##Модуль generators 
Модуль, который содержит функции для работы с массивами транзакций через генераторы.



#Тестирование
Пакет tests содержит модули для тестирования кодов маскирования и сортировки карт.

##Модуль tests_masks
Модуль тестирует функции для маркировки номера карты и функции для маскировки аккаунта.
Пример:
def test_none_input():
    """Тестирование None ввода"""
    assert get_mask_card_number("None") == "None"

def test_get_mask_account_standard():
    """Тест стандартного случая с полным номером счета"""
    assert get_mask_account("12345678901234567890") == "**7890"



##Модуль tests_processing 
Модуль тестирует функции filter_by_state и sort_by_date.
Пример:
def test_only_canceled_transactions(
    only_canceled_transactions: List[Dict[str, Any]]
):
    """Тест с транзакциями только в одном состоянии (не EXECUTED)"""
    result = filter_by_state(only_canceled_transactions)
    assert result == []

@pytest.mark.parametrize("reverse,expected_order", [
        (True, ["2023-03-01", "2023-02-01", "2023-01-01"]),  # по убыванию
        (False, ["2023-01-01", "2023-02-01", "2023-03-01"]),  # по возрастанию
    ])
def test_sort_order(self, reverse, expected_order):
    """Тестирование правильности порядка сортировки"""
    dict_list = [
        {"date": "2023-01-01", "name": "A"},
        {"date": "2023-03-01", "name": "B"},
        {"date": "2023-02-01", "name": "C"}
        ]

    result = sort_by_date(dict_list, reverse)
    actual_order = [item["date"] for item in result]

    assert actual_order == expected_order

##Модуль tests_widget
Модуль тестирует функции mask_account_card и get_date.
Пример:
def test_visa_card_mask(self, card_data, expected_masked_data):
    """Тест маскировки номера Visa карты"""
    result = mask_account_card(card_data["visa_classic"])
    expected = expected_masked_data["visa_classic"]
    assert result == expected

def test_basic_date_conversion(self, sample_date_1):
    """Тест базового преобразования даты"""
    result = get_date(sample_date_1)
    assert result == "11.03.2024"

##Модуль tests_generators
filter_by_currency, transaction_descriptions, card_number_generator
Пример:
    def test_empty_transaction_list(self) -> None:
        """Тест с пустым списком транзакций"""
        result = list(filter_by_currency([], "USD"))
        assert len(result) == 0

    def test_with_fixture_transactions(self, sample_transactions1) -> None:
        """Тест с фикстурой из conftest.py"""
        result = list(transaction_descriptions(sample_transactions1))
        expected = ['Покупка', 'Продажа', 'Перевод']
        assert result == expected

    def test_generator_returns_iterator(self) -> None:
        """Проверка, что функция возвращает итератор"""
        result = card_number_generator(1, 5)
        assert hasattr(result, '__iter__')
        assert hasattr(result, '__next__')

#Декорирование

Модуль содержит декоратор `log` для логирования выполнения функций.

##Использование

`python
from decorators import log

#Примеры:
@log()
def my_function(x, y):
    return x + y


@log("myapp.log")
def another_function(x):
    return x * 2

##Модуль conftest
Модуль содержит фикстуры для функций тестирования

#Библиотеки

Модуль содержит модули utils external.api читающие JSON-файл и возвращает список словарей с данными о транзакциях.
            Если файл пустой, содержит не список или не найден, возвращается пустой список.И конвертируют сумму 
транзакции в рубли.
Содержит файлы для тестирования test_external_api.py и test_utils.py
Примеры: 
def test_convert_to_rubles_missing_amount():
    """Тест при отсутствии суммы."""
    transaction = {"currency": "RUB"}
    result = convert_to_rubles(transaction)
    assert result == 0.0

def test_read_json_file_not_found():
    """Тест для несуществующего файла."""
    result = read_json_file("/nonexistent/path/file.json")
    assert result == []
 
#Модуль работы с библиотеками

Модуль содержит два файла с данными операций в форматах CSV и EXCEL,файл с функция чтения этих форматов и файл тестирования функций
Загружены pandas и openpyxl
Пример:
def test_read_csv_file_not_found(self):
    """Тест ошибки при отсутствии файла."""
    with pytest.raises(FileNotFoundError):
        read_csv_file('nonexistent.csv')

def test_read_excel_file_not_found(self):
    """Тест ошибки при отсутствии файла."""
    with pytest.raises(FileNotFoundError):
        read_excel_file('nonexistent.xlsx')

##Модуль содержит файл bank_operations с функциями process_bank_operations и process_bank_search,которые 
ищут транзакции по заданной строке в описании с использованием регулярных выражений и подсчитывает количество 
банковских операций определенных категорий.Так же содержит файл с тестами к ним.
Пример:
def test_process_bank_search_partial_match(sample_transactions):
    result = process_bank_search(sample_transactions, "карт")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_process_bank_operations(sample_transactions):
    categories = ["Перевод организации", "Оплата услуг"]
    result = process_bank_operations(sample_transactions, categories)

    assert "Перевод организации" in result
    assert result["Перевод организации"] == 2
    assert "Оплата услуг" in result
    assert result["Оплата услуг"] == 1
#Файл main для запуска взаимосвязей функций
##Команда
user.name=Павел Руцкин
user.email=pavelru163@gmail.com
