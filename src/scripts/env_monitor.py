from models import EnvMonitor
from singletons import ClockTower
import uasyncio

er = EnvMonitor()
er.initialize()
#runtime = int(input("Run for how many seconds?"))


readings = []
readings_lock = uasyncio.Lock()
wifi_lock = uasyncio.Lock()


async def take_reading_task():
    print("starting reading task")
    while True:
        try:
            r = er.take_reading()
            async with readings_lock:
                readings.append(r)
            await uasyncio.sleep(60)
        except RuntimeError as re:
            print("Caught error: {}".format(re))


async def listen_task():
    print("starting listening task")
    while True:
        async with wifi_lock:
            er.get_command(timeout_ms=55000)
        await uasyncio.sleep(5)


async def post_reading_task():
    print("starting posting task")
    while True:
        async with readings_lock:
            async with wifi_lock:
                for r in readings:
                    er.record(r)
            readings.clear()
        await uasyncio.sleep(60)


async def main():
    loop = uasyncio.get_event_loop()
    rt = loop.create_task(take_reading_task())
    prt = loop.create_task(post_reading_task())
    lt = loop.create_task(listen_task())
    await uasyncio.gather(rt, prt, lt)
    # await uasyncio.sleep(10)

#     while ClockTower.instance().not_yet(runtime):
#         try:
#             reading = er.take_reading()
#             er.record(reading)
#             print("Sleeping")
# #            await uasyncio.sleep(60)
#             ClockTower.instance().sleep(60)
#         except RuntimeError as re:
#             print("Caught error: {}".format(re))
#             er.wifi.reset()


uasyncio.run(main())
