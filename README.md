# Audio spectrum analyzer

DE2 team project – Raspberry Pi Pico W, MicroPython.

## Goal
Sample audio from a microphone, split it into frequency bands
and show a live spectrum on a display and a NeoPixel strip.

## Hardware
- Raspberry Pi Pico W
<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/883dc884-b437-44a1-a93d-39bec083df4f" />

- Microphone module 
- display
- NeoPixel strip (LED strip)

## Block diagram
```mermaid
flowchart LR
  SRC[Zdroj zvuku<br/>mobil / PC] -->|3,5mm jack L+R| MIX
  subgraph AFE[Analogový vstup]
    MIX[Součet L+R<br/>2× 10k] --> CAP[Oddělovací C<br/>1 µF] --> BIAS[Posun na 1,65 V<br/>dělič 2× 100k] --> AMP[Zesilovač<br/>MCP6002] --> LPF[Dolní propust<br/>~16 kHz]
  end
  LPF -->|0–3,3 V| ADC
  subgraph PICO[Raspberry Pi Pico]
    ADC[ADC0 GP26<br/>40 kHz] -->|DMA| BUF[Dvojitý buffer<br/>2× 1024 vzorků]
    BUF --> C0[Jádro 0<br/>okno + FFT + 16 pásem]
    C0 -->|úrovně pásem| C1[Jádro 1<br/>zobrazení + ovládání]
  end
  C1 -->|SPI0 GP17–21| LCD[Nokia 5110<br/>84×48 px]
  C1 -->|PIO GP15| LED[NeoPixel<br/>WS2812B]
  BTN[Tlačítko GP14] --> C1
  C1 <-->|USB serial| PC[PC<br/>Python záznam]
  PWR[USB 5 V] --> PICO
  PWR --> LED
```

## Team
| Name | Part |
| --- | --- |
| Rauf Iusupov | ... |
| Marek Malina | ... |
| Jaroslav Kapaňa | ... |

## Planned files
- `main.py` – main loop
- `config.py` – pins and settings
- `mic.py` – ADC sampling
- `spectrum.py` – FFT and frequency bands
- `display.py` – bars on the display
- `leds.py` – NeoPixel output
