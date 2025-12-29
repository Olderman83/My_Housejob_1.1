import pytest
from unittest.mock import mock_open, patch
import pandas as pd
from src.file_handlers import read_csv_file, read_excel_file


class TestReadCSVFile:
    """Тесты для функции чтения CSV файлов."""


    def test_read_csv_file_not_found(self):
        """Тест ошибки при отсутствии файла."""
        with pytest.raises(FileNotFoundError):
            read_csv_file('nonexistent.csv')

    def test_read_csv_file_invalid_format(self):
        """Тест ошибки при неверном формате файла."""
        csv_content = """id;state;date;amount
650703;EXECUTED;2023-09-05T11:30:32Z;16210"""

        with patch('builtins.open', mock_open(read_data=csv_content)):
            with pytest.raises(ValueError):
                read_csv_file('invalid.csv')


class TestReadExcelFile:
    """Тесты для функции чтения Excel файлов."""

    def test_read_excel_file_success(self, mocker):
        """Тест успешного чтения Excel файла."""
        # Создаем тестовый DataFrame
        test_data = pd.DataFrame({
            'id': [650703, 3598919],
            'state': ['EXECUTED', 'CANCELED'],
            'date': ['2023-09-05T11:30:32Z', '2020-12-06T23:00:58Z'],
            'amount': [16210.0, 29740.0],
            'currency_name': ['Sol', 'Peso'],
            'currency_code': ['PEN', 'COP'],
            'from': ['Счет 58803664561298323391', None],
            'to': ['Счет 39745660563456619397', 'Discover 0720428384694643'],
            'description': ['Перевод организации', 'Перевод с карты на карту']
        })

        # Мокаем pandas.read_excel
        mock_read_excel = mocker.patch('pandas.read_excel')
        mock_read_excel.return_value = test_data

        result = read_excel_file('dummy.xlsx')

        assert len(result) == 2
        assert result[0]['id'] == 650703
        assert result[0]['state'] == 'EXECUTED'
        assert result[0]['from'] == 'Счет 58803664561298323391'
        assert result[1]['from'] is None

    def test_read_excel_file_not_found(self):
        """Тест ошибки при отсутствии файла."""
        with pytest.raises(FileNotFoundError):
            read_excel_file('nonexistent.xlsx')

    def test_read_excel_file_invalid_columns(self, mocker):
        """Тест ошибки при отсутствии обязательных колонок."""
        test_data = pd.DataFrame({
            'id': [650703],
            'state': ['EXECUTED']
            # Отсутствуют остальные обязательные колонки
        })

        mock_read_excel = mocker.patch('pandas.read_excel')
        mock_read_excel.return_value = test_data

        with pytest.raises(ValueError):
            read_excel_file('invalid.xlsx')
