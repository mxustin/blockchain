from pytest import raises

from src.entities.protocol_version import pv_hlpr


def test_p_undefined_version():
    tst = pv_hlpr.undefined_version()
    assert tst == (-1, -1, -1)


def test_p_checking_byte_array_length_for_short_version():
    barr = bytearray([0b00000000])
    assert pv_hlpr.bytearray_length_for_short_version_is_correct(barr) is True


def test_n_checking_byte_array_length_for_short_version():
    barr = bytearray([0b00000000, 0b00000000])
    assert pv_hlpr.bytearray_length_for_short_version_is_correct(barr) is False


def test_p_getting_major_for_short_version_from_byte():
    b = 0b01000000
    assert pv_hlpr.major_for_short_version_from_byte(b) == 1


def test_p_getting_minor_for_short_version_from_byte():
    b = 0b00001000
    assert pv_hlpr.minor_for_short_version_from_byte(b) == 1


def test_p_getting_patch_for_short_version_from_byte():
    b = 0b00000001
    assert pv_hlpr.patch_for_short_version_from_byte(b) == 1


def test_p_parsing_short_version_from_byte():
    b = 0b01001001
    assert pv_hlpr.decode_short_version(b) == (1, 1, 1)


def test_p_encoding_major_for_short_version_to_byte():
    mj = 1
    assert pv_hlpr.major_for_short_version_to_byte(mj) == 0b01000000


def test_p_encoding_minor_for_short_version_to_byte():
    mn = 2
    assert pv_hlpr.minor_for_short_version_to_byte(mn) == 0b00010000


def test_p_encoding_patch_for_short_version_to_byte():
    ph = 3
    assert pv_hlpr.patch_for_short_version_to_byte(ph) == 0b00000011


def test_p_encoding_for_short_version():
    mj = 0
    mn = 1
    ph = 2
    assert pv_hlpr.encode_short_version(mj, mn, ph) == 0b00001010


def test_p_checking_major_for_short_version():
    mj = 1
    assert pv_hlpr.major_for_short_version_is_correct(mj) is True


def test_n_checking_major_for_short_version():
    mj = 4
    assert pv_hlpr.major_for_short_version_is_correct(mj) is False


def test_p_checking_minor_for_short_version():
    mn = 4
    assert pv_hlpr.minor_for_short_version_is_correct(mn) is True


def test_n_checking_minor_for_short_version():
    mn = 8
    assert pv_hlpr.minor_for_short_version_is_correct(mn) is False


def test_p_checking_patch_for_short_version():
    ph = 5
    assert pv_hlpr.patch_for_short_version_is_correct(ph) is True


def test_n_checking_patch_for_short_version():
    ph = 11
    assert pv_hlpr.patch_for_short_version_is_correct(ph) is False


