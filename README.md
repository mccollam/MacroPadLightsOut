# MacroPadLightsOut

A game of Lights Out on the [Adafruit MacroPad](https://www.adafruit.com/product/5128)

## To install:
Grab the [CircuitPython libraries](https://circuitpython.org/libraries) for your version of CircuitPython.

You'll need to put the following in the `/lib` folder on the MacroPad:
 * `adafruit_display_text/`
 * `adafruit_hid/`
 * `adafruit_midi/`
 * `adafruit_debouncer.mpy`
 * `adafruit_macropad.mpy`
 * `adafruit_simple_text_display.mpy`
 * `neopixel.mpy`

Copy `code.py` and `patterns.py` to the root folder on the MacroPad.

## To play:

Use the rotary encoder to select a level.

Push a button to toggle the light on that button and on the buttons to the
left, right, above, and below.

To win, turn all the lights off.

## To add new levels:

Add sets of lists to `patterns.py`.  1 is on, 0 is off.
