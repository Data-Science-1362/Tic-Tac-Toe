import csv
import json
import RPi.GPIO as GPIO
from time import sleep
from RPLCD.i2c import CharLCD
from GameBoard import GameBoard

class Keypad:
    def __init__(self, column_count=4):
        # Initialisiert das GPIO-Modul und setzt den Modus auf BCM
        GPIO.setmode(GPIO.BCM)
        # Definiert das Tastenlayout des Keypads
        self.KEYPAD = [
            [1, 2, 3, "A"],
            [4, 5, 6, "B"],
            [7, 8, 9, "C"],
            ["*", 0, "#", "D"]
        ]
        # Definiert die GPIO-Pins für die Reihen und Spalten
        self.ROW = [7, 8, 11, 25]
        self.COLUMN = [24, 10, 9, 12]

    def get_key(self):
        # Setzt die Spalten als Ausgänge und zieht sie auf LOW
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
        # Setzt die Reihen als Eingänge mit Pull-up-Widerständen
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Überprüft, ob eine Taste gedrückt wurde (Reihe)
        row_val = -1
        for i in range(len(self.ROW)):
            tmp_read = GPIO.input(self.ROW[i])
            if tmp_read == 0:
                row_val = i
        
        # Wenn keine Taste gedrückt wurde, beendet die Methode
        if row_val < 0 or row_val > 3:
            self.exit()
            return None
        
        # Setzt die Spalten als Eingänge mit Pull-down-Widerständen
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Setzt die gefundene Reihe als Ausgang und zieht sie auf HIGH
        GPIO.setup(self.ROW[row_val], GPIO.OUT)
        GPIO.output(self.ROW[row_val], GPIO.HIGH)
        
        # Überprüft, ob eine Taste gedrückt wurde (Spalte)
        col_val = -1
        for j in range(len(self.COLUMN)):
            tmp_read = GPIO.input(self.COLUMN[j])
            if tmp_read == 1:
                col_val = j
        
        # Wenn keine Taste gedrückt wurde, beendet die Methode
        if col_val < 0 or col_val > 3:
            self.exit()
            return None
        
        # Stellt den Ausgangszustand der GPIO-Pins wieder her
        self.exit()
        # Gibt die gedrückte Taste zurück
        return self.KEYPAD[row_val][col_val]

    def exit(self):
        # Setzt alle Reihen und Spalten wieder auf Eingänge mit Pull-up-Widerständen
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

class TicTacToe:
    def __init__(self, questions_file):
        # Initialisiert das Spielbrett und die Spieler
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.players = ["X", "O"]
        self.turn = 0
        self.current_question_index = 0
        self.display = GameBoard()
        
        # Lädt die Fragen aus einer JSON-Datei
        with open(questions_file, 'r', encoding='utf-8') as f:
            self.questions = json.load(f)['Fragen']
        
        # Initialisiert das Keypad
        self.keypad = Keypad()
        
        # Initialisiert das LCD-Display
        self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)
        self.lcd.clear()

        # Initialisiert die CSV-Datei mit Headern
        self.results_file = 'results.csv'
        with open(self.results_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Frage Index', 'Richtige Antwort', 'Gewählte Antwort'])

    def game_reset(self):
        # Setzt das Spiel zurück
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = 0
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Das war super!")
        sleep(2)

    def print_board(self):
        # Zeichnet das Spielbrett auf dem Display und in der Konsole
        self.display.drawGame(self.board)
        for row in self.board:
            print(" | ".join(row))
            print("-" * 5)

    def check_winner(self, player):
        # Überprüft, ob ein Spieler gewonnen hat
        return any(all(s == player for s in row) for row in self.board) or \
               any(all(row[col] == player for row in self.board) for col in range(3)) or \
               all(self.board[i][i] == player for i in range(3)) or \
               all(self.board[i][2 - i] == player for i in range(3))

    def check_draw(self):
        # Überprüft, ob das Spiel unentschieden ist
        return all(all(cell != " " for cell in row) for row in self.board)

    def get_move(self):
        # Wartet auf eine gültige Bewegung vom Keypad
        while True:
            move = self.keypad.get_key()
            if isinstance(move, int) and 1 <= move <= 9:
                move -= 1
                if self.board[move // 3][move % 3] == " ":
                    return move // 3, move % 3

    def scroll_text(self, text, choices, num_rows=4, num_cols=20, delay=4.0):
        # Zeigt Text und Optionen auf dem LCD-Display und wartet auf eine Auswahl vom Keypad
        pos = 0
        tasten = []
        lines = [text[i:i+num_cols] for i in range(0, len(text), num_cols)]
        for key in choices:
            tasten.append(key)
            lines.append(f"{key}: {choices[key]}")
        print(lines)
        curr_line = 0
        max_rows = min(num_rows, len(lines))
        print(max_rows)
        while True:
            self.lcd.clear()
            for i in range(max_rows):
                self.lcd.cursor_pos = (i, 0)
                line_text = lines[i + curr_line]
                self.lcd.write_string(line_text)
            curr_line += 1
            if (curr_line + num_rows) > len(lines):
                curr_line = 0
            
            for i in range(40):
                key = self.keypad.get_key()
                if key in tasten:
                    return key
                sleep(delay / 40)

    def ask_question(self):
        # Stellt die aktuelle Frage und überprüft die Antwort
        question_set = self.questions[self.current_question_index // len(self.questions[0]['Fragen'])]
        question = question_set['Fragen'][self.current_question_index % len(question_set['Fragen'])]
        
        choice = question["Optionen"]
        answer = self.scroll_text(question['Frage'], choice)
        
        correct_answer = question['Antwort']['key']

        # Speichert die Ergebnisse in der CSV-Datei
        with open(self.results_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.current_question_index, correct_answer, answer])

        if answer == correct_answer:
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string("Richtig!")
            sleep(2)
            return True
        
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Falsch!")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(f"Antwort: {question['Antwort']['text']}")
        sleep(4)
        return False

    def play_game(self):
        # Startet das Tic Tac Toe-Spiel
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Das Detmold Tic Tac Toe Raetsel")        
        self.lcd.cursor_pos = (2, 0)
        self.lcd.write_string("X ist Gruen und ") 
        self.lcd.cursor_pos = (3, 0)
        self.lcd.write_string("O ist Rot") 
               
        sleep(10)
               
        while True:
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string(f"Spieler {self.players[self.turn]} ist am ZugWaehle ein Feld 1-9")
            self.print_board()
            row, col = self.get_move()
            print(f"Spieler {self.players[self.turn]} wählt Feld ({row}, {col})")

            if self.ask_question():
                self.board[row][col] = self.players[self.turn]
                if self.check_winner(self.players[self.turn]):
                    self.print_board()
                    print(f"Spieler {self.players[self.turn]} gewinnt!")
                    self.lcd.clear()
                    self.lcd.cursor_pos = (0, 0)
                    self.lcd.write_string(f"Spieler {self.players[self.turn]} gewinnt!")
                    self.display.showWinner(self.players[self.turn])
                    break
                elif self.check_draw():
                    self.print_board()
                    print("Es ist unentschieden!")
                    self.lcd.clear()
                    self.lcd.cursor_pos = (0, 0)
                    self.lcd.write_string("Es ist unentschieden!")
                    sleep(2)
                    break
            
            # Wechselt den Spieler und die Frage
            self.current_question_index = (self.current_question_index + 1) % (len(self.questions) * len(self.questions[0]['Fragen']))
            self.turn = 1 - self.turn

if __name__ == "__main__":
    # Startet das Spiel und setzt es nach jedem Spiel zurück
    game = TicTacToe('fragen.json')
    while True:
        game.play_game()
        game.game_reset()
    GPIO.cleanup()
