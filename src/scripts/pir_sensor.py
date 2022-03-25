import components
import singletons

pico = singletons.Pico.instance()
sensor = components.PirSensor(pico.gp28)


def handler():
    print("Motion!")


sensor.on_movement(handler=handler)
