# Audio spectrum analyzer

DE2 team project – Raspberry Pi Pico W, MicroPython.

## Goal

A pocket-size, real-time audio analyzer built on a Raspberry Pi Pico W.
Plug in a phone or PC through a 3.5 mm jack and the device instantly shows
what the sound is made of: which frequencies it contains, how loud it is,
and which musical note is playing.

### What the project demonstrates
- **Analog design:** summing L+R channels, DC bias to 1.65 V and an
  anti-aliasing low-pass filter, so a line-level signal can be safely
  measured by the 3.3 V ADC.
- **Fast sampling:** ADC at 40 kHz with DMA into a double buffer.
- **Digital signal processing on a microcontroller:** windowing, FFT,
  band levels in dB, RMS/peak measurement and pitch detection.
- **Dual-core design:** core 0 processes the audio, core 1 drives the
  displays and the button, so the picture stays smooth.
- **Two outputs:** a detailed view on the OLED (I2C) and a colourful
  overview on the 8×8 RGB LED matrix (WS2812B).
- **Simple control:** three modes switched with a single button.

## Modes

**Mode 1 – Spectrum.** Shows the distribution of sound in 8 frequency bands
(63, 125, 250, 500 Hz, 1, 2, 4, 8 kHz).
- Display: level of each band in dB and its frequency
- Matrix: 8 colour columns (green → yellow → red) with peak hold

**Mode 2 – Loudness.** Measures the signal level in dBFS.
- Display: RMS, sample peak, CLIP warning
- Matrix: full-width VU meter, the top row blinks red on clipping

**Mode 3 – Tuner.** Detects the dominant frequency.
- Display: note (e.g. A), frequency in Hz, deviation in cents,
  arrow left or right towards the nearest note
- Matrix: green = in tune (±5 cents), red = out of tune

**Controls:** short button press = next mode, long press = reset maximum and peak hold.

## Hardware
- Raspberry Pi Pico W
<img width="400" height="400" alt="Raspberry Pi Pico W" src="https://github.com/user-attachments/assets/883dc884-b437-44a1-a93d-39bec083df4f" />

- 3.5 mm jack input (terminal block adapter)
<img width="300" height="300" alt="3.5 mm jack adapter" src="https://github.com/user-attachments/assets/e299277f-993a-43c2-a2d3-b405b7eb8120" />

- RGB LED matrix 8×8 NeoPixel WS2812B
<img width="310" height="310" alt="RGB LED matrix WS2812B" src="https://github.com/user-attachments/assets/c2abd4b4-54a5-4cb0-95b8-2cf05734dea7" />

- OLED display SH1106 128×64, I2C

### Bill of materials

| Part | Qty | Status |
| --- | --- | --- |
| Raspberry Pi Pico W + DFRobot Pico Gravity Board | 1 | have |
| OLED display SH1106 128×64, I2C | 1 | have |
| Breadboard, jumper wires, USB cable | – | have |
| AUX cable 3.5 mm jack–jack | 1 | have |
| RGB LED matrix 8×8 WS2812B | 1 | to get |
| 3.5 mm jack to terminal block adapter | 1 | to get |
| Push button | 1 | to get |
| Resistor 10 kΩ | 2 | to get |
| Resistor 100 kΩ | 2 | to get |
| Resistor 1 kΩ | 1 | to get |
| Resistor 330 Ω | 1 | to get |
| Capacitor 1 µF | 1 | to get |
| Capacitor 10 nF | 1 | to get |
| Capacitor 1000 µF / 10 V | 1 | to get |
| Level shifter 74AHCT125 (optional) | 1 | only if the matrix does not respond reliably |

## Block diagram
```mermaid
flowchart TB
  SRC[Zdroj zvuku<br/>mobil / PC]

  subgraph AFE[Analogový vstup]
    direction LR
    MIX[Součet L+R<br/>2× 10k] --> CAP[Oddělovací C<br/>1 µF] --> BIAS[Posun na 1,65 V<br/>dělič 2× 100k] --> LPF[Dolní propust<br/>~16 kHz]
  end

  subgraph PICO[Raspberry Pi Pico W]
    direction LR
    ADC[ADC0 GP26<br/>40 kHz] -->|DMA| BUF[Dvojitý buffer<br/>2× 1024 vzorků] --> C0[Jádro 0<br/>okno + FFT<br/>32 + 8 pásem] -->|úrovně pásem| C1[Jádro 1<br/>zobrazení + ovládání]
  end

  BTN[Tlačítko GP14]
  PWR[USB 5 V]
  OLED[OLED SH1106<br/>128×64 px<br/>detailní spektrum]
  RGB[RGB matice 8×8<br/>WS2812B<br/>8 pásem]
  PC[PC<br/>Python záznam]

  SRC -->|3,5mm jack L+R| AFE
  AFE -->|0–3,3 V| PICO
  BTN --> PICO
  PWR --> PICO
  PICO -->|I2C0 SDA/SCL| OLED
  PICO -->|PIO GP15<br/>přes 330 Ω| RGB
  PICO <-->|USB serial| PC
  PWR -->|VBUS 5 V<br/>+ 1000 µF| RGB
```
test
<img width="1465" height="227" alt="image" src="https://github.com/user-attachments/assets/a57818a9-c733-43f8-913f-6cf92eae279c" />



## Pinout

Board: Raspberry Pi Pico W on DFRobot Pico Gravity Board.

| Device | Device pin | Pico W GPIO | Physical pin | Gravity Board header |
| --- | --- | --- | --- | --- |
| OLED SH1106 | VCC | 3V3(OUT) | 36 | I2C0 – 3V3 |
| OLED SH1106 | GND | GND | 38 | I2C0 – GND |
| OLED SH1106 | SDA | GP4 (I2C0 SDA) | 6 | I2C0 – D/4 |
| OLED SH1106 | SCK | GP5 (I2C0 SCL) | 7 | I2C0 – C/5 |
| RGB matrix WS2812B | DIN | GP15, via 330 Ω | 20 | Digital – GP15 |
| RGB matrix WS2812B | 5V | VBUS (5 V), 1000 µF to GND | 40 | VBUS (center header) |
| RGB matrix WS2812B | GND | GND | 38 | Digital – GND |
| Analog front-end | output | GP26 (ADC0) | 31 | Analog – A/26 |
| Analog front-end | supply | 3V3(OUT) | 36 | Analog – 3V3 |
| Button | signal | GP14 | 19 | Digital – GP14 |

## Software and libraries

| Item | Version / source | Used for |
| --- | --- | --- |
| MicroPython firmware | v1.29.0 (2026-08-24), RPI_PICO_W, micropython.org | runtime |
| `machine` (Pin, I2C, ADC) | built-in | hardware access |
| `neopixel` | built-in | RGB LED matrix |
| `math`, `time`, `random` | built-in | calculations, timing, test data |
| `sh1106.py` | driver supplied in DE2 Lab 6 | OLED display |
| `ulab` | planned, only if pure-Python FFT is too slow | FFT |
| Thonny | x.x (fill in) | IDE |

## Repository structure (planned)

```
main.py           main loop, mode switching
config.py         pins and settings
audio_input.py    ADC sampling
spectrum.py       FFT and frequency bands (Mode 1)
loudness.py       RMS, peak, clipping (Mode 2)
tuner.py          dominant frequency, note, cents (Mode 3)
display.py        OLED output
matrix.py         RGB LED matrix output
lib/sh1106.py     OLED driver
tests/            component tests
```

## Classes / API (draft)

### `AudioInput` – audio_input.py
- `AudioInput(pin=26, n=256)` – ADC input on GP26
- `read_block()` → list of n samples (0–65535)

### `Spectrum` – spectrum.py
- `bands(samples)` → 8 levels in dB (63 Hz, 125 Hz … 8 kHz)

### `Loudness` – loudness.py
- `measure(samples)` → (rms_dbfs, peak_dbfs, clip)

### `Tuner` – tuner.py
- `detect(samples)` → (note, freq_hz, cents)

### `OledView` – display.py
- `show_spectrum(levels)` – Mode 1
- `show_loudness(rms, peak, clip)` – Mode 2
- `show_tuner(note, freq_hz, cents)` – Mode 3

### `Matrix` – matrix.py
- `bars(heights, peaks)` – 8 columns, height 0–8, green → yellow → red, peak hold dots
- `vu(level, clip)` – full-width VU meter, top row blinks red on clip
- `tuned(ok)` – whole matrix green (in tune) or red (out of tune)
- `clear()`

### Button – GP14
- short press = next mode (Spectrum → Loudness → Tuner)
- long press = reset maximum and peak hold

## Component tests

| Component | Interface / pins | Test file | Status |
| --- | --- | --- | --- |
| OLED SH1106 128×64 – Mode 1 layout (spectrum) | I2C0, GP4/GP5 | `tests/test_oled.py` | works |
| OLED SH1106 128×64 – Mode 2 layout (loudness) | I2C0, GP4/GP5 | `tests/test_mode2.py` | works |
| RGB LED matrix 8×8 WS2812B | GP15 | `tests/test_matrix.py` | not tested yet |
| Audio input (jack + analog front-end) | ADC0, GP26 | `tests/test_adc.py` | not tested yet |
| Button (mode select) | GPIO, GP14 | `tests/test_button.py` | not tested yet |

Tests for Modes 1 and 2 use generated test data, not real audio yet.

## Team

| Name | Part |
| --- | --- |
| Rauf Iusupov | … |
| Marek Malina | … |
| Jaroslav Kapaňa | … |

## Open questions
- Is an amplifier needed? Not for now, decide after testing the audio input.
- Is the 74AHCT125 level shifter needed? Only if the matrix does not respond reliably with 3.3 V data.
- OLED in Mode 1: 8 bands (as in the mode description) or detailed 32-band spectrum (as in the block diagram)?
