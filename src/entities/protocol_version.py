""" Версия протокола. Спецификация: https://clck.ru/38jK47 """

from src.ground import errs
from src.ground import bits


class ProtocolVersion:
    """ Версия протокола """

    def __init__(self, minor: int, patch: int):
        """ Инициализация """
        self._minor: int = -1  # Признак того, что значение не установлено
        self.minor = minor
        self._patch: int = -1  # Признак того, что значение не установлено
        self.patch = patch

    def __repr__(self):
        descr = f'The Version of protocol (instance of {__class__.__name__})'
        mv = f'minor: {self._minor}'
        pv = f'patch: {self._patch}'
        result = (f'{descr}:\n ▪️ {mv};\n ▪️ {pv}.'
                  f'\nAs binary string: {self.as_bin_str()}. '
                  f'As byte: {self.as_byte()}.')
        return result

    def as_byte(self) -> int:
        result = self._minor << 4
        result += self._patch
        return result

    def as_bin_str(self) -> str:
        return bits.byte_as_bits_str(self.as_byte())

    @property
    def minor(self) -> int:
        return self._minor

    @minor.setter
    def minor(self, value: int) -> None:
        if isinstance(value, int) and (1 <= value <= 15):
            self._minor: int = value
        else:
            raise ValueError(errs.PV_MINOR_VALUE_ERROR)

    @property
    def patch(self) -> int:
        return self._patch

    @patch.setter
    def patch(self, value: int) -> None:
        if isinstance(value, int) and (0 <= value <= 15):
            self._patch: int = value
        else:
            raise ValueError(errs.PV_MINOR_VALUE_ERROR)


ver = ProtocolVersion(4, 5)
print(ver)

