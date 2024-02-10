import sys


def dict_size_in_bytes(obj: dict) -> int:
    """ Возвращает размер полученного словаря в байтах """
    return sys.getsizeof(obj)
