PVS_ONLY_ONE_BYTE_EXPECTED = 'Incorrect length of bytearray (only 1 byte expected)'
""" Сообщение об ошибке входного значения "краткую версию" через массив байтов (требуется 1 байт) """

PVS_MAJOR_VALUE_ERROR = ('Incorrect "Major" value for the short version of the protocol '
                         '(a value between 0 and 3 is expected)')
""" Сообщение об ошибке входного значения при попытке установить «Мажор» для краткой версии протокола """

PVS_MINOR_VALUE_ERROR = ('Incorrect "Minor" value for the short version of the protocol '
                         '(a value between 0 and 7 is expected)')
""" Сообщение об ошибке входного значения при попытке установить «Минор» для краткой версии протокола """

PVS_PATCH_VALUE_ERROR = ('Incorrect "Patch" value for the short version of the protocol '
                         '(a value between 0 and 7 is expected)')
""" Сообщение об ошибке входного значения при попытке установить «Патч» для краткой версии протокола """

NOT_AN_OBSERVER = 'The resulting object is not an inheritor of the class PVObserver'
""" Сообщение об ошибке при попытке установить в качестве «Наблюдателя» экземпляр какого-то другого класса """
