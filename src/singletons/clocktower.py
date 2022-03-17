import utime


class ClockTower:

    _instance = None
    _now = None

    def __init__(self):
        self.sleep_duration = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ClockTower()

        return cls._instance

    def now(self):
        return utime.time() if self._now is None else self._now

    def set_now(self, now):
        self._now = now

    def set_sleep_duration(self, duration_in_seconds):
        self.sleep_duration = duration_in_seconds

    def sleep(self, duration_in_seconds):
        if self.sleep_duration is None:
            utime.sleep(duration_in_seconds)
        else:
            utime.sleep(self.sleep_duration)
