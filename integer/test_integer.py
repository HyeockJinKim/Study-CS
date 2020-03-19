from integer.integer import Integer, Bit


def test_integer_init1():
    integer = Integer(3)
    assert str(integer) == '3'


def test_integer_init2():
    integer = Integer(-1)
    assert str(integer) == '-1'


def test_integer_plus1():
    integer1 = Integer(3)
    integer2 = Integer(5)
    assert integer1 + integer2 == Integer(8)


def test_integer_plus2():
    integer1 = Integer(-5)
    integer2 = Integer(-10)
    assert integer1 + integer2 == Integer(-15)


def test_integer_plus3():
    integer1 = Integer(5)
    integer2 = Integer(-10)
    assert integer1 + integer2 == Integer(-5)


def test_integer_plus4():
    integer1 = Integer(25)
    integer2 = Integer(-10)
    assert integer1 + integer2 == Integer(15)


def test_integer_complement1():
    integer = Integer(-3)
    bit_list = [Bit(True) for i in range(Integer.field_len)]
    bit_list[-2] = Bit(False)

    for i, bit in enumerate(bit_list):
        assert integer.complement().bits[i] == bit


def test_integer_complement2():
    integer = Integer(-3)
    assert integer.complement().decomplement() == integer


def test_integer_multiplication1():
    integer1 = Integer(107)
    integer2 = Integer(97)
    assert integer1 * integer2 == Integer(10379)


def test_integer_multiplication2():
    integer1 = Integer(-107)
    integer2 = Integer(97)
    assert integer1 * integer2 == Integer(-10379)


def test_integer_multiplication3():
    integer1 = Integer(107)
    integer2 = Integer(-97)
    assert integer1 * integer2 == Integer(-10379)


def test_integer_multiplication4():
    integer1 = Integer(-107)
    integer2 = Integer(-97)
    assert integer1 * integer2 == Integer(10379)


def test_integer_division1():
    integer1 = Integer(20)
    integer2 = Integer(4)
    assert integer1 / integer2 == Integer(5)


def test_integer_division2():
    integer1 = Integer(20)
    integer2 = Integer(-4)
    assert integer1 / integer2 == Integer(-5)


def test_integer_division3():
    integer1 = Integer(-20)
    integer2 = Integer(4)
    assert integer1 / integer2 == Integer(-5)


def test_integer_division4():
    integer1 = Integer(-20)
    integer2 = Integer(-4)
    assert integer1 / integer2 == Integer(5)


def test_integer_max_value1():
    assert Integer.max_value() == Integer(2**Integer.bit_len-1)


def test_integer_max_value2():
    bits = Integer.max_value().bits
    assert Integer.max_value().sign == Bit(False)
    for bit in bits:
        assert bit == Bit(True)


def test_integer_min_value1():
    assert Integer.min_value() == Integer(-(2**Integer.bit_len-1))


def test_integer_min_value2():
    bits = Integer.min_value().bits
    assert Integer.min_value().sign == Bit(True)
    for bit in bits:
        assert bit == Bit(True)
