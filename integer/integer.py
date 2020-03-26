from bit.bit import Bit
from nums.arithmetic import Arithmetic
from nums.bit_operation import BitOperation


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

    def __init__(self, bits: list or str or int = None, sign: Bit = Bit()):
        if type(bits) == str:
            res = self.str_to_int(bits)
            self.sign = res.sign
            self.bits = res.bits
        elif type(bits) == int:
            self.sign = sign
            self.bits = BitOperation.empty_bits(self.field_len)
            self._set(bits)
        elif type(bits) == list:
            self.sign = sign
            self.bits = bits
        else:
            self.sign = sign
            self.bits = BitOperation.empty_bits(self.field_len)

    def is_zero(self) -> bool:
        """
        모든 비트가 0인지 확인하는 함수
        :return: 모든 비트가 0인지 여부
        """
        return not self.sign and BitOperation.is_empty(self.bits)

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

    def _set(self, _int: int):
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
        ten = Integer(cls.char_to_dec('10'))

        if val[0] == '-':
            sign = Bit(True)
            val = val[1:]
        else:
            sign = Bit()
        res = Integer()
        for c in val:
            res = res * ten + Integer(cls.char_to_dec(c))

        res.sign = sign
        return res

    @classmethod
    def char_to_dec(cls, val: str) -> list:
        """
        character 0-10의 값으로 읽음
        :param val: 0-10의 문자열
        :return: Integer 객체
        """
        return BitOperation.fit_bits(BitOperation.num_map[val], cls.field_len)

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
            a_bits, _ = Arithmetic.complement_bits(self.bits)
        else:
            a_bits = self.bits[::]
        if other.is_negative():
            b_bits, _ = Arithmetic.complement_bits(other.bits)
        else:
            b_bits = other.bits[::]

        res, overflow = Arithmetic.add_bits(a_bits, b_bits)
        sign = self.sign ^ other.sign ^ overflow
        if sign:
            return Integer(Arithmetic.decomplement_bits(res), sign)
        return Integer(res, sign)

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
        return Integer(Arithmetic.mul_bits(self.bits, other.bits), self.sign ^ other.sign)

    def __truediv__(self, other: "Integer") -> "Integer":
        """
        Binary Div 연산 ( / )을 위한 operator overloading
        최고 자리수부터 shift 연산을 통해 뺄셈의 반복으로 해결
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        return Integer(Arithmetic.div_bits(self.bits, other.bits), self.sign ^ other.sign)

    def __le__(self, other: "Integer") -> bool:
        """
        Low Equal 연산 ( <= )을 위한 operator overloading
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        if self.sign != other.sign:
            return self.sign == Bit()

        if self.is_negative():
            return BitOperation.le_bits(other.bits, self.bits)
        return BitOperation.le_bits(self.bits, other.bits)

    def __eq__(self, other: "Integer") -> bool:
        return self.sign == other.sign and BitOperation.eq_bits(self.bits, other.bits)

    def __and__(self, other: "Integer") -> "Integer":
        """
        Bit And 연산( & )을 위한 operator overloading
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        return Integer(BitOperation.and_bits(self.bits, other.bits), self.sign & other.sign)

    def __xor__(self, other: "Integer") -> "Integer":
        """
        Bit XOR 연산( ^ )을 위한 operator overloading
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        return Integer(BitOperation.xor_bits(self.bits, other.bits), self.sign ^ other.sign)

    def __or__(self, other: "Integer") -> "Integer":
        """
        Bit OR 연산( | )을 위한 operator overloading
        :param other: Integer 타입 가정
        :return: 새로운 Integer 객체로 return
        """
        return Integer(BitOperation.or_bits(self.bits, other.bits), self.sign | other.sign)

    def __lshift__(self, num: int) -> "Integer":
        """
        num 만큼 left shift ( << ) 연산을 위한 operator overloading
        :param num: shift 하는 크기
        :return: 새로운 Integer 객체로 return
        """
        res, _ = BitOperation.lshift_bits(self.bits, num)
        return Integer(res)
