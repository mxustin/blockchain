"""
Абстрактный класс «Наблюдатель» (применяется в «фактической» версии протокола для наблюдения за изменениями внутри
«полной» и «краткой» версий).

Спецификация: https://clck.ru/38uZ7g
"""

from abc import ABC, abstractmethod


class PVObserver(ABC):
    """
    Элемент паттерна «Наблюдатель» для реализации механизма изменений «фактической» версии протокола вслед за
    изменениями в «полной» и/или «краткой» версиях
    """

    @abstractmethod
    def process_changing(self) -> None:
        """
        Абстрактный метод, предназначенный для обработки изменений в «полной» и/или «краткой» версиях протокола. Должен
        быть реализован в потомках

        :return: Возвращаемые значения не определены
        """

        ...
