## Projektbeschreibung
Dieses Projekt implementiert ein Tic-Tac-Toe-Spiel, das auf einem Raspberry Pi läuft und ein Keypad sowie ein LCD-Display zur Benutzerinteraktion verwendet. Zusätzlich wird ein NeoPixel-LED-Board zur Anzeige des Spielbretts verwendet.

## TicTacToe
Die TicTacToe-Klasse verwaltet den Spielablauf, stellt Fragen und zeigt das Ergebnis auf dem LCD-Display und dem LED-Board an.

## GameBoard
Die GameBoard-Klasse steuert die NeoPixel-LEDs und zeigt den Spielstatus an. Es zeigt auch an, wenn ein Spieler gewinnt.

## Voraussetzungen
- Python 3
- Raspberry Pi 3
- Bibliotheken: 'RPi.GPIO', 'RPLCD', 'neopixel', 'board', 'json'

## Installation
1. Klone das Repository:

   git clone <https://github.com/Data-Science-1362/Tic-Tac-Toe.git>
3. Installiere die benötigten Bibliotheken:
   
    pip install RPi.GPIO RPLCD neopixel

## Verwendung

### TicTacToe
1. Lade die Fragen aus der JSON-Datei fragen.json.
2. Starte das Spiel:
   
   python tic-tac-toe.py

### GameBoard
Das GameBoard wird automatisch von der TicTacToe-Klasse verwendet, um den Spielstatus anzuzeigen.

### Pinbelegung
Die Pinbelegung für das Tic-Tac-Toe-Spiel ist wie folgt:

#### Keypad:
Reihen: Pin 7 (BCM 4), Pin 8 (BCM 14), Pin 11 (BCM 17), Pin 25 (BCM 26)

Spalten: Pin 24 (BCM 8), Pin 10 (BCM 15), Pin 9 (BCM 21), Pin 12 (BCM 18)

#### LCD-Display:
I2C-Schnittstelle:
   SDA: Pin 3 (BCM 2)
   SCL: Pin 5 (BCM 3)

#### LED-Board (NeoPixel): 
   Pin 12 (BCM 18)

Diese Pinbelegung sollte auf einem Raspberry Pi verwendet werden. Die BCM-Nummern beziehen sich auf das Broadcom-Nummerierungssystem für die GPIO-Pins.

### Quellen
Diese Quellen wurden für den Code benutzt:
- https://medium.com/@thedyslexiccoder/how-to-set-up-a-raspberry-pi-4-with-lcd-display-using-i2c-backpack-189a0760ae15
- https://www.az-delivery.de/en/blogs/azdelivery-blog-fur-arduino-und-raspberry-pi/raspberry-pi-und-lcd1602-bzw-lcd2004
- https://gpiozero.readthedocs.io/en/stable/recipes.html
- https://www.digikey.com/en/maker/tutorials/2021/how-to-connect-a-keypad-to-a-raspberry-pi
- https://tutorials-raspberrypi.de/raspberry-pi-openhab-2-ws2801-ws2812-rgb-led-streifen-steuern/
- https://www.az-delivery.de/en/products/u-64-led-panel
