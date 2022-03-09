import utime


class ClockTower:

    _instance = None
    _now = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ClockTower()

        return cls._instance

    def now(self):
        return utime.time() if self._now is None else self._now

    def set_now(self, now):
        self._now = now
