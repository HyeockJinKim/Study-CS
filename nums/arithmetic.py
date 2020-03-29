from typing import List

from bit.bit import Bit
from nums.bit_operation import BitOperation


class Arithmetic:
    @staticmethod
    def complement_bits(a: List[Bit], length: int) -> (List[Bit], Bit):
        a = BitOperation.fit_bits(a, length)
        a = BitOperation.neg_bits(a)
        return Arithmetic.add_bits(a, [Bit(True)], length)

    @staticmethod
    def decomplement_bits(a: List[Bit], length: int) -> List[Bit]:
        a = BitOperation.fit_bits(a, length)
        a, _ = Arithmetic.add_bits(a, [Bit(True) for _ in range(len(a))], length)
        return BitOperation.neg_bits(a)

    @staticmethod
    def add_bits(a: List[Bit], b: List[Bit], length: int) -> (List[Bit], Bit):
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return Arithmetic.raw_add_bits(a, b)

    @staticmethod
    def raw_add_bits(a: List[Bit], b: List[Bit]) -> (List[Bit], Bit):
        if BitOperation.is_empty(b):
            return a, Bit()
        carry_0 = BitOperation.raw_and_bits(a, b)
        remain = BitOperation.raw_xor_bits(a, b)
        carry = BitOperation.raw_lshift_bits(carry_0, 1)

        res, overflow = Arithmetic.raw_add_bits(remain, carry)
        return res, overflow ^ carry_0[0]

    @staticmethod
    def sub_bits(a: List[Bit], b: List[Bit], length: int) -> (List[Bit], Bit):
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return Arithmetic.raw_sub_bits(a, b)

    @staticmethod
    def raw_sub_bits(a: List[Bit], b: List[Bit]) -> (List[Bit], Bit):
        b, _ = Arithmetic.complement_bits(b, len(b))
        return Arithmetic.raw_add_bits(a, b)

    @staticmethod
    def mul_bits(a: List[Bit], b: List[Bit], length: int) -> List[Bit]:
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return Arithmetic.raw_mul_bits(a, b)

    @staticmethod
    def raw_mul_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        res = BitOperation.empty_bits(len(a))
        for i, bit in enumerate(b[::-1]):
            if bit:
                mul2 = BitOperation.raw_lshift_bits(a, i)
                res, _ = Arithmetic.raw_add_bits(res, mul2)
        return res

    @staticmethod
    def div_bits(a: List[Bit], b: List[Bit], length: int) -> List[Bit]:
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return Arithmetic.raw_div_bits(a, b)

    @staticmethod
    def raw_div_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
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
        diff, _ = Arithmetic.raw_sub_bits(a_exp, b_exp)
        diff = BitOperation.binary_to_decimal(diff)

        b_fraction = BitOperation.raw_rshift_bits(b_frac, diff)
        if not BitOperation.is_empty(b_frac[:diff]):
            b_fraction, _ = Arithmetic.add_bits(b_fraction, BitOperation.num_map['1'], len(b_fraction))
            return b_fraction
        return b_fraction

    @staticmethod
    def add_fraction(a: List[Bit], b: List[Bit], length: int) -> (List[Bit], Bit):
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return Arithmetic.raw_add_fraction(a, b)

    @staticmethod
    def raw_add_fraction(a: List[Bit], b: List[Bit]) -> (List[Bit], Bit):
        if BitOperation.is_empty(b):
            return a, Bit()
        carry_0 = BitOperation.raw_and_bits(a, b)
        remain = BitOperation.raw_xor_bits(a, b)
        carry = BitOperation.raw_lshift_bits(carry_0, 1)

        res, overflow = Arithmetic.raw_add_fraction(remain, carry)
        return res, overflow ^ carry_0[0]

    @staticmethod
    def str_to_integer(val: str, length: int) -> (List[Bit], Bit):
        res, ten = BitOperation.equalize_bit_length(BitOperation.num_map['0'], BitOperation.num_map['10'], length)
        for c in val:
            res = Arithmetic.raw_mul_bits(res, ten)
            res, _ = Arithmetic.add_bits(res, BitOperation.num_map[c], length)
        return res

    @staticmethod
    def str_to_integer_until_overflow(val: str, length: int):
        res, ten = BitOperation.equalize_bit_length(BitOperation.num_map['0'], BitOperation.num_map['10'], length)
        for i, c in enumerate(val):
            res = Arithmetic.raw_mul_bits(res, ten)
            res, res2 = Arithmetic.add_bits(res, BitOperation.num_map[c], length)

            if res2:
                return res, len(val) - i
        return res, length - BitOperation.first_bit_index(res) - 1

    @staticmethod
    def str_to_minor(real: List[Bit], val: str, digit: int, length: int):
        real, ten = BitOperation.equalize_bit_length(real, BitOperation.num_map['10'], length)
        base = BitOperation.fit_bits(BitOperation.num_map['1'], length)
        twenty = BitOperation.raw_lshift_bits(ten, 1)
        remain = BitOperation.empty_bits(length)
        shift = 1
        index = 0
        while True:
            if index < len(val):
                remain = Arithmetic.raw_mul_bits(remain, twenty)
                next_digit = BitOperation.lshift_bits(BitOperation.num_map[val[index]], shift, length)
                remain, _ = Arithmetic.raw_add_bits(remain, next_digit)
                base = Arithmetic.raw_mul_bits(base, ten)
                index += 1
                shift += 1
            else:
                remain = BitOperation.raw_lshift_bits(remain, 1)
                if BitOperation.is_empty(real):
                    return real, -127

            if BitOperation.first_bit_index(real) == 0:
                real = BitOperation.raw_lshift_bits(real, 1)
                if not BitOperation.is_empty(remain):
                    real, _ = Arithmetic.add_bits(real, BitOperation.num_map['1'], length)
                break

            real = BitOperation.raw_lshift_bits(real, 1)
            if BitOperation.raw_ge_bits(remain, base):
                real, _ = Arithmetic.add_bits(real, BitOperation.num_map['1'], length)
                remain, _ = Arithmetic.sub_bits(remain, base, length)

            if BitOperation.is_empty(real):
                digit -= 1
                continue

        return real, digit
