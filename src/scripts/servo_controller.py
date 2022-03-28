import utime

import singletons
from models import ServoController


def main():
    runtime = int(input("Run for how many seconds?"))

    controller = ServoController()

    while singletons.ClockTower.instance().not_yet(runtime):
        controller.adjust()
        utime.sleep(0.5)


main()
