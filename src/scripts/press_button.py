import singletons
import components

clocktower = singletons.ClockTower.instance()
button = components.Button()
blinker = components.Blinker()

start_time_in_sec = clocktower.now()

while clocktower.now() < start_time_in_sec + 60:
    if button.is_pressed():
        print("Button press")
        blinker.blink()
