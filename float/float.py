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

    def is_nan(self) -> bool:
        """
        값이 nan 인지 확인하는 함수
        :return: exponent가 모두 1이고 fraction은 모두 0이 아닌지 여부
        """
        return BitOperation.is_empty(BitOperation.neg_bits(self.exponents)) and not BitOperation.is_empty(self.fractions)

    def is_inf(self) -> bool:
        """
        값이 inf 인지 확인하는 함수
        :return: exponent가 모두 1이고 fraction은 모두 0인지 여부
        """
        return BitOperation.is_empty(BitOperation.neg_bits(self.exponents)) and BitOperation.is_empty(self.fractions)

    @classmethod
    def max_value(cls) -> "Float":
        """
        Float 의 최대값

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

        :return: Float 의 최소값 -1.175494490952134e-38
        """

        sign = Bit(True)
        exponent = [Bit() for _ in range(cls.exponent_len-1)]
        exponent.append(Bit(True))
        fraction = [Bit() for _ in range(cls.fraction_len-1)]
        fraction.append(Bit(True))
        return Float(exponent, fraction, sign)

    @classmethod
    def inf(cls) -> "Float":
        """
        무한대 값

        :return: Infinite 값
        """

        sign = Bit()
        exponent = [Bit(True) for _ in range(cls.exponent_len)]
        fraction = [Bit() for _ in range(cls.fraction_len)]
        return Float(exponent, fraction, sign)

    @classmethod
    def nan(cls) -> "Float":
        """
        알 수 없는 값

        Exponent 값은 모두 1 이고 fraction이 모두 0이 아닌 값 (하나라도 1이 있음)
        :return: nan 값
        """

        sign = Bit()
        exponent = [Bit(True) for _ in range(cls.exponent_len)]
        fraction = [Bit(True) for _ in range(cls.fraction_len)]
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

        fraction = frac[1:]
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
        """
        문자열을 . 을 기준으로 정수값과 소수값을 나눔
        :param val: 실수값 문자열
        :return: 정수값, 소수값
        """
        val = val.split('.')
        if len(val) < 2:
            return val[0], '0'
        return val[0], val[1]

    def val(self) -> float:
        """
        bit 들로 이루어진 값을 float 값으로 읽을 수 있도록 만드는 함수
        음수 확인은 signed bit를 통해 확인

        테스트 및 출력을 위해 사용하는 함수
        :return: float 값으로 리턴
        """

        if self.is_zero():
            return 0

        if self.is_nan():
            return float('nan')

        if self.is_inf():
            if self.sign:
                return -float('inf')
            return float('inf')

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
        exp, a_frac, b_frac = Arithmetic.equalize_exponent(self.exponents, self.fractions, other.exponents,
                                                           other.fractions)
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
        if first != 0:
            res, _ = Arithmetic.add_bits(res, BitOperation.num_map['1'], self.fraction_len + 1)
        exp, _ = Arithmetic.raw_sub_bits(exp, Arithmetic.str_to_integer(str(first), self.exponent_len))
        frac = BitOperation.raw_lshift_bits(res, first)[1:]

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
        a_frac = BitOperation.fraction_bits(self.fractions)
        b_frac = BitOperation.fraction_bits(other.fractions)

        exp, _ = Arithmetic.add_bits(self.exponents, other.exponents, self.exponent_len)
        bias = Arithmetic.str_to_integer('127', self.exponent_len)
        exp, _ = Arithmetic.raw_sub_bits(exp, bias)

        extra = BitOperation.empty_bits(self.fraction_len + 1)
        mul = a_frac
        over = BitOperation.empty_bits(self.fraction_len + 1)
        for bit in b_frac[:0:-1]:
            if bit:
                extra, overflow = Arithmetic.raw_add_bits(extra, mul)
                if overflow:
                    over, _ = Arithmetic.add_bits(over, BitOperation.num_map['1'], self.fraction_len+1)
            mul = BitOperation.raw_lshift_bits(mul, 1)
            if BitOperation.is_empty(mul):
                break

        res = BitOperation.empty_bits(self.fraction_len + 1)
        mul = a_frac
        for bit in b_frac:
            if bit:
                res, overflow = Arithmetic.raw_add_bits(res, mul)
                if overflow:
                    res = BitOperation.raw_rshift_bits(res, 1)
                    res[0] = overflow
                    exp, _ = Arithmetic.add_bits(exp, BitOperation.num_map['1'], self.exponent_len)
                    mul = BitOperation.raw_rshift_bits(mul, 1)
            mul = BitOperation.raw_rshift_bits(mul, 1)
            if BitOperation.is_empty(mul):
                break

        res, _ = Arithmetic.raw_add_bits(res, over)
        res = res[1:]
        return Float(exp, res, self.sign ^ other.sign)

    def __truediv__(self, other: "Float") -> "Float":
        """
        Binary Div 연산 ( / )을 위한 operator overloading
        :param other: Float 타입 가정
        :return: 새로운 Float 객체로 return
        """
        if other.is_zero():
            if self.is_zero():
                return self.nan()
            if self.sign ^ other.sign:
                return -self.inf()
            return self.inf()

        remain = BitOperation.fraction_bits(self.fractions)
        div = BitOperation.fraction_bits(other.fractions)
        exp, _ = Arithmetic.sub_bits(self.exponents, other.exponents, self.exponent_len)
        bias = Arithmetic.str_to_integer('127', self.exponent_len)
        exp, _ = Arithmetic.raw_add_bits(exp, bias)

        res = BitOperation.empty_bits(self.fraction_len+1)
        one = BitOperation.fit_bits(BitOperation.num_map['1'], self.fraction_len+1)

        for i in range(self.fraction_len, -1, -1):
            if BitOperation.raw_ge_bits(remain, div):
                remain, _ = Arithmetic.raw_sub_bits(remain, div)
                quotient = BitOperation.raw_lshift_bits(one, i)
                res = BitOperation.raw_or_bits(res, quotient)
                remain = BitOperation.raw_lshift_bits(remain, 1)
            else:
                div = BitOperation.raw_rshift_bits(div, 1)

        if BitOperation.first_bit_index(res) != 0:
            res = BitOperation.raw_lshift_bits(res, 1)
            exp, _ = Arithmetic.sub_bits(exp, BitOperation.num_map['1'], self.exponent_len)

        return Float(exp, res[1:], self.sign ^ other.sign)

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
