from typing import Dict, Callable

from alu.control_signal import ControlSignal
from alu.arithmetic_unit import *
from alu.logic_unit import *


class ALU:
    """
    Arithmetic Logic Unit
    """

    def __init__(self):
        self.op: Dict[ControlSignal, Callable] = {
            ControlSignal.NOT: lambda x, y: invert_32bit(x),
            ControlSignal.AND: lambda x, y: and_32bit(x, y),
            ControlSignal.NAND: lambda x, y: nand_32bit(x, y),
            ControlSignal.OR: lambda x, y: or_32bit(x, y),
            ControlSignal.NOR: lambda x, y: nor_32bit(x, y),
            ControlSignal.XOR: lambda x, y: xor_32bit(x, y),
            ControlSignal.XNOR: lambda x, y: xnor_32bit(x, y),
            ControlSignal.INC: lambda x, y: incrementer_32bit(x),
            ControlSignal.DEC: lambda x, y: decrementer_32bit(x),
            ControlSignal.MINUS: lambda x, y: complementer_32bit(x),
            ControlSignal.ADD: lambda x, y: adder_32bit(x, y),
            ControlSignal.SUB: lambda x, y: subtract_32bit(x, y),
            ControlSignal.LSHIFT: lambda x, y: logical_lshift_32bit(x),
            ControlSignal.RSHIFT: lambda x, y: logical_rshift_32bit(x),
        }

    def func(self, x: Word, y: Word, control: ControlSignal):
        return self.op[control](x, y)
