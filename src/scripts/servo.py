import singletons
import components
import random

runtime = int(input("Run for how many seconds?"))
clocktower = singletons.ClockTower.instance()
pico = singletons.Pico.instance()
servo = components.Servo(pico.pwm("7B"))

while clocktower.not_yet(runtime):
    r = random.randrange(-90, 90)
    print(r)
    servo.set_position(r)
    clocktower.sleep(3)
