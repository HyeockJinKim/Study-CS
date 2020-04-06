import enum
from bit.bit import Bit


class ControlSignal(enum.Enum):
    NOT = [Bit(), Bit(), Bit(), Bit()]                 # 0
    AND = [Bit(), Bit(), Bit(), Bit(True)]             # 1
    NAND = [Bit(), Bit(), Bit(True), Bit()]            # 2
    OR = [Bit(), Bit(), Bit(True), Bit(True)]          # 3
    NOR = [Bit(), Bit(True), Bit(), Bit()]             # 4
    XOR = [Bit(), Bit(True), Bit(), Bit(True)]         # 5
    XNOR = [Bit(), Bit(True), Bit(True), Bit()]        # 6
    INC = [Bit(), Bit(True), Bit(True), Bit(True)]     # 7
    DEC = [Bit(True), Bit(), Bit(), Bit()]             # 8
    MINUS = [Bit(True), Bit(), Bit(), Bit(True)]       # 9
    ADD = [Bit(True), Bit(), Bit(True), Bit()]         # 10
    SUB = [Bit(True), Bit(), Bit(True), Bit(True)]     # 11
    LSHIFT = [Bit(True), Bit(True), Bit(), Bit()]      # 12
    RSHIFT = [Bit(True), Bit(True), Bit(), Bit(True)]  # 13
