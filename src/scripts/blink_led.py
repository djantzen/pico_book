import components
import singletons

pico = singletons.Pico.instance()
blinker = components.Blinker(pico.reserve_pin(pico.gp25), 0.5)

for i in range(6):
    blinker.blink()
