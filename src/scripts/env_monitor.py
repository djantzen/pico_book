from models import EnvMonitor
from singletons import ClockTower

er = EnvMonitor()
er.initialize()
runtime = int(input("Run for how many seconds?"))

while ClockTower.instance().not_yet(runtime):
    try:
        reading = er.take_reading()
        er.record(reading)
        ClockTower.instance().sleep(60)
    except RuntimeError:
        print("Caught error")
        er.wifi.reset()

