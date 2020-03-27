from typing import List

from bit.bit import Bit
from nums.bit_operation import BitOperation


class Arithmetic:
    @staticmethod
    def complement_bits(a: List[Bit]) -> (List[Bit], Bit):
        a = BitOperation.neg_bits(a)
        return Arithmetic.add_bits(a, [Bit(True)])

    @staticmethod
    def decomplement_bits(a: List[Bit]) -> List[Bit]:
        a, _ = Arithmetic.add_bits(a, [Bit(True) for _ in range(len(a))])
        return BitOperation.neg_bits(a)

    @staticmethod
    def add_bits(a: List[Bit], b: List[Bit]) -> (List[Bit], Bit):
        a, b = BitOperation.equalize_bit_length(a, b)
        return Arithmetic._add_bits(a, b)

    @staticmethod
    def _add_bits(a: List[Bit], b: List[Bit]) -> (List[Bit], Bit):
        if BitOperation.is_empty(b):
            return a, Bit()
        carry = BitOperation.and_bits(a, b)
        remain = BitOperation.xor_bits(a, b)
        carry, _ = BitOperation.lshift_bits(carry, 1)

        res, overflow = Arithmetic._add_bits(remain, carry)
        return res, overflow ^ carry[0]

    @staticmethod
    def mul_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        a, b = BitOperation.equalize_bit_length(a, b)
        return Arithmetic._mul_bits(a, b)

    @staticmethod
    def _mul_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        res = BitOperation.empty_bits(len(a))
        for i, bit in enumerate(b[::-1]):
            if bit:
                mul2, _ = BitOperation.lshift_bits(a, i)
                res, _ = Arithmetic.add_bits(res, mul2)
        return res

    @staticmethod
    def div_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        a, b = BitOperation.equalize_bit_length(a, b)
        return Arithmetic._div_bits(a, b)

    @staticmethod
    def _div_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        if BitOperation.is_empty(b):
            raise ZeroDivisionError()

        remain = BitOperation.empty_bits(len(a))
        res = BitOperation.empty_bits(len(a))
        one = BitOperation.fit_bits(BitOperation.num_map['1'], len(a))

        for i in range(len(a) - 1, -1, -1):
            div, overflow = BitOperation.lshift_bits(b, i)
            if overflow:
                continue
            sum_val, overflow = Arithmetic.add_bits(remain, div)
            if overflow:
                continue
            if BitOperation.le_bits(sum_val, a):
                remain, _ = Arithmetic.add_bits(remain, div)
                quotient, _ = BitOperation.lshift_bits(one, i)
                res = BitOperation.or_bits(res, quotient)

        return res

    @staticmethod
    def str_to_integer(val: str) -> (List[Bit], Bit):
        # TODO: Should be changed
        res = BitOperation.empty_bits(32)
        ten = BitOperation.num_map['10']
        overflow = Bit()
        for c in val:
            res = Arithmetic.mul_bits(res, ten)
            res, res2 = Arithmetic.add_bits(res, BitOperation.num_map[c])
            overflow ^= res2
        return res, overflow
