"""
Класс «Краткая версия» содержит в себе «смещения» относительно последней актуальной полной версии.

Спецификация: https://clck.ru/38uZ7g
"""

from multipledispatch import dispatch

from src.entities.protocol_version import pv_observer as pvo
from src.entities.protocol_version import pv_hlpr
from src.entities.protocol_version import pv_errs
from src.entities.protocol_version import pv_cnst

from src.ground import bits


class PVShort:
    """
    «Краткая версия» протокола (используется «Семантическое версионирование»: «мажор» — 2 бита, «минор» — 3 бита,
    «патч» — 3 бита) для «малого» заголовка. Данная версия, по сути, является смещением по трем параметрам по
    отношению к «Полной версии». Записывается в первый байт «Малого» заголовка
    """

    @dispatch(int, int, int)
    def __init__(self,
                 major: int = pv_cnst.DEF_MAJOR_SHIFT,
                 minor: int = pv_cnst.DEF_MINOR_SHIFT,
                 patch: int = pv_cnst.DEF_PATCH_SHIFT) -> None:
        """
        Инициализация «Краткой версии» через три целых числа: «мажор» (0..3), «минор» (0..7), «патч» (0..7),
        которые нужно рассматривать как «смещения» по отношению к соответствующим значениям последней
        актуальной «Полной версии»

        :param major: «Мажор» (смещение)
        :param minor: «Минор» (смещение)
        :param patch: «Патч» (смещение)
        :return: Возвращаемые значения не определены
        """

        # region Устанавливаем «неопределенные» значения
        self._major, self._minor, self._patch = pv_hlpr.undefined_version()
        # endregion
        # region Обозначаем «наблюдателя»
        self._observer = None
        self._observer: pvo.PVObserver
        # endregion
        # region Устанавливаем значения с соответствующими проверками
        self.major = major
        self.minor = minor
        self.patch = patch
        # endregion

    @dispatch()
    def __init__(self) -> None:
        """
        Инициализация «Краткой версии» без параметров (то есть, с параметрами по умолчанию)

        :return: Возвращаемые значения не определены
        """

        self.__init__(pv_cnst.DEF_MAJOR_SHIFT, pv_cnst.DEF_MINOR_SHIFT, pv_cnst.DEF_PATCH_SHIFT)

    @dispatch(bytearray)
    def __init__(self, raw_bytes: bytearray) -> None:
        """
        Инициализация через чтение «сырых» байтов (должен поступить байтовый массив из одного байта, где
        2 бита — «мажор», 3 бита — «минор», 3 бита — «патч», которые нужно рассматривать как «смещения» по отношению к
        соответствующим значениям последней актуальной «Полной версии»)

        :param raw_bytes: «Мажор» (смещение), «Минор» (смещение) и «Патч» (смещение), упакованные в 1 байт
        :return: Возвращаемые значения не определены
        """

        # region Устанавливаем «неопределенные» значения
        self._major, self._minor, self._patch = pv_hlpr.undefined_version()
        # endregion
        # region Обозначаем «наблюдателя»
        self._observer = None
        self._observer: pvo.PVObserver
        # endregion
        if pv_hlpr.bytearray_length_for_short_version_is_correct(raw_bytes):
            # region «Парсим» полученный байт и устанавливаем значения
            b = raw_bytes[pv_cnst.FIRST_BYTE]
            self._major, self._minor, self._patch = pv_hlpr.decode_short_version(b)
            # endregion
        else:
            # region Поднимаем исключение
            raise ValueError(pv_errs.PVS_ONLY_ONE_BYTE_EXPECTED)
            # endregion

    def __repr__(self) -> str:
        """
        Репрезентация (человеко-читаемое, наглядное представление объекта, который должен рассматриваться как
        смещение по отношению к последней актуальной «Полной версии»)

        :return: Строка с описанием объекта
        """

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
        """
        Человеко-читаемое строковое представление (например, для JSON)

        :return: Строковое представление (например, "+0.+0.+0")
        """

        return self.as_str()

    def __lshift__(self, other: tuple[int, int, int]) -> None:
        """
        Установка через операцию сдвига влево «<<» (на вход должен поступить кортеж из трех целых чисел, но с
        ограничениями: 2 бита на «мажор», и по 3 бита на «минор» и на «патч»)

        :param other: Кортеж, состоящих из «Мажора», «Минора» и «Патча»
        :return: Возвращаемые значения не определены
        """

        # region Устанавливаем значения, путем пере-использования сеттеров для соответствующих свойств
        self.major, self.minor, self.patch = other
        # endregion

    def _get_bytes(self) -> int:
        """
        Возвращает один байт (2 бита — «Мажор», 3 бита — «Минор», 3 бита — «Патч»)

        ⚠️ Несмотря на то, что здесь возвращается только один байт, переименовывать этот метод не нужно. Одноименный
        метод используется для «Полной версии». Там возвращается 2 байта. Поэтому тут хотелось бы соблюсти единообразие

        :return: Один байт, в котором упакованы «Мажор», «Минор» и «Патч»
        """

        return pv_hlpr.encode_short_version(self._major, self._minor, self._patch)

    def _notify_observer(self) -> None:
        """
        Если «Наблюдатель» определен, вызывается метод process_changing у «Наблюдателя»

        :return: Возвращаемые значения не определены
        """

        if self._observer:
            self._observer.process_changing()

    def as_str(self) -> str:
        """
        Строковое представление (для JSON, или для словарного представления)

        :return: Строковое, человеко-понятное представление, например, «+0.+0.+0»
        """

        return f'+{self._major}.+{self._minor}.+{self._patch}'

    def as_bytes(self) -> bytearray:
        """
        Возвращает байтовый массив длиной в 1 байт, содержащий значения, которые должны рассматриваться как
        смещения для последней актуальной полной версии (2 бита — «Мажор», 3 бита — «Минор», 3 бита — «Патч»)

        :return: Байтовый массив длиной в один байт, в котором упакованы «Мажор», «Минор» и «Патч»
        """

        return bytearray([self._get_bytes()])

    def as_hex(self) -> str:
        """
        Возвращает текущее значение в виде строки, состоящей из шестнадцатеричных символов (1 байт = 2 символа)

        :return: Байт в шестнадцатеричной форме, в котором упакованы «Мажор», «Минор» и «Патч»
        """

        return self.as_bytes().hex()

    def as_binary_str(self) -> str:
        """
        Возвращает текущее значение в виде строки из нулей и единиц (длиной в 1 байт)

        :return: Байт, в котором упакованы «Мажор», «Минор» и «Патч», в строковом представлении
        """

        return bits.byte_as_bits_str(self.as_bytes()[0])

    @property
    def major(self) -> int:
        """
        Значение для «Мажора» (смещение по отношению к последней актуальной «Полной версии»)

        :return: Текущее значение «Мажора»
        """

        return self._major

    @major.setter
    def major(self, value) -> None:
        """
        Установка значения для «Мажора» (смещение по отношению к последней актуальной «Полной версии»)

        :param value: Устанавливаемое значение «Мажора»
        :return: Возвращаемое значение не определено
        """

        if pv_hlpr.major_for_short_version_is_correct(value):
            self._major = value
            self._notify_observer()
        else:
            raise ValueError(pv_errs.PVS_MAJOR_VALUE_ERROR)

    @property
    def minor(self) -> int:
        """
        Значение для «Минора» (смещение по отношению к последней актуальной «Полной версии»)

        :return: Текущее значение «Минора»
        """

        return self._minor

    @minor.setter
    def minor(self, value) -> None:
        """
        Установка значения для «Минора» (смещение по отношению к последней актуальной «Полной версии»)

        :param value: Устанавливаемое значение «Минора»
        :return: Возвращаемое значение не определено
        """

        if pv_hlpr.minor_for_short_version_is_correct(value):
            self._minor = value
            self._notify_observer()
        else:
            raise ValueError(pv_errs.PVS_MINOR_VALUE_ERROR)

    @property
    def patch(self) -> int:
        """
        Значение для «Патча» (смещение по отношению к последней актуальной «Полной версии»)

        :return: Текущее значение «Патча»
        """

        return self._patch

    @patch.setter
    def patch(self, value) -> None:
        """
        Установка значения для «Патча» (смещение по отношению к последней актуальной «Полной версии»)

        :param value: Устанавливаемое значение «Патча»
        :return: Возвращаемое значение не определено
        """

        if pv_hlpr.patch_for_short_version_is_correct(value):
            self._patch = value
            self._notify_observer()
        else:
            raise ValueError(pv_errs.PVS_PATCH_VALUE_ERROR)

    @property
    def observer(self) -> pvo.PVObserver:
        """
        Свойство, соответствующее текущему «Наблюдателю»

        :return: Возвращает текущего «Наблюдателя»
        """

        return self._observer

    @observer.setter
    def observer(self, value: pvo.PVObserver) -> None:
        """
        Свойство, позволяющее установить «Наблюдателя»

        :param value: Устанавливаемый «Наблюдатель» (будет немедленно после установки оповещен об изменениях)
        :return: Возвращаемое значение не определено
        """

        if isinstance(value, pvo.PVObserver):
            self._observer = value
            self._notify_observer()
        else:
            raise ValueError(pv_errs.NOT_AN_OBSERVER)
