

class Bit:
    """
    bit 표현
    """
    def __init__(self, val: bool = False):
        self.val: bool = val

    def set(self, _val: bool):
        self.val = _val

    def __str__(self):
        return str(int(self.val))

    def __repr__(self):
        return self.__str__()

    def __invert__(self):
        """
        Bit invert 연산( ~ )을 위한 operator overloading
        :return: 새로운 Bit 객체로 return
        """
        return Bit(not self.val)

    def __eq__(self, other: "Bit"):
        return self.val == other.val

    def __gt__(self, other: "Bit"):
        """
        Greater 연산 ( > )을 위한 operator overloading
        :param other: Bit 타입 가정
        :return: 새로운 Bit 객체로 return
        """
        return self.val and not other.val

    def __xor__(self, other: "Bit"):
        """
        Bit XOR 연산( ^ )을 위한 operator overloading
        :param other: Bit 타입 가정
        :return: 새로운 Bit 객체로 return
        """
        return Bit(self.val ^ other.val)

    def __and__(self, other: "Bit"):
        """
        Bit AND 연산( & )을 위한 operator overloading
        :param other: Bit 타입 가정
        :return: 새로운 Bit 객체로 return
        """
        return Bit(self.val & other.val)

    def __or__(self, other: "Bit"):
        """
        Bit Or 연산( | )을 위한 operator overloading
        :param other: Bit 타입 가정
        :return: 새로운 Bit 객체로 return
        """
        return Bit(self.val | other.val)

    def __bool__(self):
        """
        Bool 값 operator overloading
        :return: val 값
        """
        return self.val
