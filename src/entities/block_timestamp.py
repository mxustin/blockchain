""" Временная метка блока. Спецификация: https://clck.ru/38trLa """

from multipledispatch import dispatch
from datetime import datetime, timezone
from pytz import timezone as tz

from src.ground import cnst


class LargeHeaderTimestamp:

    @dispatch()
    def __init__(self) -> None:
        """ Инициализация «по умолчанию» без параметров (берется текущее время в UTC) """
        self._datetime: datetime = datetime.now(timezone.utc)
        self._beginning: datetime = datetime.strptime(cnst.DATETIME_BEGINNING, cnst.DATETIME_FORMAT)

    def __repr__(self) -> str:
        """ Репрезентация (человеко-читаемое, наглядное представление объекта, который должен рассматриваться как
        количество секунд, прошедших с 01.01.2024 00:00:00.0 UTC+0) """
        # region Готовим «элементы»
        descr = f'The Large Header Timestamp (instance of {__class__.__name__}) is {self.as_str()}'
        mtz = tz(cnst.MOSCOW_TIMEZONE)
        mdt = f'Moscow date/time: {self._datetime.astimezone(mtz)}'
        # endregion
        # region «Собираем» представление
        result = (f'{descr}:'
                  f'\n ▪️ {mdt}.')
        # endregion
        return result

    def as_str(self) -> str:
        return datetime.strftime(self._datetime, cnst.DATETIME_FORMAT)


dt = LargeHeaderTimestamp()
print(dt)

