import machine


class Pico:
    _instance = None

    gp0 = machine.Pin(1)
    gp1 = machine.Pin(2)
    gp2 = machine.Pin(4)
    gp3 = machine.Pin(5)
    gp4 = machine.Pin(6)
    gp5 = machine.Pin(7)
    gp6 = machine.Pin(9)
    gp7 = machine.Pin(10)
    gp8 = machine.Pin(11)
    gp9 = machine.Pin(12)
    gp10 = machine.Pin(14)
    gp11 = machine.Pin(15)
    gp12 = machine.Pin(16)
    gp13 = machine.Pin(17)
    gp14 = machine.Pin(19)
    gp15 = machine.Pin(20)
    gp16 = machine.Pin(21)
    gp17 = machine.Pin(22)
    gp18 = machine.Pin(24)
    gp19 = machine.Pin(25)
    gp20 = machine.Pin(26)
    gp21 = machine.Pin(27)
    gp22 = machine.Pin(29)
    gp25 = machine.Pin(25)

    def __init__(self):
        ...
#        raise RuntimeWarning("Use 'instance()'")

    @classmethod
    def instance(klass):
        if klass._instance is None:
            klass._instance = Pico()
        return klass._instance

    def to_s(self) -> str:
        """echo"""

