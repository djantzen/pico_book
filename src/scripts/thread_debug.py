import _thread
import singletons


runtime = int(input("Run for how many seconds?"))
delay = float(input("Delay in seconds for thread loop?"))
clocktower = singletons.ClockTower.instance()


def some_thread():
    print("starting child thread with id {}".format(_thread.get_ident()))
    while clocktower.not_yet(runtime):
        clocktower.sleep(delay)
    print("exiting")
    return


_thread.start_new_thread(some_thread, ())

while clocktower.not_yet(runtime):
    print("Main loop running with id {}".format(_thread.get_ident()))
    clocktower.sleep(1)
