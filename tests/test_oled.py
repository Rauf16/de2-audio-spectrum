# test_oled.py – test OLED SH1106: Rezim 1 Spektrum s testovacimi daty
from machine import I2C, Pin
from sh1106 import SH1106_I2C
import time
import random

# --- Nastaveni ---
BANDS = ["63", "125", "250", "500", "1k", "2k", "4k", "8k"]  # pasma v Hz
DB_MIN = -40      # nejtissi zobrazena uroven (prazdny sloupec)
DB_MAX = 0        # nejhlasitejsi uroven (plny sloupec)
BAR_X = 76        # kde na displeji zacina sloupec (px)
BAR_W = 128 - BAR_X   # maximalni delka sloupce = 52 px


def draw_spectrum(oled, levels):
    """Nakresli 8 radku: frekvence, uroven v dB a sloupec."""
    oled.fill(0)
    for i in range(8):
        y = i * 8                      # kazdy radek je 8 px vysoky
        db = levels[i]
        # text, napr. "125 -12dB"
        oled.text(f"{BANDS[i]:>3} {db:>3}dB", 0, y)
        # delka sloupce podle dB
        length = (db - DB_MIN) * BAR_W // (DB_MAX - DB_MIN)
        oled.fill_rect(BAR_X, y + 1, length, 6, 1)
    oled.show()


def fake_levels(levels):
    """Testovaci data: kazde pasmo se nahodne trochu zmeni."""
    for i in range(8):
        levels[i] += random.randint(-3, 3)
        levels[i] = max(DB_MIN, min(DB_MAX, levels[i]))   # omezit rozsah
    return levels


def main():
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400_000)

    if 0x3C not in i2c.scan():
        print("OLED nenalezen - zkontroluj zapojeni SDA/SCL/3V3/GND")
        return

    oled = SH1106_I2C(i2c)
    levels = [-30, -25, -20, -15, -20, -25, -30, -35]   # startovni hodnoty

    print("Test OLED bezi, Ctrl+C = konec")
    try:
        while True:
            draw_spectrum(oled, fake_levels(levels))
            time.sleep(0.1)
    except KeyboardInterrupt:
        oled.fill(0)
        oled.show()
        oled.poweroff()
        print("Konec testu.")


if __name__ == "__main__":
    main()
