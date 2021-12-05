import machine


class Pico:
    _instance = None

    gp0 = machine.Pin(0)
    gp1 = machine.Pin(1)
    gp2 = machine.Pin(2)
    gp3 = machine.Pin(3)
    gp4 = machine.Pin(4)
    gp5 = machine.Pin(5)
    gp6 = machine.Pin(6)
    gp7 = machine.Pin(7)
    gp8 = machine.Pin(8)
    gp9 = machine.Pin(9)
    gp10 = machine.Pin(10)
    gp11 = machine.Pin(11)
    gp12 = machine.Pin(12)
    gp13 = machine.Pin(13)
    gp14 = machine.Pin(14)
    gp15 = machine.Pin(15)
    gp16 = machine.Pin(16)
    gp17 = machine.Pin(17)
    gp18 = machine.Pin(18)
    gp19 = machine.Pin(19)
    gp20 = machine.Pin(20)
    gp21 = machine.Pin(21)
    gp22 = machine.Pin(22)
    gp25 = machine.Pin(25)
    gp26 = machine.Pin(26)
    gp27 = machine.Pin(27)
    gp28 = machine.Pin(28)

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

