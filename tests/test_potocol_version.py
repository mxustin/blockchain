from src.entities.protocol_version import ProtocolVersionFull


def test_positive_creation_as_integers():
    v = ProtocolVersionFull(1, 2, 3)
    assert v.minor == 2
    assert str(v) == '1.2.3'
    assert v.as_binary_str() == '0000000100100011'


def test_positive_creation_as_bytearray():
    v = ProtocolVersionFull(1, 2, 3)
    v1 = ProtocolVersionFull(v.as_bytes())
    assert v1.patch == 3
    assert str(v1) == '1.2.3'
    assert v1.as_binary_str() == '0000000100100011'


def test_positive_representation():
    v = ProtocolVersionFull(5, 8, 13)
    assert str(v) == '5.8.13'
    assert repr(v)[:3] == 'The'  # Полное представление довольно длинное...
    assert v.as_bytes() == b'\x05\x8d'


def test_value_changing():
    v = ProtocolVersionFull(5, 8, 13)
    v.patch += 1
    assert v.patch == 14

