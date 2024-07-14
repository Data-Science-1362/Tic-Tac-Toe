import board
import neopixel
from time import sleep

class GameBoard:
    
    def __init__(self):
        self.pixel_pin = board.D18  
        self.num_pixels = 16 * 16  
        self.ORDER = neopixel.GRB  
        self.static_cols = [4,5,10,11]

        # Initialisiere die NeoPixel-LEDs
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.1, auto_write=False, pixel_order=self.ORDER)
        
        self.Xred = 6
        self.Xgreen = 191
        self.Xblue = 9
        self.Ored = 237
        self.Ogreen = 19
        self.Oblue = 84
        
        self.ledOff()
        
    # Alle LEDs ausschalten
    def ledOff(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
       
        
    def showWinner(self,side):
        if side == "X":
            r = self.Xred
            g = self.Xgreen
            b = self.Xblue
        else:
            r = self.Ored
            g = self.Ogreen
            b = self.Oblue
        
        for x in range(18):
            if x % 2 == 0:
                self.ledOff()
            else:
                for i in range(256):
                    self.pixels[i] = (r, g, b) if self.ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
                self.pixels.show()
            sleep(0.5)

    def calcPixel(self,pos,state):
        r = 0
        g = 0
        b = 0
        
        row = pos // 16
        if row % 2 == 0:
            col = pos % 16
        else:
            col = 15 - (pos % 16)
            
        if col in self.static_cols or row in self.static_cols:
            r = 55
            g = 19
            b = 190
        else:
            gamerow = row // 6
            gamecol = col // 6
            gameval = state[gamerow][gamecol]
            print(gameval)
            if (gameval == "X"):
                r = self.Xred
                g = self.Xgreen
                b = self.Xblue
            elif gameval == "O":
                r = self.Ored
                g = self.Ogreen
                b = self.Oblue
                
        return (r, g, b) if self.ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
        

    def drawGame(self,state):
        for pos in range(256):
            self.pixels[pos] = self.calcPixel(pos,state)
        self.pixels.show()
        