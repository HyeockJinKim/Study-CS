from word.word import Word
from alu.logic_gate import *


def invert_32bit(a: Word) -> Word:
    """
    32 bit 단위의 invert 연산
    1의 보수 연산으로도 수행

    :param a: invert 연산을 수행할 Word
    :return: invert 연산 수행 결과 Word
    """
    return Word([not_gate(a[i]) for i in range(Word.length)])


def and_32bit(a: Word, b: Word) -> Word:
    """
    32 bit 단위의 AND 논리 연산

    :param a: AND 논리 연산을 수행할 Word 1
    :param b: AND 논리 연산을 수행할 Word 2
    :return: AND 논리 연산 수행 결과 Word
    """
    return Word([and_gate(a[i], b[i]) for i in range(Word.length)])


def or_32bit(a: Word, b: Word) -> Word:
    """
    32 bit 단위의 OR 논리 연산

    :param a: OR 논리 연산을 수행할 Word 1
    :param b: OR 논리 연산을 수행할 Word 2
    :return: OR 논리 연산 수행 결과 Word
    """
    return Word([or_gate(a[i], b[i]) for i in range(Word.length)])


def xor_32bit(a: Word, b: Word) -> Word:
    """
    32 bit 단위의 XOR 논리 연산

    :param a: XOR 논리 연산을 수행할 Word 1
    :param b: XOR 논리 연산을 수행할 Word 2
    :return: XOR 논리 연산 수행 결과 Word
    """
    return Word([xor_gate(a[i], b[i]) for i in range(Word.length)])


def nand_32bit(a: Word, b: Word) -> Word:
    """
    32 bit 단위의 NAND 논리 연산

    :param a: NAND 논리 연산을 수행할 Word 1
    :param b: NAND 논리 연산을 수행할 Word 2
    :return: NAND 논리 연산 수행 결과 Word
    """
    return Word([nand_gate(a[i], b[i]) for i in range(Word.length)])


def nor_32bit(a: Word, b: Word) -> Word:
    """
    32 bit 단위의 NOR 논리 연산

    :param a: NOR 논리 연산을 수행할 Word 1
    :param b: NOR 논리 연산을 수행할 Word 2
    :return: NOR 논리 연산 수행 결과 Word
    """
    return Word([nor_gate(a[i], b[i]) for i in range(Word.length)])


def xnor_32bit(a: Word, b: Word) -> Word:
    """
    32 bit 단위의 XNOR 논리 연산

    :param a: XNOR 논리 연산을 수행할 Word 1
    :param b: XNOR 논리 연산을 수행할 Word 2
    :return: XNOR 논리 연산 수행 결과 Word
    """
    return Word([xnor_gate(a[i], b[i]) for i in range(Word.length)])


def logical_lshift_32bit(a: Word, num: int) -> Word:
    """
    32 bit 단위의 Logical left-shift 연산
    shift 된 위치의 값은 0으로 채워짐

    :param a: logical left-shift 연산을 수행할 Word
    :param num: logical left-shift 연산을 수행할 크기
    :return: logical left-shift 연산 수핼 결과 Word
    """
    # TODO: shift gate를 통한 계산으로 변경 필요
    # TODO: Barrel shift 구현
    word = Word()
    for new_index, old_index in range(num, Word.length):
        word[new_index] = a[old_index]

    return word


def logical_rshift_32bit(a: Word, num: int) -> Word:
    """
    32 bit 단위의 Logical right-shift 연산
    shift 된 위치의 값은 0으로 채워짐

    :param a: logical right-shift 연산을 수행할 Word
    :param num: logical right-shift 연산을 수행할 크기
    :return: logical right-shift 연산 수핼 결과 Word
    """
    # TODO: shift gate를 통한 계산으로 변경 필요
    # TODO: Barrel shift 구현
    word = Word()
    for new_index, old_index in range(num, Word.length):
        word[old_index] = a[new_index]

    return word


def pass_through_32bit(a: Word) -> Word:
    """
    입력에 아무런 연산도 처리하지 않고 반환하는 연산

    :param a: 그대로 반환할 값 Word
    :return: 입력과 같은 값 Word
    """
    return Word([bit for bit in a.bit_list])

