import pytest
from integer.integer import Integer, Bit


def test_integer_init1():
    integer = Integer('3')
    assert str(integer) == '3'


def test_integer_init2():
    integer = Integer('-1')
    assert str(integer) == '-1'


def test_integer_plus1():
    integer1 = Integer('3')
    integer2 = Integer('5')
    assert integer1 + integer2 == Integer('8')


def test_integer_plus2():
    integer1 = Integer('-5')
    integer2 = Integer('-10')
    assert integer1 + integer2 == Integer('-15')


def test_integer_plus3():
    integer1 = Integer('5')
    integer2 = Integer('-10')
    assert integer1 + integer2 == Integer('-5')


def test_integer_plus4():
    integer1 = Integer('25')
    integer2 = Integer('-10')
    assert integer1 + integer2 == Integer('15')


def test_integer_multiplication1():
    integer1 = Integer('107')
    integer2 = Integer('97')
    assert integer1 * integer2 == Integer('10379')


def test_integer_multiplication2():
    integer1 = Integer('-107')
    integer2 = Integer('97')
    assert integer1 * integer2 == Integer('-10379')


def test_integer_multiplication3():
    integer1 = Integer('107')
    integer2 = Integer('-97')
    assert integer1 * integer2 == Integer('-10379')


def test_integer_multiplication4():
    integer1 = Integer('-107')
    integer2 = Integer('-97')
    assert integer1 * integer2 == Integer('10379')


def test_integer_division1():
    integer1 = Integer('20')
    integer2 = Integer('4')
    assert integer1 / integer2 == Integer('5')


def test_integer_division2():
    integer1 = Integer('20')
    integer2 = Integer('-4')
    assert integer1 / integer2 == Integer('-5')


def test_integer_division3():
    integer1 = Integer('-20')
    integer2 = Integer('4')
    assert integer1 / integer2 == Integer('-5')


def test_integer_division4():
    integer1 = Integer('-20')
    integer2 = Integer('-4')
    assert integer1 / integer2 == Integer('5')


def test_integer_division5():
    integer1 = Integer.max_value()
    integer2 = Integer('5')
    assert integer1 / integer2 == Integer('429496729')


def test_integer_division6():
    integer1 = Integer.max_value()
    integer2 = Integer('5')
    assert integer2 / integer1 == Integer('0')


def test_integer_division7():
    integer1 = Integer('6')
    integer2 = Integer('0')
    with pytest.raises(ZeroDivisionError):
        integer1 / integer2


def test_integer_division8():
    integer1 = Integer('0')
    integer2 = Integer('0')
    with pytest.raises(ZeroDivisionError):
        integer1 / integer2


def test_integer_max_value1():
    assert Integer.max_value() == Integer(str(2**(Integer.bit_len-1) -1))


def test_integer_max_value2():
    bits = Integer.max_value().bits
    assert Integer.max_value().sign == Bit(False)
    for bit in bits:
        assert bit == Bit(True)


def test_integer_min_value1():
    assert Integer.min_value() == Integer(str(-(2**(Integer.bit_len-1)-1)))


def test_integer_min_value2():
    bits = Integer.min_value().bits
    assert Integer.min_value().sign == Bit(True)
    for bit in bits:
        assert bit == Bit(True)
