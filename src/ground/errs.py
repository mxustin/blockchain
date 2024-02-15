""" Константы, содержащие сообщения об ошибках """

BITS_NOT_BYTE = 'The resulting value goes beyond the byte'
""" Сообщение об ошибке при попытке получить битовое представление длинной в байт для значения, превышающего байт """

PVF_MAJOR_VALUE_ERROR = ('Incorrect "major" value for the full version of the protocol '
                         '(a value between 0 and 255 is expected)')
""" Сообщение об ошибке входного значения при попытке установить «мажор» для полной версии протокола """

PVF_MINOR_VALUE_ERROR = ('Incorrect "minor" value for the full version of the protocol '
                         '(a value between 0 and 15 is expected if "major" > 0 else between 1 and 15)')
""" Сообщение об ошибке входного значения при попытке установить «минор» для полной версии протокола """

PVF_PATCH_VALUE_ERROR = ('Incorrect "patch" value for the full version of the protocol '
                         '(a value between 0 and 15 is expected)')
""" Сообщение об ошибке входного значения при попытке установить «патч» для полной версии протокола """

PVF_BYTE_ARRAY_HAS_INCORRECT_LENGTH = 'Incorrect length of bytearray (exactly 2 bytes expected)'
""" Сообщение об ошибке входного значения при попытке установить версию через массив байтов 
(требуется ровно 2 байта) """

PVS_ONLY_ONE_BYTE_EXPECTED = 'Incorrect length of bytearray (only 1 byte expected)'
""" Сообщение об ошибке входного значения "краткую версию" через массив байтов (требуется 1 байт) """

PVS_MAJOR_VALUE_ERROR = ('Incorrect "major" value for the short version of the protocol '
                         '(a value between 0 and 3 is expected)')
""" Сообщение об ошибке входного значения при попытке установить «мажор» для краткой версии протокола """

PVS_MINOR_VALUE_ERROR = ('Incorrect "minor" value for the short version of the protocol '
                         '(a value between 0 and 7 is expected)')
""" Сообщение об ошибке входного значения при попытке установить «минор» для краткой версии протокола """

PVS_PATCH_VALUE_ERROR = ('Incorrect "patch" value for the short version of the protocol '
                         '(a value between 0 and 7 is expected)')
""" Сообщение об ошибке входного значения при попытке установить «патч» для краткой версии протокола """

