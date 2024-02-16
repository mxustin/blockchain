""" Версия протокола. Спецификация: https://clck.ru/38jK47 """

from abc import ABC, abstractmethod
from multipledispatch import dispatch

from src.ground import errs
from src.ground import bits


def _undefined_version() -> tuple[int, int, int]:
    """ Возвращает кортеж из трех «-1» для того, чтобы пометить «мажор», «минор» и «патч» как неопределенные """
    return -1, -1, -1


class ProtocolVersionObserver(ABC):
    @abstractmethod
    def process_changing(self):
        ...


class ProtocolVersionShort:
    """ «Краткая версия» протокола (используется «Семантическое версионирование»: «мажор» — 2 бита, «минор» — 3 бита,
    «патч» — 3 бита) для «малого» заголовка. Данная версия, по сути, является смещением по трем параметрам по
    отношению к «Полной версии» (см. ниже) """

    @dispatch(int, int, int)
    def __init__(self, major: int = 0, minor: int = 0, patch: int = 0) -> None:
        """
        Инициализация «Краткой версии» через три целых числа: «мажор» (0..3), «минор» (0..7), «патч» (0..7),
        которые нужно рассматривать как «смещения» по отношению к соответствующим значениям последней
        актуальной «Полной версии»
        :param major: «Мажор»
        :param minor: «Минор»
        :param patch: «Патч»
        """
        # region Устанавливаем «неопределенные» значения
        self._major, self._minor, self._patch = _undefined_version()
        # endregion
        # region Обозначаем «наблюдателя»
        self._observer = None
        self._observer: ProtocolVersionObserver
        # endregion
        # region Устанавливаем значения с соответствующими проверками
        self.major = major
        self.minor = minor
        self.patch = patch
        # endregion

    @dispatch(bytearray)
    def __init__(self, raw_bytes: bytearray) -> None:
        """ Инициализация через чтение «сырых» байтов (должен поступить байтовый массив из одного байта, где
        2 бита — «мажор», 3 бита — «минор», 3 бита — «патч», которые нужно рассматривать как «смещения» по отношению к
        соответствующим значениям последней актуальной «Полной версии») """
        # region Обозначаем «наблюдателя»
        self._observer = None
        self._observer: ProtocolVersionObserver
        # endregion
        if len(raw_bytes) == 1:
            # region «Парсим» полученный байт и устанавливаем значения
            self._major = raw_bytes[0] >> 6                    # Старшие два бита — «мажор»
            self._minor = (raw_bytes[0] & 0b00111000) >> 3     # ... следующие три бита — «минор»
            self._patch = raw_bytes[0] & 0b00000111            # ... младшие три бита — «патч»
            # endregion
        else:
            # region Поднимаем исключение
            raise ValueError(errs.PVS_ONLY_ONE_BYTE_EXPECTED)
            # endregion

    def __repr__(self) -> str:
        """ Репрезентация (человеко-читаемое, наглядное представление объекта, который должен рассматриваться как
        смещение по отношению к последней актуальной «Полной версии») """
        # region Готовим «элементы»
        descr = f'The Short Version (shifts) of protocol (instance of {__class__.__name__}) is {self.as_str()}'
        mj = f'major shift: {self._major}'
        mn = f'minor shift: {self._minor}'
        pt = f'patch shift: {self._patch}'
        # endregion
        # region «Собираем» представление
        result = (f'{descr}:'
                  f'\n ▪️ {mj};'
                  f'\n ▪️ {mn};'
                  f'\n ▪️ {pt}.'
                  f'\nAs binary string: {self.as_binary_str()}. '
                  f'As bytes (in hexadecimal notation): {self.as_hex()}.')
        # endregion
        return result

    def __str__(self) -> str:
        """ Человеко-читаемое строковое представление (например, для JSON) """
        return self.as_str()

    def __lshift__(self, other: tuple[int, int, int]) -> None:
        """ Установка через операцию сдвига влево «<<» (на вход должен поступить кортеж из трех целых чисел, но с
        ограничениями: 2 бита на «мажор», и по 3 бита на «минор» и на «патч») """
        # region Устанавливаем значения, путем пере-использования методов
        self.major, self.minor, self.patch = other
        # endregion

    def _get_bytes(self) -> int:
        """ Возвращает один байт (2 бита - мажор, 3 бита - минор, 3 бита - патч) """
        # region Собираем наш единственный байт
        mj = self._major << 6                                  # Поднимаем «мажор» в старшие 2 бита
        mn = self._minor << 3                                  # Поднимаем «минор» в следующие 3 бита
        pt = self._patch                                       # Добавляем «патч» в последние 3 бита
        # endregion
        return mj + mn + pt

    def as_str(self) -> str:
        """ Строковое представление (для JSON, или для словарного представления) """
        return f'+{self._major}.+{self._minor}.+{self._patch}'

    def as_bytes(self) -> bytearray:
        """ Возвращает байтовый массив длиной в 1 байт, содержащий значения, которые должны рассматриваться как
        смещения для последней актуальной полной версии (2 бита - мажор, 3 бита - минор, 3 бита - патч) """
        return bytearray([self._get_bytes()])

    def as_hex(self) -> str:
        """ Возвращает текущее значение в виде строки, состоящей из шестнадцатеричных символов (1 байт = 2 символа) """
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
            if self._observer:
                self._observer.process_changing()
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
            if self._observer:
                self._observer.process_changing()
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
            if self._observer:
                self._observer.process_changing()
        else:
            raise ValueError(errs.PVS_PATCH_VALUE_ERROR)

    @property
    def observer(self) -> ProtocolVersionObserver:
        return self._observer

    @observer.setter
    def observer(self, value: ProtocolVersionObserver) -> None:
        if isinstance(value, ProtocolVersionObserver):
            self._observer = value
            self._observer.process_changing()


class ProtocolVersionFull:
    """ Полная версия протокола (мажор — 8 бит, минор — 4 бита, патч — 4 бита) для «большого» заголовка """

    @dispatch(int, int, int)
    def __init__(self, major: int = 0, minor: int = 1, patch: int = 0) -> None:
        """ Инициализация (установка начальных значений) через установку отдельно «мажора», «минора» и «патча» """
        # region Устанавливаем «неопределенные» значения
        self._major, self._minor, self._patch = _undefined_version()
        # endregion
        # region Обозначаем «наблюдателя»
        self._observer = None
        self._observer: ProtocolVersionObserver
        # endregion
        # region Устанавливаем значения с соответствующими проверками
        self.major = major
        self.minor = minor
        self.patch = patch
        # endregion

    @dispatch(bytearray)
    def __init__(self, raw_bytes: bytearray) -> None:
        """ Инициализация через чтение "сырых" байтов (должен поступить байтовый массив из двух байтов) """
        # region Обозначаем «наблюдателя»
        self._observer = None
        self._observer: ProtocolVersionObserver
        # endregion
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
            if self._observer:
                self._observer.process_changing()
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
            if self._observer:
                self._observer.process_changing()
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
            if self._observer:
                self._observer.process_changing()
        else:
            raise ValueError(errs.PVF_PATCH_VALUE_ERROR)

    @property
    def observer(self) -> ProtocolVersionObserver:
        return self._observer

    @observer.setter
    def observer(self, value: ProtocolVersionObserver) -> None:
        if isinstance(value, ProtocolVersionObserver):
            self._observer = value
            self._observer.process_changing()


class ProtocolVersion(ProtocolVersionObserver):
    """ «Фактическая» версия протокола — объект для хранения в памяти (не записывается в заголовки блоков) """

    def __init__(self, full: ProtocolVersionFull, short: ProtocolVersionShort) -> None:
        """

        :param full: Полная версия (объект)
        :param short: Краткая версия (объект)
        """
        self._full = None
        self._full: ProtocolVersionFull
        self._short = None
        self._short: ProtocolVersionShort
        self.full = full
        self.short = short
        self._major, self._minor, self._patch = _undefined_version()
        self._upd()

    def __repr__(self) -> str:
        descr = f'The Version of protocol (instance of {__class__.__name__}) is {self.as_str()}'
        mj = f'major version: {self._major}'
        mn = f'minor version: {self._minor}'
        pt = f'patch version: {self._patch}'
        result = (f'{descr}:'
                  f'\n ▪️ {mj};'
                  f'\n ▪️ {mn};'
                  f'\n ▪️ {pt}.')
        return result

    def __str__(self) -> str:
        """ Человеко-читаемое строковое представление (например, для JSON) """
        return self.as_str()

    def _upd(self) -> None:
        if self._full and self._short:
            self._major, self._minor, self._patch = self._full + self._short
        else:
            self._major, self._minor, self._patch = _undefined_version()

    def as_str(self) -> str:
        """ Строковое представление (для JSON, или для словарного представления) """
        return f'{self._major}.{self._minor}.{self._patch}'

    def process_changing(self):
        self._upd()

    @property
    def major(self) -> int:
        """ "Мажор" """
        return self._major

    @property
    def minor(self) -> int:
        """ "Минор" """
        return self._minor

    @property
    def patch(self) -> int:
        """ "Патч" """
        return self._patch

    @property
    def short(self) -> ProtocolVersionShort:
        return self._short

    @short.setter
    def short(self, value: ProtocolVersionShort) -> None:
        if isinstance(value, ProtocolVersionShort):
            self._short = value
            self._short.observer = self
            self._upd()

    @property
    def full(self) -> ProtocolVersionFull:
        return self._full

    @full.setter
    def full(self, value: ProtocolVersionFull) -> None:
        if isinstance(value, ProtocolVersionFull):
            self._full = value
            self._full.observer = self
            self._upd()
