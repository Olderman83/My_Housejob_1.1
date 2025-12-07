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

##Модуль conftest
Модуль содержит фикстуры для функций тестирования


##Команда
user.name=Павел Руцкин
user.email=pavelru163@gmail.com
