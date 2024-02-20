"""
Вспомогательный модуль для «Версии протокола»
"""

from src.entities.protocol_version import pv_cnst


def undefined_version() -> tuple[int, int, int]:
    """
    Предоставляет кортеж из трех «-1»

    :return: Возвращает кортеж из трех «-1» (см. pv_cnst) для того, чтобы пометить «мажор», «минор» и «патч» как
    неопределенные
    """

    return pv_cnst.UNDEF_MAJOR, pv_cnst.UNDEF_MINOR, pv_cnst.UNDEF_PATCH


def bytearray_length_for_short_version_is_correct(barr: bytearray) -> bool:
    """
    Проверяет корректность длины массива байтов для «Краткой» версии

    :return: True, если длина массива байтов составляет 1
    """

    return len(barr) == pv_cnst.CORRECT_BYTEARRAY_LENGTH_FOR_SHORT_VERSION


def major_for_short_version_from_byte(b: int) -> int:
    """
    Выделяет старшие два бита из байта (чтобы получить «Мажор»)

    :param b: Исходный байт (в котором должны быть упакованы значения для «Краткой версии»)
    :return: «Мажор», выделенный из исходного байта (старшие 2 бита)
    """

    return b >> pv_cnst.MAJOR_R_SHIFT_FOR_SHORT_VERSION


def minor_for_short_version_from_byte(b: int) -> int:
    """
    Выделяет биты с 5 по 3 из байта (чтобы получить «Минор»)

    :param b: Исходный байт (в котором должны быть упакованы значения для «Краткой версии»)
    :return: «Минор», выделенный из исходного байта (биты с 5 по 3)
    """

    return (b & pv_cnst.MINOR_MASK_FOR_SHORT_VERSION) >> pv_cnst.MINOR_R_SHIFT_FOR_SHORT_VERSION


def patch_for_short_version_from_byte(b: int) -> int:
    """
    Выделяет биты со 2 по 0 из байта (чтобы получить «Патч»)

    :param b: Исходный байт (в котором должны быть упакованы значения для «Краткой версии»)
    :return: «Патч», выделенный из исходного байта (биты со 2 по 0)
    """

    return b & pv_cnst.PATCH_MASK_FOR_SHORT_VERSION


def decode_short_version(b: int) -> tuple[int, int, int]:
    """
    Позволяет получить «Краткую версию» («Минор», «Мажор» и «Патч») из байта

    :param b: Исходный байт (в котором должны быть упакованы значения для «Краткой версии»)
    :return: Кортеж, содержащий «Минор», «Мажор» и «Патч»
    """

    return (major_for_short_version_from_byte(b),
            minor_for_short_version_from_byte(b),
            patch_for_short_version_from_byte(b))


def major_for_short_version_to_byte(value: int) -> int:
    """
    Позволяет упаковать «Мажор» в первые два бита возвращаемого байта

    :param value: Текущее значение «Мажора»
    :return: Байт, в котором в первые два бита записано значение «Мажора»
    """

    return value << pv_cnst.MAJOR_L_SHIFT_FOR_SHORT_VERSION


def minor_for_short_version_to_byte(value: int) -> int:
    """
    Позволяет упаковать «Минор» в биты с 5 по 3 возвращаемого байта

    :param value: Текущее значение «Минора»
    :return: Байт, в котором в биты с 5 по 3 записано значение «Мажора»
    """

    return value << pv_cnst.MINOR_L_SHIFT_FOR_SHORT_VERSION


def patch_for_short_version_to_byte(value: int) -> int:
    """
    Позволяет упаковать «Патч» в биты со 2 по 0 возвращаемого байта (ну, на самом деле, оставляет все как есть, потому
    что там и так должно быть значение, находящееся в битах со 2 по 0;
    ⚠️ этот метод реализован просто для единообразия)

    :param value: Текущее значение «Патча»
    :return: Байт, в котором в биты со 2 по 0 записано значение «Патча»
    """

    return value


def encode_short_version(major: int, minor: int, patch: int) -> int:
    """
    Позволяет закодировать в одном байте «Краткую версию» из соответствующих значений «Мажора», «Минора» и «Патча»

    :param major: «Мажор»
    :param minor: «Минор»
    :param patch: «Патч»
    :return: Возвращает 1 байт, где биты 7 и 6 — «Мажор», с 5 по 3-й биты — «Минор» и биты со 2 по 0 — «Патч»
    """

    return (major_for_short_version_to_byte(major) +
            minor_for_short_version_to_byte(minor) +
            patch_for_short_version_to_byte(patch))


def major_for_short_version_is_correct(value: int) -> bool:
    """
    Проверяет корректность значения «Мажора» для «Краткой версии» (должно быть в интервале от 0 до 3, т.е., 2 бита)

    :param value: Значение «Мажора» на проверку
    :return: True, если значение «Мажора» корректно
    """

    return (isinstance(value, int) and
            (pv_cnst.MAJOR_FOR_SHORT_VERSION_MIN <= value <= pv_cnst.MAJOR_FOR_SHORT_VERSION_MAX))


def minor_for_short_version_is_correct(value: int) -> bool:
    """
    Проверяет корректность значения «Минора» для «Краткой версии» (должно быть в интервале от 0 до 7, т.е., 3 бита)

    :param value: Значение «Минора» на проверку
    :return: True, если значение «Минора» корректно
    """

    return (isinstance(value, int) and
            (pv_cnst.MINOR_FOR_SHORT_VERSION_MIN <= value <= pv_cnst.MINOR_FOR_SHORT_VERSION_MAX))


def patch_for_short_version_is_correct(value: int) -> bool:
    """
    Проверяет корректность значения «Патча» для «Краткой версии» (должно быть в интервале от 0 до 7, т.е., 3 бита)

    :param value: Значение «Патча» на проверку
    :return: True, если значение «Патча» корректно
    """

    return (isinstance(value, int) and
            (pv_cnst.PATCH_FOR_SHORT_VERSION_MIN <= value <= pv_cnst.PATCH_FOR_SHORT_VERSION_MAX))
