import utime
from models import ServoController


def main():

    controller = ServoController()

    while True:
        controller.adjust()
        utime.sleep(0.5)


main()
