import singletons
import components
import random
import utime

pico = singletons.Pico.instance()
servo = components.Servo(pico.pwm_7b_gp15)

for i in range(10):
    r = random.randrange(-90, 90)
    print(r)
    servo.set_position(r)
    utime.sleep(3)
