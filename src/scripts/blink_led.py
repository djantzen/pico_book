import components
import singletons

runtime = int(input("Run for how many seconds?"))

pico = singletons.Pico.instance()
blinker = components.Blinker(pico.reserve_pin(pico.gp25), 0.5)

while singletons.ClockTower.instance().not_yet(runtime):
    blinker.blink()
