from src.frontier import chronos
from src.frontier import jsonifier
from src.frontier import sysutils
from src.ground import cnst


# region Константы
INIT_HEIGHT: int = -1
""" Значение высоты, используемое при инициализации блока (означает, что блок не полностью инициализирован) """

INIT_NONCE: int = -1
""" Значение nonce, используемое при инициализации блока (означает, что блок не полностью инициализирован) """

INIT_PREV_HASH: str = ''
""" Значение хэша предыдущего блока, используемое при инициализации блока (означает, что блок не полностью 
инициализирован) """

HGH_REPR_LENGTH: int = 10
""" Длина строкового представления текущей высоты (заполняется ведущими пробелами) """
# endregion


class BlockHeader:
    """ Заголовок блока (служебная информация, включая высоту блока и текущий момент времени в UTC). Любой заголовок
    кроме генезис-блока содержит также хэш предыдущего блока, благодаря чему выстраивается криптографически защищенная
    устойчивая цепочка """

    def __init__(self, genesis: bool = False) -> None:
        """ Инициализация частичная (установка начальных значений) """
        self._version: str = cnst.CURRENT_PROTOCOL_VERSION
        self._height: int = cnst.GENESIS_HEIGHT if genesis else INIT_HEIGHT
        self._prev_hash: str = cnst.ZERO_HASH if genesis else INIT_PREV_HASH
        self._merkel_root: str = cnst.ZERO_HASH  # todo Это — заглушка
        self._moment = chronos.this_moment()
        self._moment_str: str = chronos.moment_to_str(self._moment)
        self._difficulty: int = cnst.DEFAULT_DIFFICULTY
        self._nonce: int = INIT_NONCE
        self._genesis: bool = genesis

    def __repr__(self):
        """ Репрезентация (человеко-понятное описание объекта) """
        ver = f'protocol ver.: {self._version}'
        hgh_repr = '🚫' if self._height == INIT_HEIGHT else str(self._height).zfill(HGH_REPR_LENGTH)
        hgh = f'height: {hgh_repr}'
        pr_h_repr = '🚫' if self._prev_hash == INIT_PREV_HASH else self._prev_hash
        pr_h = f'previous block hash: {pr_h_repr}'
        dfn = 'genesis' if self._genesis else 'regular'
        stts = 'partially initialized' if not self.fully_initialized() else 'fully initialized'
        descr = (f'The header of a {dfn} block (instance '
                 f'of {__class__.__name__})\ncreated at {self._moment_str} and {stts}')
        mr = f'merkel root: {self._merkel_root}'
        nnc_repr = '🚫' if self._nonce == INIT_NONCE else str(self._nonce)
        nnc = f'nonce: {nnc_repr}'
        sze = f'size in bytes: {self.dict_size_in_bytes_str()}'
        nom = f'number of members in dict: {self.number_of_members_str()}'
        dfft = f'difficulty: {str(self._difficulty)}'
        result = (f'{descr}:\n ▪️ {ver};\n ▪️ {hgh};\n ▪️ {pr_h};\n ▪️ {mr};\n ▪️ {nnc};\n ▪️ {dfft};'
                  f'\n ▪️ {sze};\n ▪️ {nom}.\n')
        if not self.fully_initialized():
            result += f'⚠️ Please do not forget to fully initialize the object before using it!'
        return result

    def fully_initialized(self) -> bool:
        """ Признак того, чтоб объект полностью инициализирован """
        result = ((not self._height == INIT_HEIGHT) and
                  (not self._prev_hash == INIT_PREV_HASH) and
                  (not self._nonce == INIT_NONCE))
        return result

    def as_dict(self) -> dict:
        """ Преобразование внутренних данных в словарь """
        result = {
            'version': self.version,
            'height': self.height_str,
            'prev_hash': self.prev_hash,
            'merkle_root': self.merkle_root,
            'moment': self.moment_str,
            'difficulty': self.difficulty_str,
            'nonce': self.nonce_str,
            'genesis': self.genesis_str
        }
        return result

    def as_json(self) -> str:
        """ Преобразование внутренних данных в JSON-строку """
        return jsonifier.dict_to_json_str(self.as_dict())

    def as_bytes(self):
        return self.as_json().encode()

    def size_in_bytes(self):
        return len(self.as_bytes())

    def dict_size_in_bytes(self) -> int:
        """ Размер внутренних данных (в виде словаря) в байтах """
        return sysutils.dict_size_in_bytes(self.as_dict())

    def dict_size_in_bytes_str(self) -> str:
        """ Строковое представление размера внутренних данных (в виде словаря) в байтах """
        return str(self.dict_size_in_bytes())

    def number_of_members(self) -> int:
        """ Количество элементов в словаре """
        return len(self.as_dict())

    def number_of_members_str(self) -> str:
        """ Строковое представление количества элементов в словаре """
        return str(self.number_of_members())

    @property
    def version(self) -> str:
        """ Текущая версия протокола """
        return self._version

    @property
    def height(self) -> int:
        """ Текущая высота """
        return self._height

    @property
    def height_str(self) -> str:
        """ Строковое представление текущей высоты """
        return str(self._height)

    @height.setter
    def height(self, value: int) -> None:
        """ Установка высоты """
        if isinstance(value, int) and value > 0:
            self._height = value

    @property
    def prev_hash(self) -> str:
        """ Хэш предыдущего блока """
        return self._prev_hash

    @prev_hash.setter
    def prev_hash(self, value: str) -> None:
        """ Установка хэша предыдущего блока """
        if isinstance(value, str) and True:
            # todo возможно, есть смысл как-то проверять полученный хэш
            self._prev_hash = value

    @property
    def merkle_root(self) -> str:
        """ Корень дерева Меркла (дерева хэшей транзакций)  """
        return self._merkel_root

    @merkle_root.setter
    def merkle_root(self, value: str) -> None:
        """ Установка корня дерева Меркла (дерева хэшей транзакций) """
        if isinstance(value, str) and True:
            # todo возможно, есть смысл как-то проверять полученный рут
            self._merkel_root = value

    @property
    def moment(self):
        """ Дата/время """
        return self._moment

    # по идее, сеттер для moment не нужен (блок помечается соответствующей временной меткой во время создания

    @property
    def moment_str(self):
        """ Текстовое представление даты/времени """
        return self._moment_str

    @property
    def difficulty(self) -> int:
        """ Текущая сложность (майнинга) """
        return self._difficulty

    @property
    def difficulty_str(self) -> str:
        """ Текстовое представление текущей сложности (майнинга) """
        return str(self._difficulty)

    @difficulty.setter
    def difficulty(self, value: int) -> None:
        """ Установка сложности (майнинга) """
        if isinstance(value, int) and value >= cnst.MINIMAL_DIFFICULTY:
            self._difficulty = value

    @property
    def nonce(self) -> int:
        """ ... """
        # todo Дать внятный комментарий (после того, как станет понятно, что именно здесь подразумевается под nonce)
        return self._nonce

    @property
    def nonce_str(self) -> str:
        """ Текстовое представление ... """
        # todo Дать внятный комментарий (после того, как станет понятно, что именно здесь подразумевается под nonce)
        return str(self._nonce)

    @nonce.setter
    def nonce(self, value: int) -> None:
        """ Установка значения для """
        # todo Дать внятный комментарий (после того, как станет понятно, что именно здесь подразумевается под nonce)
        if isinstance(value, int) and value >= 0:
            self._nonce = value

    @property
    def genesis(self) -> bool:
        """ Признак того, является ли данный блок генезис-блоком """
        return self._genesis

    @property
    def genesis_str(self) -> str:
        """ Текстовое представление признака того, что данный блок является генезис-блоком """
        return str(self._genesis)

    # По идее, сеттер для genesis не нужен (и даже невозможен)


bh = BlockHeader(True)
print(bh)

