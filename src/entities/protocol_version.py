""" Версия протокола. Спецификация: https://clck.ru/38jK47 """

from multipledispatch import dispatch

from src.ground import errs
from src.ground import bits


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
