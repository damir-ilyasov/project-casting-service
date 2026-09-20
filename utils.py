"""Вспомогательные функции безопасного ввода данных пользователем."""


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число.

    При некорректном вводе запрос повторяется.

    :param prompt: текст приглашения к вводу
    :return: введённое целое число
    """
    while True:
        raw_value = input(prompt)
        try:
            return int(raw_value)
        except ValueError:
            print("Введите целое число, попробуйте снова")


def input_nonempty_str(prompt: str) -> str:
    """Запросить у пользователя непустую строку.

    При пустом вводе запрос повторяется.

    :param prompt: текст приглашения к вводу
    :return: введённая строка без пробелов по краям
    """
    while True:
        raw_value = input(prompt).strip()
        if raw_value:
            return raw_value
        print("Значение не может быть пустым, попробуйте снова")
