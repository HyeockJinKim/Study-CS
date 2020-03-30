from bit.bit import Bit
from float.float import Float


def test_float_init1():
    float_val = Float('3')
    assert str(float_val) == '3.0'


def test_float_init2():
    float_val = Float('-1')
    assert str(float_val) == '-1.0'


def test_float_init3():
    float_val = Float('0')
    assert str(float_val) == '0'


def test_float_init4():
    float_val = Float('0.0')
    assert str(float_val) == '0'


def test_float_init5():
    float_val = Float('3.14')
    assert str(float_val) == '3.140000104904175'


def test_float_init6():
    float_val = Float('0.0001')
    assert str(float_val) == '9.999999747378752e-05'


def test_float_plus1():
    float1 = Float('3.14')
    float2 = Float('2.5')
    assert float1 + float2 == Float('5.640000343322754')


def test_float_plus2():
    float1 = Float('-3.14')
    float2 = Float('-2.5')
    assert float1 + float2 == Float('-5.640000343322754')


def test_float_plus3():
    float1 = Float('5')
    float2 = Float('-10')
    assert float1 + float2 == Float('-5.0')


def test_float_plus4():
    float1 = Float('25')
    float2 = Float('-10')
    assert float1 + float2 == Float('15.0')


def test_float_multiplication1():
    float1 = Float('107')
    float2 = Float('97')
    assert float1 * float2 == Float('10379.0')


def test_float_multiplication2():
    float1 = Float('107')
    float2 = Float('-97')
    assert float1 * float2 == Float('-10379.0')


def test_float_multiplication3():
    float1 = Float('-107')
    float2 = Float('-97')
    assert float1 * float2 == Float('10379.0')


def test_float_multiplication4():
    float1 = Float('3.14')
    float2 = Float('2.0001')
    assert str(float1 * float2) == '6.280313491821289'


def test_float_multiplication5():
    float1 = Float('0.14')
    float2 = Float('0.0001')
    res = float1 * float2

    assert res.sign == Bit()
    exponents = map(lambda x: Bit(bool(x)), [0, 1, 1, 0, 1, 1, 1, 0])
    for i, exp in enumerate(exponents):
        assert res.exponents[i] == exp

    fractions = map(lambda x: Bit(bool(x)), [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0])
    for i, exp in enumerate(fractions):
        assert res.fractions[i] == exp


def test_float_division1():
    float1 = Float('20')
    float2 = Float('4')
    assert float1 / float2 == Float('5.0')


def test_float_division2():
    float1 = Float('3.14')
    float2 = Float('2.0001')
    assert str(float1 / float2) == '1.569921612739563'


def test_float_division3():
    float1 = Float('3.14')
    float2 = Float('0')
    assert str(float1 / float2) == 'inf'


def test_float_division4():
    float1 = Float('-3.14')
    float2 = Float('0')
    assert str(float1 / float2) == '-inf'


def test_float_division5():
    float1 = Float('0')
    float2 = Float('0')
    assert str(float1 / float2) == 'nan'


def test_float_max_value1():
    assert str(Float.max_value()) == '340282346638528859811704183484516925440'


def test_float_max_value2():
    assert Float.max_value().sign == Bit(False)
    for bit in Float.max_value().exponents[:-1]:
        assert bit == Bit(True)
    assert Float.max_value().exponents[-1] == Bit()
    for bit in Float.max_value().fractions:
        assert bit == Bit(True)


def test_float_min_value1():
    assert str(Float.min_value()) == '-1.175494490952134e-38'


def test_float_min_value2():
    assert Float.min_value().sign == Bit(True)
    for bit in Float.min_value().exponents[:-1]:
        assert bit == Bit()
    assert Float.min_value().exponents[-1] == Bit(True)
    for bit in Float.min_value().fractions[:-1]:
        assert bit == Bit()
    assert Float.min_value().fractions[-1] == Bit(True)
