import json
import os
import tempfile
from unittest.mock import mock_open, patch

from src.utils import read_json_file


def test_read_json_file_valid():
    """Тест для корректного JSON-файла."""
    # Создаем временный файл с корректными данными
    data = [
        {"id": 1, "amount": 100, "currency": "RUB"},
        {"id": 2, "amount": 200, "currency": "USD"}
    ]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name

    try:
        result = read_json_file(temp_path)
        assert result == data
        assert len(result) == 2
    finally:
        os.unlink(temp_path)


def test_read_json_file_empty():
    """Тест для пустого файла."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        result = read_json_file(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_read_json_file_not_list():
    """Тест для файла, содержащего не список."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"not": "a list"}, f)
        temp_path = f.name

    try:
        result = read_json_file(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_read_json_file_not_found():
    """Тест для несуществующего файла."""
    result = read_json_file("/nonexistent/path/file.json")
    assert result == []


def test_read_json_file_invalid_json():
    """Тест для файла с некорректным JSON."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json content")
        temp_path = f.name

    try:
        result = read_json_file(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


@patch('builtins.open')
@patch('os.path.exists')
def test_read_json_file_with_mock(mock_exists, mock_open_file):
    """Тест с использованием mock."""
    mock_exists.return_value = True
    mock_data = [{"id": 1, "amount": 100}]

    # Создаем мок для файлового объекта
    mock_file = mock_open_file.return_value.__enter__.return_value

    # Важно: патчить json.load нужно вместе с остальными декораторами
    with patch('json.load') as mock_json_load:
        mock_json_load.return_value = mock_data

        result = read_json_file("dummy_path.json")
