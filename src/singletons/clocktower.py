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

    def not_yet(self, duration_in_seconds, caller: str = "global"):
        calling_thread = _thread.get_ident()
        caller_id = str(calling_thread) + ':' + caller
        if calling_thread not in self.not_yets:
            self.not_yets[caller_id] = self.now
            return True
        else:
            if self.now >= self.not_yets[caller_id] + duration_in_seconds:
                del(self.not_yets[caller_id])
                return False
            else:
                return True
