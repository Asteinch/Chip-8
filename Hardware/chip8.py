import pygame
    
class Chip8:

    def __init__(self) -> None:
        
        self.mhz = 700

        self.PC = 0x200

        self.memory = [0x0] * 4096
        self.registers = [0x0] * 16    
        self.stack = [0x0] * 16

        self.delay_timer = 0x3C
        self.sound_timer = 0x3C

        self.font = [   0xF0, 0x90, 0x90, 0x90, 0xF0,
                        0x20, 0x60, 0x20, 0x20, 0x70,
                        0xF0, 0x10, 0xF0, 0x80, 0xF0,
                        0xF0, 0x10, 0xF0, 0x10, 0xF0,
                        0x90, 0x90, 0xF0, 0x10, 0x10,
                        0xF0, 0x80, 0xF0, 0x10, 0xF0, 
                        0xF0, 0x80, 0xF0, 0x90, 0xF0,
                        0xF0, 0x10, 0x20, 0x40, 0x40, 
                        0xF0, 0x90, 0xF0, 0x90, 0xF0,
                        0xF0, 0x90, 0xF0, 0x10, 0xF0,
                        0xF0, 0x90, 0xF0, 0x90, 0x90,
                        0xE0, 0x90, 0xE0, 0x90, 0xE0, 
                        0xF0, 0x80, 0x80, 0x80, 0xF0,
                        0xE0, 0x90, 0x90, 0x90, 0xE0,
                        0xF0, 0x80, 0xF0, 0x80, 0xF0,
                        0xF0, 0x80, 0xF0, 0x80, 0x80    ]
        
        self.clock = pygame.time.Clock()

        self.load_essentials()

    
    def load_essentials(self):

        with open("rom.ch8", "rb") as file:    # Loading the rom to memory from 0x200 -> 0xFFF
            file_bytes = file.read()

            for i, byte in enumerate(file_bytes, 0x200): # Inherits each byte in the rom and adds to memory
                self.memory[i] = hex(byte)

        #Loading the system Font
        for i, byte in enumerate(self.font, 0x0): # Loading system Font to memory from 0x0 -> 0x200

            self.memory[i] = byte


    def cpu_tick(self):

        self.clock.tick(self.mhz)

        if self.PC > 0xFFF: # Increments the Program Counter by 2 if under 0xFFF
            self.PC = 0x200

        if (self.memory[self.PC] != 0x0 and self.memory[self.PC + 0x1] !=0x0): # Reads ONLY non-empty Data

            print(self.memory[self.PC],":",self.memory[self.PC + 0x001]) # Groups the two bytes to a 16-bit number


    