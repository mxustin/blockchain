""" Версия протокола. Спецификация: https://clck.ru/38jK47 """

from multipledispatch import dispatch

from src.ground import errs
from src.ground import bits


class ProtocolVersionShort:
    """ Краткая версия протокола (мажор — 2 бита, минор — 3 бита, патч — 3 бита) для «малого» заголовка.
    Данная версия, по сути, является смещением по отношению к «Полной версии» """

    @dispatch(int, int, int)
    def __init__(self, major: int = 0, minor: int = 0, patch: int = 0):
        """ Инициализация краткой версии через три целых числа: "мажор", "минор", "патч", которые нужно
        рассматривать как "сдвиг" по отношению к значениям последней актуальной полной версии """
        self._major: int = -1  # Признак того, что значение не установлено
        self.major = major
        self._minor: int = -1  # Признак того, что значение не установлено
        self.minor = minor
        self._patch: int = -1  # Признак того, что значение не установлено
        self.patch = patch

    @dispatch(bytearray)
    def __init__(self, raw_bytes: bytearray) -> None:
        """ Инициализация через чтение "сырых" байтов (должен поступить байтовый массив из одного байта, где
        2 бита - мажор, 3 бита - минор, 3 бита - патч, которые нужно рассматривать как сдвиг по отношению к
        значениям последней актуальной версии) """
        if len(raw_bytes) == 1:
            self._major = raw_bytes[0] >> 6
            self._minor = (raw_bytes[0] & 0b00111000) >> 3
            self._patch = raw_bytes[0] & 0b00000111
        else:
            raise ValueError(errs.PVS_ONLY_ONE_BYTE_EXPECTED)

    def __repr__(self) -> str:
        """ Репрезентация (человеко-читаемое, наглядное представление объекта, который должен рассматриваться как
        сдвиг по отношению к последней актуальной полной версии) """
        descr = f'The Short Version (shifts) of protocol (instance of {__class__.__name__}) is {self.as_str()}'
        ...  # todo ...
        mj = f'major shift: {self._major}'
        mn = f'minor shift: {self._minor}'
        pt = f'patch shift: {self._patch}'
        result = (f'{descr}:'
                  f'\n ▪️ {mj};'
                  f'\n ▪️ {mn};'
                  f'\n ▪️ {pt}.'
                  f'\nAs binary string: {self.as_binary_str()}. As bytes (in hexadecimal notation): {self.as_hex()}.')
        return result

    def __str__(self) -> str:
        """ Человеко-читаемое строковое представление (например, для JSON) """
        return self.as_str()

    def __lshift__(self, other):
        """ Установка через << (на вход должен поступить кортеж из трех целых чисел, но с ограничениями:
        2 бита на мажор, и по 3 бита на минор и на патч) """
        self.major, self.minor, self.patch = other

    # Метод __iadd__ для краткой версии не требуется

    def _get_bytes(self):
        """ Возвращает один байт (2 бита - мажор, 3 бита - минор, 3 бита - патч) """
        mj = self._major << 6
        mn = self._minor << 3
        pt = self._patch
        return mj + mn + pt

    def as_str(self) -> str:
        """ Строковое представление (для JSON, или для словарного представления) """
        return f'+{self._major}.+{self._minor}.+{self._patch}'

    def as_bytes(self) -> bytearray:
        """ Возвращает байтовый массив длиной в 1 байт, содержащий значения, которые должны рассматриваться как
        смещения для последней актуальной полной версии (2 бита - мажор, 3 бита - минор, 3 бита - патч) """
        return bytearray([self._get_bytes()])

    def as_hex(self):
        return self.as_bytes().hex()

    def as_binary_str(self) -> str:  # noqa
        return bits.byte_as_bits_str(self.as_bytes()[0])

    @property
    def major(self) -> int:
        """ Смещение для "Мажора" (по отношению к последней актуальной полной версии) """
        return self._major

    @major.setter
    def major(self, value) -> None:
        """ Установка значения смещения для "Мажора" (по отношению к последней актуальной полной версии) """
        if isinstance(value, int) and (0 <= value <= 3):
            self._major = value
        else:
            raise ValueError(errs.PVS_MAJOR_VALUE_ERROR)

    @property
    def minor(self) -> int:
        """ Смещение для "Минора" (по отношению к последней актуальной полной версии) """
        return self._minor

    @minor.setter
    def minor(self, value) -> None:
        """ Установка значения смещения для "Минора" (по отношению к последней актуальной полной версии) """
        if isinstance(value, int) and (0 <= value <= 7):
            self._minor = value
        else:
            raise ValueError(errs.PVS_MINOR_VALUE_ERROR)

    @property
    def patch(self) -> int:
        """ Смещение для "Патча" (по отношению к последней актуальной полной версии) """
        return self._patch

    @patch.setter
    def patch(self, value) -> None:
        """ Установка значения смещения для "Патча" (по отношению к последней актуальной полной версии) """
        if isinstance(value, int) and (0 <= value <= 7):
            self._patch = value
        else:
            raise ValueError(errs.PVS_PATCH_VALUE_ERROR)


class ProtocolVersionFull:
    """ Полная версия протокола (мажор — 8 бит, минор — 4 бита, патч — 4 бита) для «большого» заголовка """

    @dispatch(int, int, int)
    def __init__(self, major: int = 0, minor: int = 1, patch: int = 0) -> None:
        """ Инициализация (установка начальных значений) через установку "мажора", "минора" и "патча" """
        self._major: int = -1  # Признак того, что значение не установлено
        self.major = major
        self._minor: int = -1  # Признак того, что значение не установлено
        self.minor = minor
        self._patch: int = -1  # Признак того, что значение не установлено
        self.patch = patch

    @dispatch(bytearray)
    def __init__(self, raw_bytes: bytearray) -> None:
        """ Инициализация через чтение "сырых" байтов (должен поступить байтовый массив из двух байтов) """
        if len(raw_bytes) == 2:
            self._major = raw_bytes[0]
            self._minor = raw_bytes[1] >> 4
            self._patch = raw_bytes[1] & 0b00001111
        else:
            raise ValueError(errs.PVF_BYTE_ARRAY_HAS_INCORRECT_LENGTH)

    def __repr__(self) -> str:
        """ Репрезентация (человеко-читаемое, наглядное представление объекта) """
        descr = f'The Full Version of protocol (instance of {__class__.__name__}) is {self.as_str()}'
        mj = f'major: {self._major}'
        mn = f'minor: {self._minor}'
        pt = f'patch: {self._patch}'
        result = (f'{descr}:'
                  f'\n ▪️ {mj};'
                  f'\n ▪️ {mn};'
                  f'\n ▪️ {pt}.'
                  f'\nAs binary string: {self.as_binary_str()}. As bytes (in hexadecimal notation): {self.as_hex()}.')
        return result

    def __str__(self) -> str:
        """ Человеко-читаемое строковое представление (например, для JSON) """
        return self.as_str()

    def __lshift__(self, other):
        """ Установка через << (на вход должен поступить кортеж из трех целых чисел) """
        self.major, self.minor, self.patch = other

    def __add__(self, other: ProtocolVersionShort):
        """ Метод для добавления «краткой версии» в качестве смещения, чтобы получить реальную полную актуальную
        версию для конкретного блока """
        return self.major + other.major, self.minor + other.minor, self.patch + other.patch

    def _minor_is_correct(self, value):
        """ Проверка: является ли минорная версия корректной """
        # На "минор" выделяется 4 бита, то есть, в общем случае, от 0 до 15, но если "мажор" = 0, то минор не должен
        # начинаться с нуля (минимальная версия: 0.1.0, и не может быть 0.0.0, например)
        minor_minimal = 0 if self._major > 0 else 1
        return isinstance(value, int) and (minor_minimal <= value <= 15)

    def _get_bytes(self):
        """ Возвращает два байта: "мажор" (первый байт) и "минор" с "патчем" (второй байт) """
        first_byte = self._major
        second_byte = self._minor << 4
        second_byte += self._patch
        return first_byte, second_byte

    def as_str(self) -> str:
        """ Строковое представление (для JSON, или для словарного представления) """
        return f'{self._major}.{self._minor}.{self._patch}'

    def as_bytes(self) -> bytearray:
        """ Возвращает байтовый массив """
        # ⚠️ Не знаю, почему, но при значении minor = 2, 3, 4, 5, 6, 7 отображается какая-то шляпа, хотя в других
        # представлениях все нормально. Других косяков не было обнаружено, и на уровне данных, вроде бы, все норм,
        # но print(f'  Bytes: {ver.as_bin()}') выводит что-то странное при указанных значениях
        a, b = self._get_bytes()
        return bytearray([a, b])

    def as_hex(self):
        return self.as_bytes().hex()

    def as_binary_str(self) -> str:
        a, b = self._get_bytes()
        return bits.byte_as_bits_str(a) + bits.byte_as_bits_str(b)

    @property
    def major(self) -> int:
        """ "Мажор" """
        return self._major

    @major.setter
    def major(self, value) -> None:
        """ Установка значения "Мажора" """
        if isinstance(value, int) and (0 <= value <= 255):
            self._major = value
        else:
            raise ValueError(errs.PVF_MAJOR_VALUE_ERROR)

    @property
    def minor(self) -> int:
        """ "Минор" """
        return self._minor

    @minor.setter
    def minor(self, value) -> None:
        """ Установка значения "Минора" """
        if self._minor_is_correct(value):
            self._minor = value
        else:
            raise ValueError(errs.PVF_MINOR_VALUE_ERROR)

    @property
    def patch(self) -> int:
        """ "Патч" """
        return self._patch

    @patch.setter
    def patch(self, value) -> None:
        """ Установка значения "Патча" """
        if isinstance(value, int) and (0 <= value <= 15):
            self._patch = value
        else:
            raise ValueError(errs.PVF_PATCH_VALUE_ERROR)
