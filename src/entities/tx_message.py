from src.frontier import chronos
from src.frontier import jsonifier
from src.frontier import sysutils

# region Константы
SENDER_UNDEFINED: str = 'undefined'

ACCEPTOR_UNDEFINED: str = 'undefined'

EMPTY_STR: str = ''

EMPTY_MESSAGE: str = EMPTY_STR

NO_SIGNATURE: str = EMPTY_STR
# endregion


class TxMessage:
    """ Отдельная транзакция: сообщение """

    def __init__(self):
        self._moment = chronos.this_moment()
        self._moment_str: str = chronos.moment_to_str(self._moment)
        self._sender: str = SENDER_UNDEFINED
        self._acceptor: str = ACCEPTOR_UNDEFINED
        self._content: str = EMPTY_MESSAGE
        self._signature: str = NO_SIGNATURE
        # todo Может потребоваться еще хэш транзакции

    def __repr__(self):
        # todo Если появится хэш транзакции, то здесь его тоже надо будет отразить
        descr = (f'The "Message" type transaction (instance '
                 f'of {__class__.__name__})\ncreated at {self._moment_str}')
        cnt = f'content: {self._content}' if self._content else f'the content is not presented (empty)'
        result = (f'{descr}:'
                  f'\n ▪️ {cnt}.\n')
        return result

    def fully_initialized(self) -> bool:                                                                                # noqa
        """ Признак того, чтоб объект полностью инициализирован """
        # todo Возможно, в будущем появится необходимость каким-либо образом дифференцировать
        return True

    def as_dict(self) -> dict:
        """ Преобразование внутренних данных в словарь """
        result = {
            'moment': self.moment_str,
            'sender': self.sender,
            'acceptor': self.acceptor,
            'content': self.content,
            'signature': self.signature
            # todo Если потребуется хэш транзакции, сюда его тоже надо будет добавить
        }
        return result

    def as_json(self) -> str:
        """ Преобразование внутренних данных в JSON-строку """
        return jsonifier.dict_to_json_str(self.as_dict())

    def size_in_bytes(self) -> int:
        """ Размер внутренних данных (в виде словаря) в байтах """
        return sysutils.dict_size_in_bytes(self.as_dict())

    def size_in_bytes_str(self) -> str:
        """ Строковое представление размера внутренних данных (в виде словаря) в байтах """
        return str(self.size_in_bytes())

    def number_of_members(self) -> int:
        """ Количество элементов в словаре """
        return len(self.as_dict())

    def number_of_members_str(self) -> str:
        """ Строковое представление количества элементов в словаре """
        return str(self.number_of_members())

    @property
    def moment(self):
        """ Дата/время """
        return self._moment

    # по идее, сеттер для moment не нужен (блок помечается соответствующей временной меткой во время создания

    @property
    def moment_str(self) -> str:
        """ Текстовое представление даты/времени """
        return self._moment_str

    @property
    def sender(self) -> str:
        return self._sender

    @sender.setter
    def sender(self, value: str) -> None:
        # todo Если появится хэш транзакции, то установка этого поля должна менять хэш
        if isinstance(value, str) and value:
            self._sender = value

    @property
    def acceptor(self) -> str:
        return self._acceptor

    @acceptor.setter
    def acceptor(self, value: str) -> None:
        # todo Если появится хэш транзакции, то установка этого поля должна менять хэш
        if isinstance(value, str) and value:
            self._acceptor = value

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str):
        # todo Если появится хэш транзакции, то установка этого поля должна менять хэш
        if isinstance(value, str) and value:
            self._content = value

    @property
    def signature(self) -> str:
        return self._signature

    # По идее установить "произвольную" сигнатуру должно быть нельзя: нужно определить метод "подписания" транзакции
    # todo Если появится хэш транзакции, то подписание должно использовать хэш
    # todo Определить метод подписания транзакции


msg = TxMessage()
print(msg)
