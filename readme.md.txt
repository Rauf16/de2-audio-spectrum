# Audio spectrum analyzer

DE2 team project – Raspberry Pi Pico W, MicroPython.

## Goal
Sample audio from a microphone, split it into frequency bands
and show a live spectrum on a display and a NeoPixel strip.

## Hardware
- Raspberry Pi Pico W
- Microphone module 
- display
- NeoPixel strip (LED strip)

## Team
| Name | Part |
| --- | --- |
| Rauf Iusupov | hardware, wiring, leds.py |
| … | mic.py |
| … | spectrum.py |
| … | display.py |

## Planned files
- `main.py` – main loop
- `config.py` – pins and settings
- `mic.py` – ADC sampling
- `spectrum.py` – FFT and frequency bands
- `display.py` – bars on the display
- `leds.py` – NeoPixel output