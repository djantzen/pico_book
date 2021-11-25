import singletons
import components

clock_tower = singletons.ClockTower.instance()
pico = singletons.Pico.instance()
button = components.Button(pico.gp10)
blinker = components.Blinker(pico.gp19)

start_time_in_sec = clock_tower.now()

while clock_tower.now() < start_time_in_sec + 60:
    if button.is_pressed():
        print("Button press")
        blinker.blink()
