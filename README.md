## Projektbeschreibung
Dieses Projekt implementiert ein Tic-Tac-Toe-Spiel, das auf einem Raspberry Pi läuft und ein Keypad sowie ein LCD-Display zur Benutzerinteraktion verwendet. Zusätzlich wird ein NeoPixel-LED-Board zur Anzeige des Spielbretts verwendet.

## TicTacToe
Die TicTacToe-Klasse verwaltet den Spielablauf, stellt Fragen und zeigt das Ergebnis auf dem LCD-Display und dem LED-Board an.

## GameBoard
Die GameBoard-Klasse steuert die NeoPixel-LEDs und zeigt den Spielstatus an. Es zeigt auch an, wenn ein Spieler gewinnt.

## Voraussetzungen
- Python 3
- Raspberry Pi mit Raspbian OS
- Bibliotheken: 'RPi.GPIO', 'RPLCD', 'neopixel', 'board', 'json'

## Installation
1. Klone das Repository:

   git clone <[REPOSITORY_URL](https://github.com/Data-Science-1362/Tic-Tac-Toe.git)>
3. Installiere die benötigten Bibliotheken:
   
    pip install RPi.GPIO RPLCD neopixel

## Verwendung

### TicTacToe
1. Lade die Fragen aus der JSON-Datei fragen.json.
2. Starte das Spiel:
   
   python tic-tac-toe.py

### GameBoard
Das GameBoard wird automatisch von der TicTacToe-Klasse verwendet, um den Spielstatus anzuzeigen.
