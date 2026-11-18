# test_mode2.py – Rezim 2 Hlasitost: RMS, peak, CLIP (testovaci signal)
from machine import I2C, Pin, SPI
from sh1106 import SH1106_I2C
import math
import time

USE_MATRIX = False   # True = kreslit i na LED matici MAX7219

N = 256              # pocet vzorku v jednom bloku
MID = 32768          # stred ADC (klidove napeti 1,65 V)
FULL = 32768         # plny rozsah = 0 dBFS
DB_MIN = -48         # nejtissi zobrazena uroven
CLIP_LIMIT = 65000   # vzorek nad 65000 nebo pod 535 = CLIP


# ---------- Vypocet hlasitosti ----------
def measure(samples):
    """Vrati (rms_db, peak_db, clip) pro blok vzorku 0-65535."""
    total = 0
    peak = 0
    clip = False
    for s in samples:
        x = s - MID                    # odecist stred -> signal kolem nuly
        total += x * x
        if abs(x) > peak:
            peak = abs(x)
        if s >= CLIP_LIMIT or s <= 65535 - CLIP_LIMIT:
            clip = True
    rms = math.sqrt(total / len(samples))
    rms_db = 20 * math.log10(max(rms, 1) / FULL)
    peak_db = 20 * math.log10(max(peak, 1) / FULL)
    return rms_db, peak_db, clip


# ---------- Testovaci signal (pozdeji nahradi ADC) ----------
def fake_samples(amp):
    """Sinusovka s amplitudou amp (1.0 = plny rozsah)."""
    out = []
    for k in range(N):
        s = int(MID + amp * 32767 * math.sin(2 * math.pi * k / 32))
        out.append(max(0, min(65535, s)))   # orez jako skutecny ADC
    return out


# ---------- OLED ----------
def draw_oled(oled, rms_db, peak_db, clip, blink):
    oled.fill(0)
    oled.text("Hlasitost", 0, 0)
    oled.text(f"RMS :{rms_db:6.1f} dBFS", 0, 16)
    oled.text(f"Peak:{peak_db:6.1f} dBFS", 0, 28)
    # sloupec RMS pres celou sirku
    length = int((max(rms_db, DB_MIN) - DB_MIN) * 128 / -DB_MIN)
    oled.rect(0, 40, 128, 8, 1)
    oled.fill_rect(0, 40, min(length, 128), 8, 1)
    # blikajici varovani CLIP
    if clip and blink:
        oled.fill_rect(40, 52, 48, 12, 1)
        oled.text("CLIP", 48, 54, 0)    # cerny text na bilem
    oled.show()


# ---------- LED matice MAX7219 ----------
if USE_MATRIX:
    spi = SPI(0, baudrate=1_000_000, sck=Pin(18), mosi=Pin(19))
    cs = Pin(17, Pin.OUT, value=1)


def mx_write(register, value):
    cs.value(0)
    spi.write(bytes([register, value]))
    cs.value(1)


def mx_init():
    for reg, val in ((0x0F, 0), (0x09, 0), (0x0B, 7), (0x0A, 2), (0x0C, 1)):
        mx_write(reg, val)


def draw_matrix(rms_db, clip, blink):
    """VU metr pres celou matici, pri CLIP blika horni radek."""
    h = int((max(rms_db, DB_MIN) - DB_MIN) * 8 / -DB_MIN)   # 0-8 radku
    for row in range(8):
        value = 0xFF if row < h else 0x00
        if row == 7 and clip:
            value = 0xFF if blink else 0x00
        mx_write(row + 1, value)


# ---------- Hlavni program ----------
def main():
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400_000)
    oled = SH1106_I2C(i2c)
    if USE_MATRIX:
        mx_init()

    amp = 0.01
    blink = False
    print("Test Rezimu 2 bezi, Ctrl+C = konec")
    try:
        while True:
            samples = fake_samples(amp)
            rms_db, peak_db, clip = measure(samples)
            blink = not blink
            draw_oled(oled, rms_db, peak_db, clip, blink)
            if USE_MATRIX:
                draw_matrix(rms_db, clip, blink)
            amp *= 1.1                  # signal pomalu sili
            if amp > 1.3:
                amp = 0.01              # a znovu od zacatku
            time.sleep(0.15)
    except KeyboardInterrupt:
        oled.fill(0)
        oled.show()
        if USE_MATRIX:
            for row in range(1, 9):
                mx_write(row, 0)
        print("Konec testu.")


if __name__ == "__main__":
    main()