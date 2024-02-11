""" Константы, содержащие сообщения об ошибках """

PV_MINOR_VALUE_ERROR = ('An attempt to set an incorrect value for the minor version number '
                        '(must be in [1..15])')
""" Сообщение об ошибке при попытке установить некорректную минорную версию протокола """

PV_PATCH_VALUE_ERROR = ('An attempt to set an incorrect value for the patch version number '
                        '(must be in [0..15])')
""" Сообщение об ошибке при попытке установить некорректную версию патча протокола """

BITS_NOT_BYTE = 'The resulting value goes beyond the byte'
""" Сообщение об ошибке при попытке получить битовое представление длинной в байт для значения, превышающего байт """
