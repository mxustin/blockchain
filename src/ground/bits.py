""" Операции с отдельными битами и битовыми строками """

import array
from src.ground import errs


def byte_bits_to_int(byte_bits: str):
    if len(byte_bits) <= 8:                                    # отбрасываем, что не поместится в беззнаковый байт
        i = int(byte_bits, 2)                                  # преобразуем в целое (основание = 2)
        return i
    else:
        raise ValueError(errs.BITS_NOT_BYTE)


def get_bit(value: int, pos: int) -> str:
    """ Получить отдельный бит в конкретном значении (значение может быть любого размера int) """
    return str(value >> pos & 1)                               # сдвигаем на нужное количество бит и смотрим, что там


def byte_as_bits_str(value: int) -> str:
    """ Получить битовую строку длинной в один байт (с ведущими нулями) """
    if 0 <= value <= 255:                                      # отбрасываем, что не поместится в беззнаковый байт
        result = 'XXXXXXXX'                                    # резервируем шаблон длиной 8 символов
        for pos in range(8):                                   # для всех значений от 0 до 7:
            bit = get_bit(value, pos)                          # - получаем бит
            np = 7 - pos                                       # - инвертируем позицию
            result = result[:np] + bit + result[np + 1:]       # - записываем в инвертированную позицию в шаблоне
        return result
    else:
        raise ValueError(errs.BITS_NOT_BYTE)
