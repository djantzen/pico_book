import _thread
import utime

runtime = int(input("Run for how many seconds?"))
delay = float(input("Delay in seconds for thread loop?"))
start_time = utime.time()
stop_time = start_time + runtime
print("Start time is ", start_time)
print("Stop time is ", stop_time)
print("Delay is ", delay)


def some_thread():
    print("starting thread")
    while utime.time() < stop_time:
        utime.sleep(delay)
    print("exiting")
    return


_thread.start_new_thread(some_thread, ())

while utime.time() < stop_time:
    print("Main loop running")
    utime.sleep(1)
