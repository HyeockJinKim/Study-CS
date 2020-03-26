from functools import reduce
from typing import List

from bit.bit import Bit


class BitOperation:
    num_map = {
        '0': [Bit(), Bit(), Bit(), Bit()],
        '1': [Bit(), Bit(), Bit(), Bit(True)],
        '2': [Bit(), Bit(), Bit(True), Bit()],
        '3': [Bit(), Bit(), Bit(True), Bit(True)],
        '4': [Bit(), Bit(True), Bit(), Bit()],
        '5': [Bit(), Bit(True), Bit(), Bit(True)],
        '6': [Bit(), Bit(True), Bit(True), Bit()],
        '7': [Bit(), Bit(True), Bit(True), Bit(True)],
        '8': [Bit(True), Bit(), Bit(), Bit()],
        '9': [Bit(True), Bit(), Bit(), Bit(True)],
        '10': [Bit(True), Bit(), Bit(True), Bit()],
    }

    @staticmethod
    def equalize_bit_length(a: List[Bit], b: List[Bit]) -> (List[Bit], List[Bit]):
        if len(a) < len(b):
            b, a = a, b
        if len(a) != len(b):
            b = BitOperation.fit_bits(b, len(a))
        return a, b

    @staticmethod
    def eq_bits(a: List[Bit], b: List[Bit]):
        a, b = BitOperation.equalize_bit_length(a, b)
        return BitOperation._eq_bits(a, b)

    @staticmethod
    def _eq_bits(a: List[Bit], b: List[Bit]):
        for i in range(len(a)):
            if a[i] != b[i]:
                return False
        return True

    @staticmethod
    def le_bits(a: List[Bit], b: List[Bit]):
        a, b = BitOperation.equalize_bit_length(a, b)
        return BitOperation._le_bits(a, b)

    @staticmethod
    def _le_bits(a: List[Bit], b: List[Bit]):
        for i in range(len(a)):
            if a[i] > b[i]:
                return False
            if b[i] > a[i]:
                return True
        return True

    @staticmethod
    def and_bits(a: List[Bit], b: List[Bit]):
        a, b = BitOperation.equalize_bit_length(a, b)
        return BitOperation._and_bits(a, b)

    @staticmethod
    def _and_bits(a: List[Bit], b: List[Bit]):
        return [a[i] & b[i] for i in range(len(a))]

    @staticmethod
    def xor_bits(a: List[Bit], b: List[Bit]):
        a, b = BitOperation.equalize_bit_length(a, b)
        return BitOperation._xor_bits(a, b)

    @staticmethod
    def _xor_bits(a: List[Bit], b: List[Bit]):
        return [a[i] ^ b[i] for i in range(len(a))]

    @staticmethod
    def or_bits(a: List[Bit], b: List[Bit]):
        a, b = BitOperation.equalize_bit_length(a, b)
        return BitOperation._or_bits(a, b)

    @staticmethod
    def _or_bits(a: List[Bit], b: List[Bit]):
        return [a[i] | b[i] for i in range(len(a))]

    @staticmethod
    def lshift_bits(a: List[Bit], index: int or List[Bit]):
        if index == 0:
            return a, False
        bits = a[index:]
        for _ in range(index):
            bits.append(Bit())
        return bits, not BitOperation.is_empty(a[:index])

    @staticmethod
    def neg_bits(a: List[Bit]):
        return [~bit for bit in a]

    @staticmethod
    def fit_bits(a: List[Bit], length: int):
        empty = BitOperation.empty_bits(length)
        for i in range(1, len(a)+1):
            empty[-i] = a[-i]
        return empty

    @staticmethod
    def is_empty(a: List[Bit]):
        return not reduce(lambda x, y: x | y, a)

    @staticmethod
    def empty_bits(length: int):
        return [Bit() for _ in range(length)]

    @staticmethod
    def binary_to_decimal(a: List[Bit]) -> int:
        res = 0
        frame = 1
        for i, bit in enumerate(a):
            if bit.val:
                res += frame
                frame <<= 1
        return res
