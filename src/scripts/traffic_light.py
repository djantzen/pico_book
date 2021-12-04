import machine
import _thread
import utime
import singletons
import components

global clock_tower
global button
global button_pressed
global join_now


join_now = False
clock_tower = singletons.ClockTower.instance()
pico = singletons.Pico.instance()
red_light = components.Blinker(pico.gp15, 3, 0)
yellow_light = components.Blinker(pico.gp14, 1, 0)
green_light = components.Blinker(pico.gp13, 3, 0)
button_pressed = False
button = components.Button(pico.gp16)
buzzer = components.Buzzer(pico.gp12)
start_time_in_sec = clock_tower.now()


def button_reader_thread():
    global button
    global button_pressed
    global clock_tower
    global join_now
#    while clock_tower.now() < start_time_in_sec + 59:
    while not join_now:
        if button.is_pressed():
            # print("press ")
            button_pressed = True
        utime.sleep(.01)
    print("exiting")
    return


_thread.start_new_thread(button_reader_thread, ())

while clock_tower.now() < start_time_in_sec + 60:
    if button_pressed:
        red_light.on()
        buzzer.buzz()
        button_pressed = False
        red_light.off()
    green_light.blink()
    yellow_light.blink()
    red_light.blink()

join_now = True
