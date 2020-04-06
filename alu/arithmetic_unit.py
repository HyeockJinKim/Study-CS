from alu.logic_unit import *
from alu.arithmetic_gate import *


def incrementer_32bit(a: Word) -> Word:
    """
    1을 더하는 연산

    :param a: 1을 더할 값 Word
    :return: 1을 더한 값 Word
    """
    c = Bit(True)
    word = Word()
    for i in range(a.length-1, -1, -1):
        word[i], c = full_adder_gate(a[i], Bit(), c)
    return word


def adder_32bit(a: Word, b: Word) -> Word:
    """
    32 bit 단위의 덧셈 연산
    LSB (최하위 비트)에 대해서는 반가산기를 이용한 덧셈 연산을 수행하고
    상위 비트들에 대해서는 전가산기를 통해 하위 비트의 carry 비트 값을 고려해 덧셈 연산

    :param a: 덧셈 연산을 수행할 Word 1
    :param b: 덧셈 연산을 수행할 Word 2
    :return: 덧셈 연산 수행 결과 Word
    """
    word = Word()
    word[-1], c = half_adder_gate(a.lsb(), b.lsb())
    for i in range(a.length-2, -1, -1):
        word[i], c = full_adder_gate(a[i], b[i], c)
    return word


def complementer_32bit(a: Word) -> Word:
    """
    32 bit 단위의 2의 보수 연산
    뺄셈 연산을 위한 Gate 대신 보수를 취하여 뺄셈을 구현 가능

    1의 보수는 0이 +0과 -0의 두 값이 생기기 때문에 모호할 수 있고
    2의 보수는 1 비트를 더 사용할 수 있어 최소값이 1비트 더 큰 수를 가질 수 있음

    :param a: 2의 보수 연산을 수행할 Word
    :return: 2의 보수 연산 수행 결과 Word
    """
    word = invert_32bit(a)
    one = incrementer_32bit(Word())
    res = adder_32bit(word, one)
    return res


def decrementer_32bit(a: Word) -> Word:
    """
    1을 빼는 연산

    :param a: 1을 뺄 값 Word
    :return: 1을 뺀 값 Word
    """
    minus_one = Word([Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True),
                      Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True),
                      Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True),
                      Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True), Bit(True)])
    return adder_32bit(a, minus_one)


def subtract_32bit(a: Word, b: Word) -> Word:
    """
    32 bit 단위의 뺄셈 연산
    빼는 값에 2의 보수를 취하여 덧셈 연산을 수행

    :param a: 뺄셈 연산을 수행할 Word 1
    :param b: 뺄셈 연산을 수행할 Word 2
    :return: 뺄셈 연산 수행 결과 Word
    """
    complement = complementer_32bit(b)
    return adder_32bit(a, complement)
