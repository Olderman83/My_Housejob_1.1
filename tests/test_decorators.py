import pytest
import os
import tempfile
from src.decorators import log


def test_log_to_console_success(capsys):
    """Тест успешного выполнения с логированием в консоль"""

    @log()
    def add(a, b):
        return a + b

    result = add(1, 2)

    # Проверяем результат
    assert result == 3

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_to_console_error(capsys):
    """Тест ошибки с логированием в консоль"""

    @log()
    def divide(a, b):
        return a / b

    # Проверяем, что исключение пробрасывается
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "divide error" in captured.out
    assert "ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0)" in captured.out


def test_log_to_console_with_kwargs(capsys):
    """Тест с ключевыми аргументами"""

    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")

    assert result == "Hi, Alice!"
    captured = capsys.readouterr()
    assert "greet ok" in captured.out


# Тесты для логирования в файл
def test_log_to_file_success():
    """Тест успешного выполнения с логированием в файл"""

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        @log(filename=filename)
        def multiply(x, y):
            return x * y

        result = multiply(3, 4)

        # Проверяем результат
        assert result == 12

        # Проверяем запись в файл
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "multiply ok" in content
    finally:
        # Удаляем временный файл
        os.unlink(filename)


def test_log_to_file_error():
    """Тест ошибки с логированием в файл"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        @log(filename=filename)
        def raise_value_error(num):
            if num < 0:
                raise ValueError("Number must be positive")
            return num

        # Проверяем, что исключение пробрасывается
        with pytest.raises(ValueError):
            raise_value_error(-1)

        # Проверяем запись в файл
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "raise_value_error error" in content
            assert "ValueError" in content
            assert "Number must be positive" in content
            assert "Inputs: (-1,)" in content
    finally:
        # Удаляем временный файл
        os.unlink(filename)


def test_log_to_file_multiple_calls():
    """Тест нескольких вызовов с логированием в файл"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        @log(filename=filename)
        def power(base, exponent=2):
            return base ** exponent

        # Делаем несколько вызовов
        assert power(2) == 4
        assert power(3, 3) == 27

        # Проверяем, что все вызовы записаны
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 2
            assert all("power ok" in line for line in lines)
    finally:
        os.unlink(filename)


def test_log_preserves_function_metadata():
    """Тест, что декоратор сохраняет метаданные функции"""

    @log()
    def example_func(a: int, b: int) -> int:
        """Example function for testing."""
        return a + b

    # Проверяем сохранение метаданных
    assert example_func.__name__ == "example_func"
    assert example_func.__doc__ == "Example function for testing."
    assert example_func.__annotations__ == {'a': int, 'b': int, 'return': int}



