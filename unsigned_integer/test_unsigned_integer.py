from bit.bit import Bit
from unsigned_integer.unsigned_integer import UnsignedInteger


def test_unsigned_integer_init1():
    unsigned_integer = UnsignedInteger(3)
    assert str(unsigned_integer) == '3'


def test_unsigned_integer_init2():
    unsigned_integer = UnsignedInteger(-1)
    assert unsigned_integer.val() == 2**UnsignedInteger.bit_len-1


def test_unsigned_integer_plus1():
    unsigned_integer1 = UnsignedInteger(3)
    unsigned_integer2 = UnsignedInteger(5)
    assert unsigned_integer1 + unsigned_integer2 == UnsignedInteger(8)


def test_unsigned_integer_plus2():
    unsigned_integer1 = UnsignedInteger(-5)
    unsigned_integer2 = UnsignedInteger(-10)
    assert unsigned_integer1 + unsigned_integer2 == UnsignedInteger(-15)


def test_unsigned_integer_plus3():
    unsigned_integer1 = UnsignedInteger(5)
    unsigned_integer2 = UnsignedInteger(-10)
    assert unsigned_integer1 + unsigned_integer2 == UnsignedInteger(-5)


def test_unsigned_integer_plus4():
    unsigned_integer1 = UnsignedInteger(25)
    unsigned_integer2 = UnsignedInteger(-10)
    assert unsigned_integer1 + unsigned_integer2 == UnsignedInteger(15)


def test_unsigned_integer_complement1():
    unsigned_integer = UnsignedInteger(-3)
    bit_list = [Bit(True) for _ in range(UnsignedInteger.field_len)]
    bit_list[-2] = Bit(False)

    for i, bit in enumerate(bit_list):
        assert unsigned_integer.bits[i] == bit


def test_unsigned_integer_complement2():
    unsigned_integer = UnsignedInteger(3)
    assert unsigned_integer.complement() == UnsignedInteger(-3)


def test_unsigned_integer_multiplication():
    unsigned_integer1 = UnsignedInteger(107)
    unsigned_integer2 = UnsignedInteger(97)
    assert unsigned_integer1 * unsigned_integer2 == UnsignedInteger(10379)


def test_unsigned_integer_division():
    unsigned_integer1 = UnsignedInteger(20)
    unsigned_integer2 = UnsignedInteger(4)
    assert unsigned_integer1 / unsigned_integer2 == UnsignedInteger(5)


def test_unsigned_integer_max_value1():
    assert UnsignedInteger.max_value() == UnsignedInteger(2**(UnsignedInteger.bit_len+1)-1)


def test_unsigned_integer_max_value2():
    bits = UnsignedInteger.max_value().bits
    for bit in bits:
        assert bit == Bit(True)


def test_unsigned_integer_min_value1():
    assert UnsignedInteger.min_value() == UnsignedInteger(0)


def test_unsigned_integer_min_value2():
    bits = UnsignedInteger.min_value().bits
    for bit in bits:
        assert bit == Bit(False)
