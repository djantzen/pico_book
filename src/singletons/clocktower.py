"""
The ClockTower is the single source of truth for time in the system. This enhances testability by allowing
test suites to set values for current time and sleep durations
"""
import _thread
import utime


class ClockTower:

    _instance = None
    _now = None

    def __init__(self):
        self.sleep_duration = None
        self.not_yets = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ClockTower()

        return cls._instance

    @property
    def now(self):
        return utime.time() if self._now is None else self._now

    @now.setter
    def now(self, now):
        self._now = now

    def set_sleep_duration(self, duration_in_seconds):
        self.sleep_duration = duration_in_seconds

    def sleep(self, duration_in_seconds):
        if self.sleep_duration is None:
            utime.sleep(duration_in_seconds)
        else:
            utime.sleep(self.sleep_duration)

    def not_yet(self, duration_in_seconds):
        calling_thread = _thread.get_ident()
        if calling_thread not in self.not_yets:
            self.not_yets[calling_thread] = self.now
            return True
        else:
            if self.now >= self.not_yets[calling_thread] + duration_in_seconds:
                del(self.not_yets[calling_thread])
                return False
            else:
                return True
