from typing import List
from bit.bit import Bit


class Word:
    length = 32

    def __init__(self, bit_list: List[Bit] = None):
        if not bit_list:
            bit_list = [Bit() for _ in range(self.length)]
        self.bit_list = bit_list

    def __getitem__(self, item: int) -> "Bit":
        return self.bit_list[item]

    def __setitem__(self, key: int, value: Bit):
        self.bit_list[key] = value

    def msb(self):
        return self.bit_list[0]

    def lsb(self):
        return self.bit_list[-1]
