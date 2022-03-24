import utime
from models import TrafficLight

start_time_in_sec = utime.time()

traffic_light = TrafficLight()
traffic_light.start()

while utime.time() < start_time_in_sec + 60:
    traffic_light.cycle()

traffic_light.stop()
