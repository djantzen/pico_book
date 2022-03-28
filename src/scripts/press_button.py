import singletons
import components

runtime = int(input("Run for how many seconds?"))
clock_tower = singletons.ClockTower.instance()
pico = singletons.Pico.instance()
button = components.Button(pico.gp10)
blinker = components.Blinker(pico.gp25)


while singletons.ClockTower.instance().not_yet(runtime):
    if button.is_pressed():
        print("Button press")
        blinker.blink()
