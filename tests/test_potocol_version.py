from pytest import raises
from src.entities import protocol_version as pver


# region «Краткая версия»

# region Позитивные тесты
def test_p_short_version_init_via_ints():
    # Определяем через int-ы
    sv = pver.ProtocolVersionShort(1, 2, 3)
    assert sv.minor == 2
    assert sv.as_str() == '+1.+2.+3'
    assert sv.as_binary_str() == '01010011'


def test_p_short_version_init_via_bytes():
    v = pver.ProtocolVersionShort(bytearray([0b01010011]))
    assert v.as_hex() == '53'
    assert v.major == 1


def test_p_short_version_repr():
    v = pver.ProtocolVersionShort(0, 0, 0)
    assert str(v) == '+0.+0.+0'
    assert repr(v)[:3] == 'The'  # Полное представление довольно длинное...


def test_p_short_version_changing_values():
    v = pver.ProtocolVersionShort(0, 0, 0)
    v << (1, 2, 3)
    assert v.as_str() == '+1.+2.+3'


def test_p_short_version_changing_all():
    v = pver.ProtocolVersionShort(0, 0, 0)
    v.major += 1
    v.minor += 2
    v.patch += 3
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 3


def test_p_short_version_getting_bytes():
    v = pver.ProtocolVersionShort(1, 2, 3)
    assert v._get_bytes() == 83  # 01010011
    assert v.as_bytes() == bytearray([83])

# endregion


# region Негативные тесты
def test_n_short_version_init_via_ints():
    # Определяем через int-ы
    with raises(ValueError):
        sv = pver.ProtocolVersionShort(5, 9, 12)


def test_n_short_version_init_via_bytes():
    arr = bytearray([1, 2, 3])
    with raises(ValueError):
        v = pver.ProtocolVersionShort(arr)


def test_n_short_version_changing_values():
    v = pver.ProtocolVersionShort(0, 0, 0)
    with raises(ValueError):
        v << (9, 9, 15)

# endregion

# endregion


# region «Полная версия»

# region Позитивные тесты
def test_p_full_version_init_via_ints():
    v = pver.ProtocolVersionFull(1, 2, 3)
    assert v.minor == 2
    assert str(v) == '1.2.3'
    assert v.as_binary_str() == '0000000100100011'


def test_p_full_version_repr():
    v = pver.ProtocolVersionFull(5, 8, 13)
    assert str(v) == '5.8.13'
    assert repr(v)[:3] == 'The'  # Полное представление довольно длинное...
    assert v.as_bytes() == b'\x05\x8d'


def test_p_full_version_init_via_bytes():
    v = pver.ProtocolVersionFull(1, 2, 3)
    v1 = pver.ProtocolVersionFull(v.as_bytes())
    assert v1.patch == 3
    assert str(v1) == '1.2.3'
    assert v1.as_binary_str() == '0000000100100011'


def test_p_full_version_value_changing():
    v = pver.ProtocolVersionFull(5, 8, 13)
    v.patch += 1
    assert v.patch == 14
    v << (7, 9, 14)
    assert v.major == 7

# endregion

# region Негативные тесты

# endregion

# endregion


# region Фактическая версия (полная + кратка)

# region Позитивные тесты
def test_p_ver_init():
    f_ver = pver.ProtocolVersionFull(0, 1, 0)
    s_ver = pver.ProtocolVersionShort(0, 0, 0)
    v = pver.ProtocolVersion(f_ver, s_ver)
    assert v.minor == 1
    v.full.patch += 1
    assert v.full.patch == 1



# endregion

# region Негативные тесты

# endregion

# endregion

# region Прочее
def test_undefined_version():
    assert pver._undefined_version() == (-1, -1, -1)


# endregion


