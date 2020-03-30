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
        """
        입력받은 두 Bit List의 길이를 length 길이로 만듦
        :param a: length 길이로 맞출 Bit List
        :param b: length 길이로 맞출 Bit List
        :param length: 원하는 Bit List의 길이
        :return: length 길이의 a, b
        """
        a = BitOperation.fit_bits(a, length)
        b = BitOperation.fit_bits(b, length)
        return a, b

    @staticmethod
    def eq_bits(a: List[Bit], b: List[Bit], length: int) -> bool:
        """
        두 Bit List의 길이를 length 길이로 맞춘 뒤 같은 지 ( == ) 비교
        raw_eq_bits 함수를 통해 비교
        :param a: equal 인지 확인하기 위한 BitList
        :param b: 비교 BitList
        :param length: 원하는 Bit List의 길이
        :return: 값이 같은 지 여부
        """
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_eq_bits(a, b)

    @staticmethod
    def raw_eq_bits(a: List[Bit], b: List[Bit]) -> bool:
        """
        같은 길이의 Bit List를 값이 같은 지 ( == ) 비교
        :param a: equal 인지 확인하기 위한 BitList
        :param b: 비교 BitList
        :return: 값이 같은 지 여부
        """
        for i in range(len(a)):
            if a[i] != b[i]:
                return False
        return True

    @staticmethod
    def le_bits(a: List[Bit], b: List[Bit], length: int) -> bool:
        """
        두 Bit List의 길이를 length 길이로 맞춘 뒤 a가 작거나 같은 지 ( <= ) 비교
        raw_le_bits 함수를 통해 비교
        :param a: low-equal 인지 확인하기 위한 BitList
        :param b: 비교 BitList
        :param length: 원하는 Bit List의 길이
        :return: 값이 작거나 같은지 여부
        """
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_le_bits(a, b)

    @staticmethod
    def raw_le_bits(a: List[Bit], b: List[Bit]) -> bool:
        """
        같은 길이의 Bit List 중 a가 작거나 같은 지 ( <= ) 비교
        :param a: low-equal 인지 확인하기 위한 BitList
        :param b: 비교 BitList
        :return: 값이 작거나 같은지 여부
        """
        for i in range(len(a)):
            if a[i] > b[i]:
                return False
            if b[i] > a[i]:
                return True
        return True

    @staticmethod
    def ge_bits(a: List[Bit], b: List[Bit], length: int) -> bool:
        """
        두 Bit List의 길이를 length 길이로 맞춘 뒤 a가 크거나 같은 지 ( >= ) 비교
        raw_ge_bits 함수를 통해 비교
        :param a: greater-equal 인지 확인하기 위한 BitList
        :param b: 비교 BitList
        :param length: 원하는 Bit List의 길이
        :return: 값이 크거나 같은 지 여부
        """
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_ge_bits(a, b)

    @staticmethod
    def raw_ge_bits(a: List[Bit], b: List[Bit]) -> bool:
        """
        같은 길이의 Bit List 중 a가 크거나 같은 지 ( >= ) 비교
        :param a: greater-equal 인지 확인하기 위한 BitList
        :param b: 비교 BitList
        :return: 값이 크거나 같은 지 여부
        """
        for i in range(len(a)):
            if a[i] > b[i]:
                return True
            if b[i] > a[i]:
                return False
        return True

    @staticmethod
    def and_bits(a: List[Bit], b: List[Bit], length: int) -> List[Bit]:
        """
        Bit List의 길이를 같게 만든 후 And ( & ) 연산
        raw_and_bits 함수를 통해 연산
        :param a: And 연산을 수행할 Bit List
        :param b: And 연산을 수행할 Bit List
        :param length: 원하는 Bit List의 길이
        :return: And 연산 결과 Bit List
        """
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_and_bits(a, b)

    @staticmethod
    def raw_and_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        """
        Bit List 의 And ( & ) 연산
        :param a: And 연산을 수행할 Bit List
        :param b: And 연산을 수행할 Bit List
        :return: And 연산 결과 Bit List
        """
        return [a[i] & b[i] for i in range(len(a))]

    @staticmethod
    def xor_bits(a: List[Bit], b: List[Bit], length: int) -> List[Bit]:
        """
        Bit List의 길이를 같게 만든 후 Xor ( ^ ) 연산
        raw_xor_bits 함수를 통해 연산
        :param a: Xor 연산을 수행할 Bit List
        :param b: Xor 연산을 수행할 Bit List
        :param length: 원하는 Bit List의 길이
        :return: Xor 연산 결과 Bit List
        """
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_xor_bits(a, b)

    @staticmethod
    def raw_xor_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        """
        Bit List 의 Xor ( ^ ) 연산
        :param a: Xor 연산을 수행할 Bit List
        :param b: Xor 연산을 수행할 Bit List
        :return: Xor 연산 결과 Bit List
        """
        return [a[i] ^ b[i] for i in range(len(a))]

    @staticmethod
    def or_bits(a: List[Bit], b: List[Bit], length: int) -> List[Bit]:
        """
        Bit List의 길이를 같게 만든 후 Or ( | ) 연산
        raw_or_bits 함수를 통해 연산
        :param a: Or 연산을 수행할 Bit List
        :param b: Or 연산을 수행할 Bit List
        :param length: 원하는 Bit List의 길이
        :return: Or 연산 결과 Bit List
        """
        a, b = BitOperation.equalize_bit_length(a, b, length)
        return BitOperation.raw_or_bits(a, b)

    @staticmethod
    def raw_or_bits(a: List[Bit], b: List[Bit]) -> List[Bit]:
        """
        Bit List 의 Or ( | ) 연산
        :param a: Or 연산을 수행할 Bit List
        :param b: Or 연산을 수행할 Bit List
        :return: Or 연산 결과 Bit List
        """
        return [a[i] | b[i] for i in range(len(a))]

    @staticmethod
    def lshift_bits(a: List[Bit], index: int or List[Bit], length: int) -> List[Bit]:
        """
        Bit List의 길이를 length 길이로 만든 후 left-shift ( << ) 연산
        index를 Bit List 값일 경우 shift 연산을 위해 int 값으로 변경
        raw_lshift_bits 함수 이용
        :param a: left-shift 연산할 Bit List
        :param index: left-shift 할 크기
        :param length: 원하는 Bit List의 길이
        :return: index 크기만큼 left-shift 한 Bit List
        """
        if type(index) == list:
            index = BitOperation.binary_to_decimal(index)

        a = BitOperation.fit_bits(a, length)
        return BitOperation.raw_lshift_bits(a, index)

    @staticmethod
    def raw_lshift_bits(a: List[Bit], index: int) -> List[Bit]:
        """
        Bit List를 left-shift ( << ) 연산
        :param a: left-shift 연산할 Bit List
        :param index: left-shift 할 크기
        :return: index 크기만큼 left-shift 한 Bit List
        """
        bits = BitOperation.empty_bits(len(a))
        bits[:len(a) - index] = a[index:]
        return bits

    @staticmethod
    def rshift_bits(a: List[Bit], index: int or List[Bit], length: int) -> List[Bit]:
        """
        Bit List의 길이를 length 길이로 만든 후 right-shift ( >> ) 연산
        index를 Bit List 값일 경우 shift 연산을 위해 int 값으로 변경
        raw_rshift_bits 함수 이용
        :param a: right-shift 연산할 Bit List
        :param index: right-shift 할 크기
        :param length: 원하는 Bit List의 길이
        :return: index 크기만큼 right-shift 한 Bit List
        """
        if type(index) == list:
            index = BitOperation.binary_to_decimal(index)

        a = BitOperation.fit_bits(a, length)
        return BitOperation.raw_rshift_bits(a, index)

    @staticmethod
    def raw_rshift_bits(a: List[Bit], index: int) -> List[Bit]:
        """
        Bit List를 right-shift ( >> )연산
        :param a: right-shift 연산할 Bit List
        :param index: right-shift 할 크기
        :return: index 크기만큼 right-shift 한 Bit List
        """
        bits = BitOperation.empty_bits(len(a))
        bits[index:] = a[:len(a) - index]
        return bits

    @staticmethod
    def fraction_bits(a: List[Bit]) -> List[Bit]:
        """
        float 값의 fraction에 생략된 1을 추가하는 함수
        :param a: 소수점의 유효숫자만 표현된 가수 값
        :return: 1이 추가된 가수 값
        """
        frac = a[::]
        frac.insert(0, Bit(True))
        return frac

    @staticmethod
    def neg_bits(a: List[Bit]) -> List[Bit]:
        """
        Bit List에 Negate ( ~ ) 연산
        Bit List의 모든 Bit의 값을 반대로 뒤집음
        :param a: Negate 연산할 Bit List
        :return: Negate 연산된 Bit List
        """
        return [~bit for bit in a]

    @staticmethod
    def fit_bits(a: List[Bit], length: int) -> List[Bit]:
        """
        Bit List를 length 길이로 만듦
        length 보다 길 경우 뒤에서부터 length 길이로 자르고
        length 보다 짧을 경우 0을 앞에 추가함

        :param a: length 길이로 만들 Bit List
        :param length: 원하는 Bit List의 길이
        :return: length 길이의 Bit List
        """
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
        """
        Bit List의 모든 Bit 가 0인지 확인
        :param a: 모든 Bit 가 0인지 확인할 함수
        :return: 모든 Bit 가 0인지 여부
        """
        if not a:
            return True
        return not reduce(lambda x, y: x | y, a)

    @staticmethod
    def empty_bits(length: int) -> List[Bit]:
        """
        length 길이의 비어있는 Bit List를 생성하는 함수
        :param length: 원하는 Bit List의 길이
        :return: 비어있는 length 길이의 Bit List
        """
        return [Bit() for _ in range(length)]

    @staticmethod
    def binary_to_decimal(a: List[Bit]) -> int:
        """
        입력받은 Bit List의 값을 읽어 int로 변환하는 함수
        python 의 기능을 실행시키기 위해 int로 변환할 때 사용 ( << 연산 등 )
        :param a: int 값을 확인하기 위한 Bit List
        :return: Bit List에 해당하는 int 값
        """
        res = 0
        frame = 1
        for bit in a[::-1]:
            if bit:
                res += frame
            frame <<= 1
        return res

    @staticmethod
    def binary_to_float(exp: List[Bit], fraction: List[Bit]) -> float:
        """
        입력받은 exponent와 fraction을 읽어 float값으로 변환하는 함수
        :param exp: exponent (지수) 값
        :param fraction: fraction (가수) 값
        :return: 가수 * 2 ^ 지수
        """
        res = 0
        exp = BitOperation.binary_to_decimal(exp) - 127 - len(fraction)
        frame = 2 ** exp
        for bit in fraction[::-1]:
            if bit:
                res += frame
            frame *= 2
        res += frame
        return res

    @staticmethod
    def first_bit_index(a: List[Bit]) -> int:
        """
        Bit List에서 첫 1의 위치를 찾는 함수
        없을 경우 Bit List의 길이 값을 return
        :param a: 첫 1의 위치를 찾을 Bit List
        :return: 첫 1의 위치
        """
        for i in range(len(a)):
            if a[i]:
                return i
        return len(a)
