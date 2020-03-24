from functools import reduce
from bit.bit import Bit
from nums.binary import Binary


class UnsignedInteger:
    """
    Integer의 메모리 구조
    +-------------------------------------------------------------------------------------+
    |                                    field (32 bit)                                   |
    +-------------------------------------------------------------------------------------+

    32 bit로 이루어진 unsigned integer 값

    음수를 표현할 수 없음
    field 값을 통해 0부터 2**31-1까지의 값을 표현함
    """
    bit_len = 32
    field_len = bit_len
    limit = 2**(bit_len+1)
    frame = [2**i for i in range(bit_len-1, -1, -1)]
    default_field = [Bit() for _ in range(field_len)]

    def __init__(self, bits: list or str or int = None):
        if type(bits) == str:
            res = self.str_to_int(bits)
            self.bits = res.bits
        elif type(bits) == int:
            self.bits = self.default_field[::]
            self.set(bits)
        elif type(bits) == list:
            self.bits = bits
        else:
            self.bits = self.default_field[::]

    def is_zero(self) -> bool:
        """
        모든 비트가 0인지 확인하는 함수
        :return: 모든 비트가 0인지 여부
        """
        return not reduce(lambda x, y: x | y, self.bits)

    @classmethod
    def max_value(cls) -> "UnsignedInteger":
        """
        UnsignedInteger 의 최대값
        :return: UnsignedInteger 의 최대값 (2**33 - 1)
        """
        max_list = [Bit(True) for _ in range(cls.field_len)]
        return UnsignedInteger(max_list)

    @classmethod
    def min_value(cls) -> "UnsignedInteger":
        """
        UnsignedInteger 의 최소값
        :return: UnsignedInteger 의 최소값 0
        """
        min_list = cls.default_field[::]
        return UnsignedInteger(min_list)

    def set(self, _int: int):
        """
        int 값을 통해 unsigned integer 를 받기 위한 함수

        int 값을 Bit를 통해 unsigned int로 어떻게 표현하는 지 로직 확인을 위한 함수
        deprecated
        """
        _int = _int % self.limit
        for i, x in enumerate(self.frame):
            self.bits[i].set(bool(_int & x))

    @classmethod
    def str_to_int(cls, val: str) -> "UnsignedInteger":
        """
        String 값을 통해 integer 값 read
        :param val: String 으로 표현된 정수 값 (공백이 없다는 가정)
        :return: UnsignedInteger 의 값
        """
        if val[0] == '-':
            sign = Bit(True)
            val = val[1:]
        else:
            sign = Bit()
        res = UnsignedInteger()
        for c in val:
            res = res * cls.ten() + UnsignedInteger(cls.char_to_dec(c))

        if sign:
            return res.complement()
        return res

    @classmethod
    def char_to_dec(cls, val: str) -> list:
        """
        character 1 개를 0-9의 값으로 읽음
        :param val: 0-9의 문자열
        :return: UnsignedInteger 객체
        """
        dec = cls.default_field[::]
        dec[-4:] = Binary.num_map[val]
        return dec

    @classmethod
    def ten(cls) -> "UnsignedInteger":
        dec = cls.default_field[::]
        dec[-4:] = Binary.num_map['10']
        return UnsignedInteger(dec)

    def val(self) -> int:
        """
        bit 들로 이루어진 값을 int 값으로 읽을 수 있도록 만드는 함수
        음수 값이 없으므로 모두 양수 읽는 것처럼 읽
        :return:
        """
        res = 0
        for i, bit in enumerate(self.bits):
            if bit.val:
                res += self.frame[i]
        return res

    def __str__(self) -> str:
        return str(self.val())

    def complement(self) -> "UnsignedInteger":
        """
        뺄셈을 위한 2의 보수 계산
        :return: 2의 보수 값
        """
        res = ~self
        return res + UnsignedInteger('1')

    def __invert__(self) -> "UnsignedInteger":
        """
        Bit invert 연산( ~ )을 위한 operator overloading
        :return: 새로운 UnsignedInteger 객체로 return
        """
        bits = [~bit for bit in self.bits]
        return UnsignedInteger(bits)

    def __neg__(self) -> "UnsignedInteger":
        """
        sign minus 연산( - )을 위한 operator overloading
        2의 보수를 취한 값을 가짐
        :return: 새로운 UnsignedInteger 객체로 return
        """
        return self.complement()

    def __add__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Binary Add 연산 ( + )을 위한 operator overloading
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        if other.is_zero():
            return self

        carry = self & other
        remain = self ^ other
        return remain + (carry << 1)

    def _add_check_overflow(self, other: "UnsignedInteger") -> ("UnsignedInteger", bool):
        if other.is_zero():
            return self, True

        carry = self & other
        remain = self ^ other
        if carry.bits[0]:
            return self, False
        return remain._add_check_overflow(carry << 1)

    def __sub__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Binary Sub 연산 ( - )을 위한 operator overloading
        음수로 변경한 후 add 연산
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        return self + (-other)

    def __mul__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Binary Mul 연산 ( * )을 위한 operator overloading
        덧셈의 반복으로 해결
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """

        res = UnsignedInteger()
        for i, bit in enumerate(other.bits[::-1]):
            if bit:
                res += self << i
        return res

    def __truediv__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Binary Div 연산 ( / )을 위한 operator overloading
        최고 자리수부터 shift 연산을 통해 뺄셈의 반복으로 해결
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        if other.is_zero():
            raise ZeroDivisionError()

        remain = UnsignedInteger()
        res = UnsignedInteger()
        for i in range(self.field_len-1, -1, -1):
            div, suc = other._lshift_check_overflow(i)
            if not suc:
                continue
            if div.is_zero():
                continue

            sum_val, suc = remain._add_check_overflow(div)
            if not suc:
                continue
            if sum_val <= self:
                remain += div
                res |= UnsignedInteger('1') << i

        return res

    def __le__(self, other: "UnsignedInteger") -> bool:
        """
        Low Equal 연산 ( <= )을 위한 operator overloading
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        for i in range(self.field_len - 1, -1, -1):
            if self.bits[i] > other.bits[i]:
                return False
        return True

    def __eq__(self, other: "UnsignedInteger") -> bool:
        return self.val() == other.val()

    def __and__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Bit And 연산( & )을 위한 operator overloading
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        return UnsignedInteger([self.bits[i] & other.bits[i] for i in range(self.field_len)])

    def __xor__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Bit XOR 연산( ^ )을 위한 operator overloading
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        return UnsignedInteger([self.bits[i] ^ other.bits[i] for i in range(self.field_len)])

    def __or__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Bit OR 연산( | )을 위한 operator overloading
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        return UnsignedInteger([self.bits[i] | other.bits[i] for i in range(self.field_len)])

    def __lshift__(self, num: int) -> "UnsignedInteger":
        """
        num 만큼 left shift ( << ) 연산을 위한 operator overloading
        :param num: shift 하는 크기
        :return: 새로운 UnsignedInteger 객체로 return
        """
        bits = self.bits[num:]
        for _ in range(num):
            bits.append(Bit())
        return UnsignedInteger(bits)

    def _lshift_check_overflow(self, num: int) -> ("UnsignedInteger", bool):
        """
        Overflow 를 확인하여 overflow 되는 값이 있을 경우 shift 하지 않음
        :param num: shift 하는 크기
        :return: 새로운 Integer 객체로 return
        """
        for bit in self.bits[:num]:
            if bit:
                return self, False

        return self << num, True
