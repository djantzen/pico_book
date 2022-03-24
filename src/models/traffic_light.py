import _thread
import components
import singletons


class TrafficLight:

    def __init__(self):
        pico = singletons.Pico.instance()
        self.red_light = components.Blinker(pico.reserve_pin(pico.gp15, "Red light"), 3, 0)
        self.yellow_light = components.Blinker(pico.reserve_pin(pico.gp14, "Yellow light"), 1, 0)
        self.green_light = components.Blinker(pico.reserve_pin(pico.gp13, "Green light"), 3, 0)
        self.button_pressed = False
        self.button = components.Button(pico.gp16)
        self.buzzer = components.Buzzer(pico.gp12)
        self.is_running = False

    def watch_button(self):
        while self.is_running:
            if self.button.is_pressed():
                self.button_pressed = True
            # without this sleep, the thread will lock up one of the two Pico cores and not let go until reboot
            singletons.ClockTower.instance().sleep(.01)
        return

    def start(self):
        self.is_running = True
        _thread.start_new_thread(self.watch_button, ())

    def stop(self):
        self.is_running = False

    def cycle(self):
        if self.button_pressed:
            self.red_light.on()
            self.buzzer.buzz()
            self.red_light.off()
            self.button_pressed = False
        self.green_light.blink()
        self.yellow_light.blink()
        self.red_light.blink()
