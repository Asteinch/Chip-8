from Hardware.chip8 import *
from Hardware.display import *

import pygame
from pygame.locals import *

class Main:

    def __init__(self) -> None:
        
        self.chip8 = Chip8()
        self.display = Display()

        self.EMU_CLOCK = USEREVENT + 1 # 60 Hz. for the timers and display
        self.CPU_CLOCK = USEREVENT + 2 # 720 Hz. For the CPU

        pygame.time.set_timer(self.EMU_CLOCK, round((1/EMU_CLOCK_RATE)*1000))
        pygame.time.set_timer(self.CPU_CLOCK, round((1/CPU_CLOCK_RATE)*1000))

        self.clock = pygame.time.Clock()

    def loop(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == self.EMU_CLOCK:

                    self.display.display_buffer(self.chip8.frame_buffer)
                    self.chip8.refresh_timers()
                    self.display.update()

                if event.type == self.CPU_CLOCK:

                    self.chip8.fetch_opcodes()
                    self.chip8.execute_opcode()
                    

                self.clock.tick(MAX_CLOCK)
                
            
main = Main()
main.loop()