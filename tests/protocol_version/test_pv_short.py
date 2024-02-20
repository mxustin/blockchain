from pytest import raises

from src.entities.protocol_version import pv_short as pvs
from src.entities.protocol_version import pv_observer as pvo


def test_p_initialization_via_defaults():
    v = pvs.PVShort()
    assert v.as_str() == '+0.+0.+0'
    assert str(v) == '+0.+0.+0'


def test_p_initialization_via_ints():
    v = pvs.PVShort(1, 2, 3)
    assert v.as_str() == '+1.+2.+3'
    assert v.as_binary_str() == '01010011'


def test_n_initialization_via_ints():
    with raises(ValueError):
        v = pvs.PVShort(5, 2, 3)                                                                                        # noqa


def test_p_initialization_via_byte_arr():
    v = pvs.PVShort(bytearray([0]))
    assert v.as_str() == '+0.+0.+0'


def test_n_initialization_via_byte_arr():
    with raises(ValueError):
        v = pvs.PVShort(bytearray([0, 0, 0]))                                                                           # noqa


def test_p_repr():
    v = pvs.PVShort(1, 2, 3)
    assert repr(v)[:3] == 'The'  # Полное представление довольно длинное 😃


def test_p_as_str():
    v = pvs.PVShort(1, 3, 5)
    assert v.as_str() == '+1.+3.+5'


def test_p_lshift():
    v = pvs.PVShort(0, 0, 0)
    assert v.as_str() == '+0.+0.+0'
    v << (1, 2, 3)
    assert v.as_str() == '+1.+2.+3'


def test_n_lshift():
    v = pvs.PVShort(0, 0, 0)
    with raises(ValueError):
        v << (5, 10, 15)


def test_p_as_bytes():
    b = 1
    v = pvs.PVShort(bytearray([b]))
    assert v.as_bytes()[0] == b


def test_p_as_hex():
    v = pvs.PVShort(bytearray([255]))
    assert v.as_hex() == 'ff'


def test_p_as_binary_str():
    v = pvs.PVShort(3, 7, 7)
    assert v.as_binary_str() == '11111111'


def test_p_get_major():
    v = pvs.PVShort(2, 4, 6)
    assert v.major == 2


def test_p_set_major():
    v = pvs.PVShort(2, 4, 6)
    v.major = 1
    assert v.major == 1


def test_n_set_major():
    v = pvs.PVShort(2, 4, 6)
    with raises(ValueError):
        v.major = 4


def test_p_get_minor():
    v = pvs.PVShort(2, 4, 6)
    assert v.minor == 4


def test_p_set_minor():
    v = pvs.PVShort(2, 4, 6)
    v.minor = 1
    assert v.minor == 1


def test_n_set_minor():
    v = pvs.PVShort(2, 4, 6)
    with raises(ValueError):
        v.minor = 9


def test_p_get_patch():
    v = pvs.PVShort(2, 4, 6)
    assert v.patch == 6


def test_p_set_patch():
    v = pvs.PVShort(2, 4, 6)
    v.patch = 1
    assert v.patch == 1


def test_n_set_patch():
    v = pvs.PVShort(2, 4, 6)
    with raises(ValueError):
        v.patch = 42


def test_p_notification():

    b = 1

    class T(pvo.PVObserver):

        def process_changing(self) -> str:
            nonlocal b
            b = 2
            return 'Yes'

    t = T()
    v = pvs.PVShort(1, 2, 3)
    v.observer = t
    v << (0, 0, 0)
    assert b == 2


def test_p_set_observer():
    class T(pvo.PVObserver):

        def process_changing(self) -> str:
            return 'Yes'

    t = T()
    v = pvs.PVShort(1, 2, 3)
    v.observer = t


def test_n_set_observer():
    v = pvs.PVShort(1, 2, 3)
    with raises(ValueError):
        v.observer = 'Вася'


def test_p_get_observer():
    class T(pvo.PVObserver):

        def process_changing(self) -> str:
            return 'Yes'

    t = T()
    v = pvs.PVShort(1, 2, 3)
    v.observer = t
    g = v.observer
    assert g == t


def test_p_getting_raw_bytes():
    v = pvs.PVShort(3, 7, 7)
    assert v._get_bytes() == 255
