from functools import reduce

from bit.bit import Bit
from nums.arithmetic import Arithmetic
from nums.bit_operation import BitOperation
from unsigned_integer.unsigned_integer import UnsignedInteger


class Float:
    """
    Float의 메모리 구조
    +--------------+--------------------------+-------------------------------------------+
    | sign (1 bit) |     exponent (8 bit)     |             fraction (23 bit)             |
    +--------------+--------------------------+-------------------------------------------+

    32 bit로 이루어진 float 값

    양수 음수를 Sign bit를 통해 구분
    exponent 를 통해 소수점의 위치를 이동 (지수)
    fraction 을 통해 유효숫자를 표현 (가수)
    """
    bit_len = 32
    exponent_len = 8
    fraction_len = 23
    default_exponent_field = [Bit() for _ in range(exponent_len)]
    default_fraction_field = [Bit() for _ in range(fraction_len)]

    def __init__(self, exponents: list or float or int or str = None, fractions: list = None, sign: Bit = Bit()):
        if type(exponents) == str:
            res = self.str_to_float(exponents)
            self.sign = res.sign
            self.exponents = res.exponents
            self.fractions = res.fractions
        elif type(exponents) == float or type(exponents) == int:
            self.sign = sign
            self.exponents = self.default_exponent_field[::]
            self.fractions = self.default_fraction_field[::]
            self.set(exponents)
        elif type(exponents) == list:
            self.sign = sign
            self.exponents = exponents
            self.fractions = fractions
        else:
            self.sign = sign
            self.exponents = self.default_exponent_field[::]
            self.fractions = self.default_fraction_field[::]

    def is_zero(self) -> bool:
        """
        모든 비트가 0인지 확인하는 함수
        :return: 모든 비트가 0인지 여부
        """

        return not self.sign and BitOperation.is_empty(self.exponents) and BitOperation.is_empty(self.fractions)

    @classmethod
    def max_value(cls) -> "Float":
        """
        Float 의 최대값

        2 ** ((1.fraction)(유효숫자 수)) ** (2 ** (exponent 절반))
        :return: Float 의 최대값 3.40282346639e+38
        """

        sign = Bit()
        exponent = [Bit(True) for _ in range(cls.exponent_len-1)]
        exponent.append(Bit())
        fraction = [Bit(True) for _ in range(cls.fraction_len)]
        return Float(exponent, fraction, sign)

    @classmethod
    def min_value(cls) -> "Float":
        """
        Float 의 최소값

        - 2 ** ((1.fraction)(유효숫자 수)) ** (2 ** (exponent 절반))
        :return: Float 의 최소값 (-(2**(23+1))**(2**7-1))
        """

        sign = Bit(True)
        exponent = [Bit() for _ in range(cls.exponent_len-1)]
        exponent.append(Bit(True))
        fraction = [Bit() for _ in range(cls.fraction_len-1)]
        fraction.append(Bit(True))
        return Float(exponent, fraction, sign)

    def set(self, _float: float):
        """
        float 값을 통해 float 를 받기 위한 함수

        float 값을 Bit를 통해 float로 어떻게 표현하는 지 로직 확인을 위한 함수
        deprecated
        """

        if _float < 0:
            self.sign = Bit(True)
            _float = -_float
        else:
            self.sign = Bit()

        bits = []
        int_val = int(_float)
        _float -= int_val
        while int_val > 0:
            bits.insert(0, Bit(bool(int_val % 2)))
            int_val //= 2

        del bits[0]
        exp = len(bits)
        exp = UnsignedInteger('127') + UnsignedInteger(str(exp))
        while _float > 0 and len(bits) < self.fraction_len:
            _float *= 2
            bits.append(Bit(int(_float) == 1))
            _float -= int(_float)

        for _ in range(self.fraction_len-len(bits)):
            bits.append(Bit())

        bits[-1] = Bit(bool(_float))
        self.exponents = exp.bits[-self.exponent_len:]
        self.fractions = bits[:self.fraction_len]

    @classmethod
    def str_to_float(cls, val: str) -> "Float":
        """
        String 값을 통해 float 값 read
        :param val: String 으로 표현된 정수 값 (공백이 없다는 가정)
        :return: Float 의 값
        """

        if val[0] == '-':
            sign = Bit(True)
            val = val[1:]
        else:
            sign = Bit()
        dec, minor = cls.split_point(val)
        fraction, digit = Arithmetic.str_to_integer_until_overflow(dec, cls.fraction_len+1)
        frac, digit = Arithmetic.str_to_minor(fraction, minor, digit, cls.fraction_len+1)
        fraction = frac[:-1]
        if frac[-1]:
            fraction, overflow = Arithmetic.add_bits(fraction, BitOperation.num_map['1'], cls.fraction_len)
            if overflow:
                digit += 1
        if str(digit)[0] == '-':
            exponent, _ = Arithmetic.sub_bits(
                Arithmetic.str_to_integer('127', cls.exponent_len),
                Arithmetic.str_to_integer(str(digit)[1:], cls.exponent_len),
                cls.exponent_len
            )
        else:
            exponent, _ = Arithmetic.add_bits(
                Arithmetic.str_to_integer('127', cls.exponent_len),
                Arithmetic.str_to_integer(str(digit), cls.exponent_len),
                cls.exponent_len
            )
        return Float(exponent, fraction, sign)

    @classmethod
    def split_point(cls, val: str) -> (str, str):
        val = val.split('.')
        if len(val) < 2:
            return val[0], '0'
        return val[0], val[1]

    def val(self) -> int:
        """
        bit 들로 이루어진 값을 int 값으로 읽을 수 있도록 만드는 함수
        음수 확인은 signed bit를 통해 확인

        테스트 및 출력을 위해 사용하는 함수
        :return: int 값으로 리턴
        """

        if self.is_zero():
            return 0

        res = BitOperation.binary_to_float(self.exponents, self.fractions)
        if self.sign:
            return -res
        return res

    def __str__(self) -> str:
        return str(self.val())

    def is_negative(self) -> Bit:
        """
        Sign 비트를 통해 음수 확인
        :return: 음수인지 여부
        """
        return self.sign

    def __neg__(self) -> "Float":
        """
        sign minus 연산( - )을 위한 operator overloading
        :return: 새로운 Float 객체로 return
        """
        return Float(self.exponents[::], self.fractions[::], ~self.sign)

    def __add__(self, other: "Float") -> "Float":
        """
        Binary Add 연산 ( + )을 위한 operator overloading
        exponent를 같은 값으로 만든 후 fraction 덧셈 연산
        :param other: Float 타입 가정
        :return: 새로운 Float 객체로 return
        """
        exp, a_frac, b_frac = Arithmetic.equalize_exponent(self.exponents, self.fractions, other.exponents, other.fractions)
        if BitOperation.raw_ge_bits(a_frac, b_frac):
            sign = self.sign
        else:
            sign = other.sign

        if self.sign ^ other.sign:
            res, overflow = Arithmetic.sub_bits(a_frac, b_frac, self.fraction_len+1)
            if sign:
                res = Arithmetic.decomplement_bits(res, self.fraction_len+1)
        else:
            res, overflow = Arithmetic.add_bits(a_frac, b_frac, self.fraction_len+1)
            if overflow:
                res.insert(0, overflow)
                res = res[:-1]
                exp, _ = Arithmetic.add_bits(exp, BitOperation.num_map['1'], self.exponent_len)

        first = BitOperation.first_bit_index(res)
        exp, _ = Arithmetic.raw_sub_bits(exp, Arithmetic.str_to_integer(str(first), self.exponent_len))
        frac = BitOperation.raw_lshift_bits(res, first)[1:]
        if not self.sign ^ other.sign and not BitOperation.is_empty(res[-first+1:]):
            frac, _ = Arithmetic.add_bits(frac, BitOperation.num_map['1'], self.fraction_len)
        return Float(exp, frac, sign)

    def __sub__(self, other: "Float") -> "Float":
        """
        Binary Sub 연산 ( - )을 위한 operator overloading
        음수로 변경한 후 add 연산
        :param other: Float 타입 가정
        :return: 새로운 Float 객체로 return
        """
        return self + (-other)

    def __mul__(self, other: "Float") -> "Float":
        """
        Binary Mul 연산 ( * )을 위한 operator overloading
        :param other: Float 타입 가정
        :return: 새로운 Float 객체로 return
        """
        pass

    def __truediv__(self, other: "Float") -> "Float":
        """
        Binary Div 연산 ( / )을 위한 operator overloading
        :param other: Float 타입 가정
        :return: 새로운 Float 객체로 return
        """
        pass

    def __le__(self, other: "Float") -> bool:
        """
        Low Equal 연산 ( <= )을 위한 operator overloading
        :param other: Float 타입 가정
        :return: 새로운 Float 객체로 return
        """
        pass

    def __eq__(self, other: "Float") -> bool:
        return self.sign == other.sign and BitOperation.eq_bits(self.exponents, other.exponents, self.exponent_len) and\
               BitOperation.eq_bits(self.fractions, other.fractions, self.fraction_len)
