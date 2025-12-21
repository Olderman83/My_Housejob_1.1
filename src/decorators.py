import functools
from datetime import datetime
from typing import Any, Callable


def log(filename: str = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Формируем информацию о вызове
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                log_message = f"{timestamp} - {func_name} ok\n"

                # Записываем лог
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_type = type(e).__name__
                error_message = str(e)
                args_str = str(args)
                kwargs_str = str(kwargs)

                log_message = (
                    f"{timestamp} - {func_name} error: {error_type} - {error_message}. "
                    f"Inputs: {args_str}, {kwargs_str}\n"
                )

                # Записываем лог
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator
