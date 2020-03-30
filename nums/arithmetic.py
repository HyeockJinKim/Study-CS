from typing import List

from bit.bit import Bit
from nums.bit_operation import BitOperation


class Arithmetic:
    @staticmethod
    def complement_bits(a: List[Bit], length: int) -> (List[Bit], Bit):
        """
        Bit List의 2의 보수를 계산
        - 연산을 하기 위해 2의 보수 계산
        :param a: 2의 보수를 계산하는 Bit List
        :param length: 원하는 Bit List의 길이
        :return: Bit List의 2의 보수 값
        """
        a = BitOperation.fit_bits(a, length)
        a = BitOperation.neg_bits(a)
        return Arithmetic.add_bits(a, [Bit(True)], length)

    @staticmethod
    def decomplement_bits(a: List[Bit], length: int) -> List[Bit]:
        """
        2의 보수 값을 되돌리는 함수
        signed number 값에서 연산 후 2의 보수 값을 되돌리기 위한 함수
        :param a: 2의 보수로 표현된 Bit List
        :param length: 원하는 Bit List의 길이
        :return: 2의 보수를 되돌린 Bit List 값
        """
        a = BitOperation.fit_bits(a, length)
        a, _ = Arithmetic.add_bits(a, [Bit(True) for _ in range(len(a))], length)
        return BitOperation.neg_bits(a)

    @staticmethod
    def add_bits(a: List[Bit], b: List[Bit], length: int) -> (List[Bit], Bit):
        """
        Bit List의 길이를 length로 맞춘 후 값을 더하는 ( + ) 함수
        이진수를 더하는 함수
        overflow 될 경우 overflow 값을 함께 return
        raw_add_bits 함수를 통해 계산
        :param a: 더할 Bit List
        :param b: 더할 Bit List
        :param length: 원하는 Bit List의 길이
        :return: a + b의 값인 Bit List, overflow 된 Bit
        """
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return Arithmetic.raw_add_bits(a, b)

    @staticmethod
    def raw_add_bits(a: List[Bit], b: List[Bit]) -> (List[Bit], Bit):
        """
        같은 길이의 Bit List를 더하는 ( + ) 함수
        덧셈 결과 overflow 되었는지 여부를 함께 return

        and ( & ) 연산, xor ( ^ ) 연산과 left-shift ( << ) 연산을 통해 덧셈을 구현

        :param a: 더할 Bit List
        :param b: 더할 Bit List
        :return: a + b의 값인 Bit List, overflow 된 Bit
        """
        if BitOperation.is_empty(b):
            return a, Bit()
        carry_0 = BitOperation.raw_and_bits(a, b)
        remain = BitOperation.raw_xor_bits(a, b)
        carry = BitOperation.raw_lshift_bits(carry_0, 1)

        res, overflow = Arithmetic.raw_add_bits(remain, carry)
        return res, overflow ^ carry_0[0]

    @staticmethod
    def sub_bits(a: List[Bit], b: List[Bit], length: int) -> (List[Bit], Bit):
        """
        Bit List의 길이를 length로 맞춘 후 값을 빼는 ( - ) 함수
        이진수를 빼는 함수
        overflow 될 경우 overflow 값을 함께 return
        raw_sub_bits 함수를 통해 계산
        :param a: - 앞의 Bit List
        :param b: 뺄 Bit List
        :param length: 원하는 Bit List의 길이
        :return: a - b의 값인 Bit List, overflow 된 Bit
        """
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return Arithmetic.raw_sub_bits(a, b)

    @staticmethod
    def raw_sub_bits(a: List[Bit], b: List[Bit]) -> (List[Bit], Bit):
        """
        같은 길이의 Bit List를 빼는 ( - ) 함수

        b의 값을 2의 보수를 취한 후 add ( + ) 연산을 수행

        :param a: - 앞의 Bit List
        :param b: 뺄 Bit List
        :return: a - b의 값인 Bit List, overflow 된 Bit
        """
        b, _ = Arithmetic.complement_bits(b, len(b))
        return Arithmetic.raw_add_bits(a, b)

    @staticmethod
    def mul_bits(a: List[Bit], b: List[Bit], length: int) -> List[Bit]:
        """
        Bit List의 길이를 length로 맞춘 후 값을 곱하는 ( * ) 함수
        이진수를 곱하는 함수
        raw_mul_bits 함수를 통해 계산
        :param a: * 앞의 Bit List
        :param b: 곱할 Bit List
        :param length: 원하는 Bit List의 길이
        :return: a * b의 값인 Bit List
        """
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return Arithmetic.raw_mul_bits(a, b)

    @staticmethod
    def raw_mul_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        """
        같은 길이의 Bit List를 곱하는 ( * ) 함수

        b Bit List의 값을 하위 비트부터 상위 비트까지 1인 비트가 있을 때마다 a bit를 left-shift하여 더함

        :param a: * 앞의 Bit List
        :param b: 곱할 Bit List
        :return: a * b의 값인 Bit List
        """
        res = BitOperation.empty_bits(len(a))
        for i, bit in enumerate(b[::-1]):
            if bit:
                mul2 = BitOperation.raw_lshift_bits(a, i)
                res, _ = Arithmetic.raw_add_bits(res, mul2)
        return res

    @staticmethod
    def div_bits(a: List[Bit], b: List[Bit], length: int) -> List[Bit]:
        """
        Bit List의 길이를 length로 맞춘 후 값을 나누는 ( / ) 함수
        이진수를 나누는 함수
        raw_div_bits 함수를 통해 계산
        :param a: / 앞의 Bit List
        :param b: 나눌 Bit List
        :param length: 원하는 Bit List의 길이
        :return: a / b의 값인 Bit List
        """
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return Arithmetic.raw_div_bits(a, b)

    @staticmethod
    def raw_div_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        """
        같은 길이의 Bit List를 나누는 ( / ) 함수

        left-shift ( << ) 연산과 add ( + ) 연산, lower-equal ( <= ) 연산을 통해 나눗셈 구현
        상위 비트부터 하위 비트까지 값을 빼면서 몫을 구함

        :param a: / 앞의 Bit List
        :param b: 나눌 Bit List
        :return: a / b의 값인 Bit List
        """
        if BitOperation.is_empty(b):
            raise ZeroDivisionError()

        remain = BitOperation.empty_bits(len(a))
        res = BitOperation.empty_bits(len(a))
        one = BitOperation.fit_bits(BitOperation.num_map['1'], len(a))

        for i in range(len(a) - 1, -1, -1):
            first_bit = BitOperation.first_bit_index(b)
            if first_bit < i:
                continue
            div = BitOperation.raw_lshift_bits(b, i)
            sum_val, overflow = Arithmetic.raw_add_bits(remain, div)
            if overflow:
                continue
            if BitOperation.raw_le_bits(sum_val, a):
                remain, _ = Arithmetic.raw_add_bits(remain, div)
                quotient = BitOperation.raw_lshift_bits(one, i)
                res = BitOperation.raw_or_bits(res, quotient)

        return res

    @staticmethod
    def equalize_exponent(a_exp: List[Bit], a_frac: List[Bit], b_exp: List[Bit], b_frac: List[Bit]):
        """
        두 float 값의 exponent 값이 같게 만들고 fraction을 조정함
        :param a_exp: a의 exponent ( 지수 )
        :param a_frac: a의 fraction ( 가수 )
        :param b_exp: b의 exponent ( 지수 )
        :param b_frac: b의 fraction ( 가수 )
        :return: 같은 exponent, exponent에 맞춰 조정된 a의 fraction, exponent에 맞춰 조정된 b의 fraction
        """
        a_frac = BitOperation.fraction_bits(a_frac)
        b_frac = BitOperation.fraction_bits(b_frac)

        if BitOperation.raw_ge_bits(a_exp, b_exp):
            b_frac = Arithmetic.shift_fraction(a_exp, b_exp, b_frac)
            exp = a_exp
        else:
            a_frac = Arithmetic.shift_fraction(b_exp, a_exp, a_frac)
            exp = b_exp

        return exp, a_frac, b_frac

    @staticmethod
    def shift_fraction(a_exp: List[Bit], b_exp: List[Bit], b_frac: List[Bit]):
        """
        float의 exponent 값 차이만큼 shift 한 fraction 값 연산
        right-shift 연산 할 때 생략된 값이 있을 때 1을 더함
        :param a_exp: 비교하는 exponent
        :param b_exp: 비교하는 exponent
        :param b_frac: shift 연산할 fraction
        :return: shift 연산 된 fraction
        """
        diff, _ = Arithmetic.raw_sub_bits(a_exp, b_exp)
        diff = BitOperation.binary_to_decimal(diff)

        b_fraction = BitOperation.raw_rshift_bits(b_frac, diff)
        if not BitOperation.is_empty(b_frac[:diff]):
            b_fraction, _ = Arithmetic.add_bits(b_fraction, BitOperation.num_map['1'], len(b_fraction))
            return b_fraction
        return b_fraction

    @staticmethod
    def str_to_integer(val: str, length: int) -> List[Bit]:
        """
        문자열을 읽어 Bit List를 생성하는 함수
        10진수에서 2진수로 변환하는 함수

        :param val: 숫자를 표현하는 정수 문자열
        :param length: 원하는 Bit List의 길이
        :return: 문자열 숫자에 해당하는 Bit List
        """
        res, ten = BitOperation.equalize_bit_length(BitOperation.num_map['0'], BitOperation.num_map['10'], length)
        for c in val:
            res = Arithmetic.raw_mul_bits(res, ten)
            res, _ = Arithmetic.add_bits(res, BitOperation.num_map[c], length)
        return res

    @staticmethod
    def str_to_integer_until_overflow(val: str, length: int) -> (List[Bit], int):
        """
        문자열을 읽어 overflow가 발생할 때까지 Bit List를 생성하는 함수
        :param val: 숫자를 표현하는 정수 문자열
        :param length: 원하는 Bit List의 길이
        :return: 문자열 실수값에 해당하는 Bit List, 자리수
        """
        res, ten = BitOperation.equalize_bit_length(BitOperation.num_map['0'], BitOperation.num_map['10'], length)
        for i, c in enumerate(val):
            res = Arithmetic.raw_mul_bits(res, ten)
            res, res2 = Arithmetic.add_bits(res, BitOperation.num_map[c], length)

            if res2:
                return res, len(val) - i
        return res, length - BitOperation.first_bit_index(res) - 1

    @staticmethod
    def str_to_minor(real: List[Bit], val: str, digit: int, length: int) -> (List[Bit], int):
        """
        소수점 아래의 값을 표현하는 문자열을 읽어 Bit List를 생성하는 함수

        :param real: 소수점 위의 값의 Bit List
        :param val: 소수점 아래의 값을 표현하는 문자열
        :param digit: 소수점 위의 자리수
        :param length: 원하는 Bit List의 길이
        :return: 문자열 실수값에 해당하는 Bit List, 자리수
        """
        real, ten = BitOperation.equalize_bit_length(real, BitOperation.num_map['10'], length)
        base = BitOperation.fit_bits(BitOperation.num_map['1'], length)
        twenty = BitOperation.raw_lshift_bits(ten, 1)
        remain = BitOperation.empty_bits(length)
        shift = 1
        index = 0
        while True:
            if index < len(val) and index < 6:
                remain = Arithmetic.raw_mul_bits(remain, twenty)
                next_digit = BitOperation.lshift_bits(BitOperation.num_map[val[index]], shift, length)
                remain, _ = Arithmetic.raw_add_bits(remain, next_digit)
                index += 1
                shift += 1
                base = Arithmetic.raw_mul_bits(base, ten)
            else:
                remain = BitOperation.raw_lshift_bits(remain, 1)
                if BitOperation.is_empty(BitOperation.raw_or_bits(remain, real)):
                    return real, -127

            real = BitOperation.raw_lshift_bits(real, 1)
            if BitOperation.raw_ge_bits(remain, base):
                real, _ = Arithmetic.add_bits(real, BitOperation.num_map['1'], length)
                remain, _ = Arithmetic.sub_bits(remain, base, length)

            if BitOperation.first_bit_index(real) == 0:
                remain = BitOperation.raw_lshift_bits(remain, 1)
                if BitOperation.raw_ge_bits(remain, base):
                    real = BitOperation.or_bits(real, BitOperation.num_map['1'], length)
                break
            elif BitOperation.is_empty(real):
                digit -= 1

        return real, digit
