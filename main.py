from src.processor import *
from src.display import *

import pygame
from pygame.locals import *

import os

class Main:

    def __init__(self) -> None:

        while not (path := input("TYPE ROM PATH: ")).endswith(".ch8") or not os.path.exists("roms/" + path):
            print("Invalid path!")
    
        self.processor = Processor()
        self.display = Display()

        self.EMU_CLOCK = USEREVENT + 1 # 60 Hz. for the timers and display
        self.CPU_CLOCK = USEREVENT + 2 # 720 Hz. For the CPU

        pygame.time.set_timer(self.EMU_CLOCK, round((1/EMU_CLOCK_RATE)*1000))
        pygame.time.set_timer(self.CPU_CLOCK, round((1/CPU_CLOCK_RATE)*1000))

        self.clock = pygame.time.Clock()

        pygame.display.set_caption(path)
        self.processor.load_essentials(path)

    def loop(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == self.EMU_CLOCK:

                    self.processor.key_pad.get_all_pressed()
                    self.processor.refresh_timers()
                    self.display.display_buffer(self.processor.frame_buffer)
                    self.display.update()

                if event.type == self.CPU_CLOCK:

                    opcode = self.processor.fetch_opcode()
                    self.processor.execute_opcode(opcode)

                self.clock.tick(MAX_CLOCK)

main = Main()
main.loop()
