import components
import singletons

pico = singletons.Pico.instance()
sensor = components.PirSensor(pico.gp28)


def handler():
    if sensor.movement():
        print("Motion!")


sensor.handle_interrupt(handler=handler)
