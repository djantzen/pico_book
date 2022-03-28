import singletons
from models import TrafficLight

runtime = int(input("Run for how many seconds?"))

traffic_light = TrafficLight()
traffic_light.start()

while singletons.ClockTower.instance().not_yet(runtime):
    traffic_light.cycle()

traffic_light.stop()
