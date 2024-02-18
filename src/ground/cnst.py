# region Константы
CURRENT_PROTOCOL_VERSION = '0.0.0.1 MVP'
""" Текущая версия протокола """

GENESIS_HEIGHT: int = 0
""" Высота первого блока (используется для заголовка генезис-блока) """

HASH_BIT_LENGTH: int = 256
""" Длина используемых хэшей (в битах) """

HASH_STR_LENGTH: int = int(HASH_BIT_LENGTH / 8)
""" Длина хэшей в строковом (шестнадцатеричном) представлении """

ZERO: str = '0'
""" Ноль (в виде строки) """

ZERO_HASH: str = ZERO * HASH_STR_LENGTH
""" Хэш из нулей (используется для заголовка генезис-блока) """

DEFAULT_DIFFICULTY: int = 2
""" Сложность майнинга (количество нулей вначале хэша)  """

UNKNOWN_NONCE: int = 0
""" Результат решения задачи майнинга (уникальный номер) """

DATETIME_FORMAT: str = '%d.%m.%Y %H:%M:%S.%f'
""" Человеко-понятный формат даты/времени """

DATETIME_BEGINNING: str = '01.01.2024 00:00:00.0'

MOSCOW_TIMEZONE: str = 'Europe/Moscow'

MINIMAL_DIFFICULTY: int = 1
""" Минимальная сложность """
# endregion
