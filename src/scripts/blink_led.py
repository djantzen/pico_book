import components
import singletons

pico = singletons.Pico.instance()
blinker = components.Blinker(pico.gp19, 0.5)

for i in range(10):
    blinker.blink()
