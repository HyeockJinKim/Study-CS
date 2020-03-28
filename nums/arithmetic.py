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
    def _mul_bits_with_overflow(a: List[Bit], b: List[Bit]) -> List[Bit]:
        res = BitOperation.empty_bits(len(a))
        for i, bit in enumerate(b[::-1]):
            if bit:
                mul2 = BitOperation.raw_lshift_bits(a, i)
                res, overflow = Arithmetic.raw_add_bits(res, mul2)
                if overflow:
                    res.insert(0, overflow)
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
    def str_to_integer(val: str, length: int) -> (List[Bit], Bit):
        res = BitOperation.num_map['0']
        ten = BitOperation.num_map['10']
        for c in val:
            res = Arithmetic.mul_bits(res, ten, length)
            res, res2 = Arithmetic.add_bits(res, BitOperation.num_map[c], length)
            if res2:
                res.insert(0, res2)
        return res
