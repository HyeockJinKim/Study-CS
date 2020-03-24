from functools import reduce
from bit.bit import Bit
from nums.binary import Binary


class Integer:
    """
    Integer의 메모리 구조
    +--------------+----------------------------------------------------------------------+
    | sign (1 bit) |                            field (31 bit)                            |
    +--------------+----------------------------------------------------------------------+

    32 bit로 이루어진 integer 값

    양수 음수를 Sign bit를 통해 구분
    field 값을 통해 -(2**30-1)부터 2**30-1까지의 값을 표현함
    """
    bit_len = 32
    field_len = bit_len - 1
    limit = 2**bit_len
    frame = [2**i for i in range(bit_len-2, -1, -1)]
    default_field = [Bit() for _ in range(field_len)]

    def __init__(self, bits: list or str or int = None, sign: Bit = Bit()):
        if type(bits) == str:
            res = self.str_to_int(bits)
            self.sign = res.sign
            self.bits = res.bits
        elif type(bits) == int:
            self.sign = sign
            self.bits = self.default_field[::]
            self.set(bits)
        elif type(bits) == list:
            self.sign = sign
            self.bits = bits
        else:
            self.sign = sign
            self.bits = self.default_field[::]

    def is_zero(self) -> bool:
        """
        모든 비트가 0인지 확인하는 함수
        :return: 모든 비트가 0인지 여부
        """
        return not self.sign and not reduce(lambda x, y: x | y, self.bits)

    @classmethod
    def max_value(cls) -> "Integer":
        """
        Integer 의 최대값
        :return: Integer 의 최대값 (2**32 - 1)
        """
        max_list = [Bit(True) for _ in range(cls.field_len)]
        sign = Bit()
        return Integer(max_list, sign)

    @classmethod
    def min_value(cls) -> "Integer":
        """
        Integer 의 최소값
        :return: Integer 의 최소값 (-(2**32 - 1))
        """
        min_list = [Bit(True) for _ in range(cls.field_len)]
        sign = Bit(True)
        return Integer(min_list, sign)

    def set(self, _int: int):
        """
        int 값을 통해 integer 를 받기 위한 함수

        int 값을 Bit를 통해 int로 어떻게 표현하는 지 로직 확인을 위한 함수
        deprecated
        """
        if _int < 0:
            self.sign = Bit(True)
            _int = -_int
        else:
            self.sign = Bit()
        _int = _int % self.limit
        for i, x in enumerate(self.frame):
            self.bits[i].set(bool(_int & x))

    @classmethod
    def str_to_int(cls, val: str) -> "Integer":
        """
        String 값을 통해 integer 값 read
        :param val: String 으로 표현된 정수 값 (공백이 없다는 가정)
        :return: Integer 의 값
        """
        if val[0] == '-':
            sign = Bit(True)
            val = val[1:]
        else:
            sign = Bit()
        res = Integer()
        for c in val:
            res = res * cls.ten() + Integer(cls.char_to_dec(c))

        res.sign = sign
        return res

    @classmethod
    def char_to_dec(cls, val: str) -> list:
        """
        character 1 개를 0-9의 값으로 읽음
        :param val: 0-9의 문자열
        :return: Integer 객체
        """
        dec = cls.default_field[::]
        dec[-4:] = Binary.num_map[val]
        return dec

    @classmethod
    def ten(cls) -> "Integer":
        dec = cls.default_field[::]
        dec[-4:] = Binary.num_map['10']
        return Integer(dec)

    def val(self) -> int:
        """
        bit 들로 이루어진 값을 int 값으로 읽을 수 있도록 만드는 함수
        음수 확인은 signed bit를 통해 확인

        테스트 및 출력을 위해 사용하는 함수
        :return: int 값으로 리턴
        """
        res = 0
        for i, bit in enumerate(self.bits):
            if bit.val:
                res += self.frame[i]
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

    def complement(self) -> "Integer":
        """
        뺄셈을 위한 2의 보수 계산
        :return: 2의 보수 값
        """
        res = ~self
        return res._add(Integer('1'))

    def decomplement(self) -> "Integer":
        """
        음수 값은 2의 보수를 취한 값을 되돌림
        :return: sign 비트로 표현된 정수 값
        """
        res = self._add(self.min_value())
        return ~res

    def __invert__(self) -> "Integer":
        """
        Bit invert 연산( ~ )을 위한 operator overloading
        :return: 새로운 Integer 객체로 return
        """
        bits = [~bit for bit in self.bits]
        return Integer(bits, self.sign)

    def __neg__(self) -> "Integer":
        """
        sign minus 연산( - )을 위한 operator overloading
        :return: 새로운 Integer 객체로 return
        """
        return Integer(self.bits[::], ~self.sign)

    def __add__(self, other: "Integer") -> "Integer":
        """
        Binary Add 연산 ( + )을 위한 operator overloading
        음수는 2의 보수로 변환하여 계산
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        if self.is_negative():
            a = self.complement()
        else:
            a = self
        if other.is_negative():
            b = other.complement()
        else:
            b = other

        res = a._add(b)
        if res.is_negative():
            return res.decomplement()
        return res

    def _add(self, other: "Integer") -> "Integer":
        """
        음수일 경우 2의 보수가 취해진 후의 더하기 연산
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        if other.is_zero():
            return self

        carry = self & other
        remain = self ^ other
        if carry.bits[0]:
            remain.sign = remain.sign ^ carry.bits[0]
        return remain._add(carry << 1)

    def _add_check_overflow(self, other: "Integer") -> ("Integer", bool):
        if other.is_zero():
            return self, True

        carry = self & other
        remain = self ^ other
        if carry.bits[0]:
            return self, False
        return remain._add_check_overflow(carry << 1)

    def __sub__(self, other: "Integer") -> "Integer":
        """
        Binary Sub 연산 ( - )을 위한 operator overloading
        음수로 변경한 후 add 연산
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        return self + (-other)

    def __mul__(self, other: "Integer") -> "Integer":
        """
        Binary Mul 연산 ( * )을 위한 operator overloading
        덧셈의 반복으로 해결
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """

        res = Integer()
        for i, bit in enumerate(other.bits[::-1]):
            if bit:
                res += self << i
        res.sign = self.sign ^ other.sign
        return res

    def __truediv__(self, other: "Integer") -> "Integer":
        """
        Binary Div 연산 ( / )을 위한 operator overloading
        최고 자리수부터 shift 연산을 통해 뺄셈의 반복으로 해결
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        if other.is_zero():
            raise ZeroDivisionError()

        sign = self.sign ^ other.sign
        remain = Integer()
        res = Integer()
        for i in range(self.field_len-1, -1, -1):
            div, suc = other._lshift_check_overflow(i)
            if not suc:
                continue
            sum_val, suc = remain._add_check_overflow(div)
            if not suc:
                continue
            if sum_val._le(self):
                remain += div
                res |= Integer('1') << i

        res.sign = sign
        return res

    def __le__(self, other: "Integer") -> bool:
        """
        Low Equal 연산 ( <= )을 위한 operator overloading
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        if self.sign != other.sign:
            return self.sign == Bit()

        if self.is_negative():
            return other._le(self)
        return self._le(other)

    def _le(self, other: "Integer") -> bool:
        """
        Field 값만 비교
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        for i in range(self.field_len):
            if self.bits[i] > other.bits[i]:
                return False
        return True

    def __eq__(self, other: "Integer") -> bool:
        return self.val() == other.val() and self.sign == other.sign

    def __and__(self, other: "Integer") -> "Integer":
        """
        Bit And 연산( & )을 위한 operator overloading
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        return Integer([self.bits[i] & other.bits[i] for i in range(self.field_len)], self.sign & other.sign)

    def __xor__(self, other: "Integer") -> "Integer":
        """
        Bit XOR 연산( ^ )을 위한 operator overloading
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        return Integer([self.bits[i] ^ other.bits[i] for i in range(self.field_len)], self.sign ^ other.sign)

    def __or__(self, other: "Integer") -> "Integer":
        """
        Bit OR 연산( | )을 위한 operator overloading
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        return Integer([self.bits[i] | other.bits[i] for i in range(self.field_len)], self.sign | other.sign)

    def __lshift__(self, num: int) -> "Integer":
        """
        num 만큼 left shift ( << ) 연산을 위한 operator overloading
        :param num: shift 하는 크기
        :return: 새로운 Integer 객체로 return
        """
        bits = self.bits[num:]
        for _ in range(num):
            bits.append(Bit())
        return Integer(bits)

    def _lshift_check_overflow(self, num: int) -> ("Integer", bool):
        """
        Overflow를 확인하여 overflow되는 값이 있을 경우 shift 하지 않음
        :param num: shift 하는 크기
        :return: 새로운 Integer 객체로 return
        """
        for bit in self.bits[:num]:
            if bit:
                return self, False

        return self << num, True
