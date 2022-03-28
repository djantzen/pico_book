## Pico Book ##

Implementations of the exercises in [Get Started with MicroPython on Raspberry Pi Pico](https://www.adafruit.com/product/4898)

**Design goals**

* Modular code
* Minimize thinking about pins and other physical minutiae, allow mental focus on behavior
* Support automated unit and functional tests
* Minimize on-device QA

To achieve these goals, the code is broken out into `components`, `singletons`, `models` and `scripts`
A component is a physical device wired to the Pico using one or more pins. A model is a collection of components that interact. 
The primary singleton is the Pico class, which represents the microcontroller configuration i.e., allocation of pins. 
Scripts tie different components, models and singletons together into an executable.

**Dependencies**

* Micropython 1.17 or greater
* [UnitTest](https://pypi.org/project/micropython-unittest/)
  * Install with `micropython -m upip install unittest`

**Hardware Used**

* [Towerpro MG92 Microservo](https://www.adafruit.com/product/2307)
* [LEDs](https://www.adafruit.com/product/4203)
* [PS1240 Piezo Buzzer](https://www.adafruit.com/product/160)
* [Potentiometer](https://www.adafruit.com/product/4133)
* [TinSharp TC1602A LCD](https://www.adafruit.com/product/181)
* [PIR Sensor](https://www.adafruit.com/product/4666)

**Functional Testing**

To prove correct functioning of components and models, we can write functional tests that
observe the states of IO channels. This is possible by providing mock implementations
of `machine` classes for `Pin`, `PWM`, and `ADC`

**Running Tests**

`micropython run_tests.py`

**Running Scripts**

Within a micropython interactive session `exec(open('scripts/the_script.py').read())`