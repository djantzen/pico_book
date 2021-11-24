import utime


class ClockTower:

    _instance = None
    _now = None

    def __init__(self):
        ...
#        raise RuntimeWarning("Call 'instance'()")

    @classmethod
    def instance(klass):
        if klass._instance is None:
            klass._instance = ClockTower()

        return klass._instance

    def now(self):
        return utime.time() if self._now is None else self._now

    def set_now(self, now):
        self._now = now
