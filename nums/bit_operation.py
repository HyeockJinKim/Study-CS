from functools import reduce
from typing import List

from bit.bit import Bit


class BitOperation:
    num_map = {
        '0': [],
        '1': [Bit(True)],
        '2': [Bit(True), Bit()],
        '3': [Bit(True), Bit(True)],
        '4': [Bit(True), Bit(), Bit()],
        '5': [Bit(True), Bit(), Bit(True)],
        '6': [Bit(True), Bit(True), Bit()],
        '7': [Bit(True), Bit(True), Bit(True)],
        '8': [Bit(True), Bit(), Bit(), Bit()],
        '9': [Bit(True), Bit(), Bit(), Bit(True)],
        '10': [Bit(True), Bit(), Bit(True), Bit()],
    }

    @staticmethod
    def equalize_bit_length(a: List[Bit], b: List[Bit], length: int) -> (List[Bit], List[Bit]):
        a = BitOperation.fit_bits(a, length)
        b = BitOperation.fit_bits(b, length)
        return a, b

    @staticmethod
    def eq_bits(a: List[Bit], b: List[Bit], length: int) -> bool:
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_eq_bits(a, b)

    @staticmethod
    def raw_eq_bits(a: List[Bit], b: List[Bit]) -> bool:
        for i in range(len(a)):
            if a[i] != b[i]:
                return False
        return True

    @staticmethod
    def le_bits(a: List[Bit], b: List[Bit], length: int) -> bool:
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_le_bits(a, b)

    @staticmethod
    def raw_le_bits(a: List[Bit], b: List[Bit]) -> bool:
        for i in range(len(a)):
            if a[i] > b[i]:
                return False
            if b[i] > a[i]:
                return True
        return True

    @staticmethod
    def and_bits(a: List[Bit], b: List[Bit], length: int) -> List[Bit]:
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_and_bits(a, b)

    @staticmethod
    def raw_and_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        return [a[i] & b[i] for i in range(len(a))]

    @staticmethod
    def xor_bits(a: List[Bit], b: List[Bit], length: int) -> List[Bit]:
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_xor_bits(a, b)

    @staticmethod
    def raw_xor_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        return [a[i] ^ b[i] for i in range(len(a))]

    @staticmethod
    def or_bits(a: List[Bit], b: List[Bit], length: int) -> List[Bit]:
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_or_bits(a, b)

    @staticmethod
    def raw_or_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        return [a[i] | b[i] for i in range(len(a))]

    @staticmethod
    def lshift_bits(a: List[Bit], index: int or List[Bit], length: int) -> List[Bit]:
        if type(index) == list:
            index = BitOperation.binary_to_decimal(index)

        a = BitOperation.fit_bits(a, length)
        return BitOperation.raw_lshift_bits(a, index)

    @staticmethod
    def raw_lshift_bits(a: List[Bit], index: int) -> List[Bit]:
        bits = BitOperation.empty_bits(len(a))
        bits[:len(a) - index] = a[index:]
        return bits

    @staticmethod
    def neg_bits(a: List[Bit]) -> List[Bit]:
        return [~bit for bit in a]

    @staticmethod
    def fit_bits(a: List[Bit], length: int) -> List[Bit]:
        if len(a) >= length:
            return a[-length:]
        if len(a) == length:
            return a[::]

        empty = BitOperation.empty_bits(length)
        for i in range(1, len(a)+1):
            empty[-i] = a[-i]
        return empty

    @staticmethod
    def is_empty(a: List[Bit]) -> bool:
        return not reduce(lambda x, y: x | y, a)

    @staticmethod
    def empty_bits(length: int) -> List[Bit]:
        return [Bit() for _ in range(length)]

    @staticmethod
    def binary_to_decimal(a: List[Bit]) -> int:
        res = 0
        frame = 1
        for bit in a[::-1]:
            if bit:
                res += frame
            frame <<= 1
        return res

    @staticmethod
    def first_bit_index(a: List[Bit]) -> int:
        for i in range(len(a)):
            if a[i]:
                return i
        return len(a)
