from bit.bit import Bit
from nums.arithmetic import Arithmetic
from nums.bit_operation import BitOperation


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

    def __init__(self, bits: list or str = None):
        if type(bits) == str:
            res = self.str_to_unsigned_int(bits)
            self.bits = res.bits
        elif type(bits) == list:
            self.bits = bits
        else:
            self.bits = BitOperation.empty_bits(self.field_len)

    def is_zero(self) -> bool:
        """
        모든 비트가 0인지 확인하는 함수
        :return: 모든 비트가 0인지 여부
        """
        return BitOperation.is_empty(self.bits)

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
        min_list = BitOperation.empty_bits(cls.field_len)
        return UnsignedInteger(min_list)

    @classmethod
    def str_to_unsigned_int(cls, val: str) -> "UnsignedInteger":
        """
        String 값을 통해 integer 값 read
        :param val: String 으로 표현된 정수 값 (공백이 없다는 가정)
        :return: UnsignedInteger 의 값
        """
        ten = UnsignedInteger(cls.char_to_dec('10'))
        if val[0] == '-':
            sign = Bit(True)
            val = val[1:]
        else:
            sign = Bit()
        res = UnsignedInteger()
        for c in val:
            res = res * ten + UnsignedInteger(cls.char_to_dec(c))

        if sign:
            res, _ = Arithmetic.complement_bits(res.bits)
            return UnsignedInteger(res)
        return res

    @classmethod
    def char_to_dec(cls, val: str) -> list:
        """
        character 1 개를 0-9의 값으로 읽음
        :param val: 0-9의 문자열
        :return: UnsignedInteger 객체
        """
        return BitOperation.fit_bits(BitOperation.num_map[val], cls.field_len)

    def val(self) -> int:
        """
        bit 들로 이루어진 값을 int 값으로 읽을 수 있도록 만드는 함수
        음수 값이 없으므로 모두 양수 읽는 것처럼 읽
        :return:
        """
        return BitOperation.binary_to_decimal(self.bits)

    def __str__(self) -> str:
        return str(self.val())

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
        return UnsignedInteger(Arithmetic.complement_bits(self.bits))

    def __add__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Binary Add 연산 ( + )을 위한 operator overloading
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """

        res, _ = Arithmetic.add_bits(self.bits, other.bits)
        return UnsignedInteger(res)

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

        return UnsignedInteger(Arithmetic.mul_bits(self.bits, other.bits))

    def __truediv__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Binary Div 연산 ( / )을 위한 operator overloading
        최고 자리수부터 shift 연산을 통해 뺄셈의 반복으로 해결
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        return UnsignedInteger(Arithmetic.div_bits(self.bits, other.bits))

    def __le__(self, other: "UnsignedInteger") -> bool:
        """
        Low Equal 연산 ( <= )을 위한 operator overloading
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        return BitOperation.le_bits(self.bits, other.bits)

    def __eq__(self, other: "UnsignedInteger") -> bool:
        return BitOperation.eq_bits(self.bits, other.bits)

    def __and__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Bit And 연산( & )을 위한 operator overloading
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        return UnsignedInteger(BitOperation.and_bits(self.bits, other.bits))

    def __xor__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Bit XOR 연산( ^ )을 위한 operator overloading
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        return UnsignedInteger(BitOperation.xor_bits(self.bits, other.bits))

    def __or__(self, other: "UnsignedInteger") -> "UnsignedInteger":
        """
        Bit OR 연산( | )을 위한 operator overloading
        :param other: UnsignedInteger 타입 가정
        :return: 새로운 UnsignedInteger 객체로 return
        """
        return UnsignedInteger(BitOperation.or_bits(self.bits, other.bits))

    def __lshift__(self, num: int) -> "UnsignedInteger":
        """
        num 만큼 left shift ( << ) 연산을 위한 operator overloading
        :param num: shift 하는 크기
        :return: 새로운 UnsignedInteger 객체로 return
        """
        res, _ = BitOperation.lshift_bits(self.bits, num)
        return UnsignedInteger(res)
