from alu.logic_gate import *


def half_adder_gate(a: Bit, b: Bit) -> (Bit, Bit):
    """
    반가산기
    LSB (최하위 비트)에 대하여 연산 처리
    두 비트의 덧셈만을 고려
    :param a: 덧셈을 수행할 비트 1
    :param b: 덧셈을 수행할 비트 2
    :return: 덧셈 수행 결과 (sum: 해당 비트에 남은 결과, carry: 상위 비트로 전달될 값)
    """
    s = xor_gate(a, b)
    c = and_gate(a, b)
    return s, c


def full_adder_gate(a: Bit, b: Bit, carry_in: Bit) -> (Bit, Bit):
    """
    전가산기
    LSB 외의 모든 비트에 대하여 연산 처리
    두 비트의 덧셈에 하위 비트에서 전달받은 carry 값을 함께 연산
    두 비트와 carry 값의 3 값을 고려
    :param a: 덧셈을 수행할 비트 1
    :param b: 덧셈을 수행할 비트 2
    :param carry_in: 하위 비트에서 전달받은 carry 값
    :return: 덧셈 수행 결과 (sum: 해당 비트에 남은 결과, carry: 상위 비트로 전달될 값)
    """
    t1 = xor_gate(a, b)
    s = xor_gate(t1, carry_in)

    t2 = and_gate(t1, carry_in)
    t3 = and_gate(a, b)
    c = xor_gate(t2, t3)
    return s, c
