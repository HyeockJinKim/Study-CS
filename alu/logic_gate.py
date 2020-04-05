from bit.bit import Bit


def not_gate(a: Bit) -> Bit:
    """
    NOT Gate
    1 비트 ~ 연산을 위한 Gate
    비트 값이 1일 경우 0인 비트,
    비트 값이 0일 경우 1인 비트를 반환

    :param a: NOT Gate의 입력 비트
    :return: Not Gate의 결과 비트
    """
    return Bit(not a.val)


def and_gate(a: Bit, b: Bit) -> Bit:
    """
    AND Gate
    1 비트 & 연산을 위한 Gate
    a 비트의 값이 1 이면서 b 비트의 값이 1인 경우 1인 비트,
    이 외의 경우에는 0인 비트를 반환

    :param a: AND Gate의 입력 비트 1
    :param b: AND Gate의 입력 비트 2
    :return: AND Gate의 결과 비트
    """
    return Bit(a.val and b.val)


def or_gate(a: Bit, b: Bit) -> Bit:
    """
    OR Gate
    1 비트 | 연산을 위한 Gate
    a 비트의 값, b 비트의 값 둘 중 하나 이상의 비트가 1인 경우 1인 비트,
    이외의 경우에는 0인 비트를 반환

    :param a: OR Gate의 입력 비트 1
    :param b: OR Gate의 입력 비트 2
    :return: OR Gate의 결과 비트
    """
    return Bit(a.val or b.val)


def xor_gate(a: Bit, b: Bit) -> Bit:
    """
    XOR Gate
    1 비트 ^ 연산을 위한 Gate
    a 비트의 값, b 비트의 값 둘 중 단 하나의 비트만이 1인 경우 1인 비트,
    이외의 경우에는 0인 비트를 반환

    :param a: XOR Gate의 입력 비트 1
    :param b: XOR Gate의 입력 비트 2
    :return: XOR Gate의 결과 비트
    """
    t1 = and_gate(a, b)
    t2 = nand_gate(a, b)
    return and_gate(t1, t2)


def nand_gate(a: Bit, b: Bit) -> Bit:
    """
    NAND Gate
    NAND 논리 연산을 위한 Gate

    a 비트의 값이 1 이면서 b 비트의 값이 1인 경우 0인 비트,
    이 외의 경우에는 1인 비트를 반환

    :param a: NAND Gate의 입력 비트 1
    :param b: NAND Gate의 입력 비트 2
    :return: NAND Gate의 결과 비트
    """
    return not_gate(and_gate(a, b))


def nor_gate(a: Bit, b: Bit) -> Bit:
    """
    NOR Gate
    NOR 논리 연산을 위한 Gate

    a 비트의 값이 0 이면서 b 비트의 값이 0인 경우 1인 비트,
    이 외의 경우에는 0인 비트를 반환

    :param a: NOR Gate의 입력 비트 1
    :param b: NOR Gate의 입력 비트 2
    :return: NOR Gate의 결과 비트
    """
    return not_gate(or_gate(a, b))


def xnor_gate(a: Bit, b: Bit) -> Bit:
    """
    XNOR Gate
    XNOR 논리 연산을 위한 Gate

    a 비트와 b 비트의 값이 같은 경우에만 1인 비트,
    a 비트와 b 비트의 값이 다른 경우에는 0인 비트를 반환

    :param a: XNOR Gate의 입력 비트 1
    :param b: XNOR Gate의 입력 비트 2
    :return: XNOR Gate의 결과 비트
    """
    return not_gate(xor_gate(a, b))
