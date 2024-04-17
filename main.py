from Hardware.chip8 import *
from Hardware.display import *

class Main:

    def __init__(self) -> None:
        
        self.chip8 = Chip8()
        self.display = Display()


    def loop(self):
        while True:

            self.chip8.cpu_tick()

            self.display.update()

main = Main()
main.loop()