import datetime
from datetime import datetime as dt
from src.ground import cnst


def this_moment():
    """ Возвращает текущее время (используется всегда только время в часовом поясе UTC): в виде объекта datetime """
    return dt.now(datetime.UTC)


def moment_to_str(moment):
    """ Возвращает дату/время в виде строки в формате, определяемом в константе DATETIME_FORMAT """
    return moment.strftime(cnst.DATETIME_FORMAT)
