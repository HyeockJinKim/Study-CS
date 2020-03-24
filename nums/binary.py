from bit.bit import Bit


class Binary:
    num_map = {
        '0': [Bit(), Bit(), Bit(), Bit()],
        '1': [Bit(), Bit(), Bit(), Bit(True)],
        '2': [Bit(), Bit(), Bit(True), Bit()],
        '3': [Bit(), Bit(), Bit(True), Bit(True)],
        '4': [Bit(), Bit(True), Bit(), Bit()],
        '5': [Bit(), Bit(True), Bit(), Bit(True)],
        '6': [Bit(), Bit(True), Bit(True), Bit()],
        '7': [Bit(), Bit(True), Bit(True), Bit(True)],
        '8': [Bit(True), Bit(), Bit(), Bit()],
        '9': [Bit(True), Bit(), Bit(), Bit(True)],
        '10': [Bit(True), Bit(), Bit(True), Bit()],
    }
