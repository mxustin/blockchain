import json


def dict_to_json_str(source: dict) -> str:
    """ Возвращает полученный объект в виде строки JSON """
    # todo Реализовать проверки и перехват возможных исключений
    return json.dumps(source)
