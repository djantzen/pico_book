from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
import utime
import singletons

runtime = int(input("Run for how many seconds?"))

@asm_pio(set_init=PIO.OUT_LOW)
def led_quarter_brightness():
    set(pins, 0)[2]
    set(pins, 1)

@asm_pio(set_init=PIO.OUT_LOW)
def led_half_brightness():
    set(pins, 0)
    set(pins, 1)

@asm_pio(set_init=PIO.OUT_HIGH)
def led_full_brightness():
    set(pins, 1)


sm1 = StateMachine(1, led_quarter_brightness, freq=10000, set_base=Pin(25))
sm2 = StateMachine(2, led_half_brightness, freq=10000, set_base=Pin(25))
sm3 = StateMachine(3, led_full_brightness, freq=10000, set_base=Pin(25))


while singletons.ClockTower.instance().not_yet(runtime):
    sm1.active(1)
    utime.sleep(1)
    sm1.active(0)

    sm2.active(1)
    utime.sleep(1)
    sm2.active(0)

    sm3.active(1)
    utime.sleep(1)
    sm3.active(0)
