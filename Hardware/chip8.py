import pygame,time
    
class Chip8:

    def __init__(self) -> None:

        self.PC = 0x200

        self.memory = [0x0] * 4096
        self.registers = [0x0] * 16    
        self.stack = [0x0] * 16

        self.delay_timer = 0x3C
        self.sound_timer = 0x3C

        self.end_of_rom_data = 0xFFF

        self.font = [0xF0, 0x90, 0x90, 0x90, 0xF0,
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
                0xF0, 0x80, 0xF0, 0x80, 0x80]
        
        self.clock = pygame.time.Clock()
        self.load_essentials()

        self.start_time = time.time()

    
    def load_essentials(self):

        with open("rom.ch8", "rb") as file:    # Loading the rom to memory from 0x200 -> 0xFFF
            file_bytes = file.read()

            for i, byte in enumerate(file_bytes, 0x200): # Inherits each byte in the rom and adds to memory
                self.memory[i] = hex(byte)
            
            self.end_of_rom_data = i

        #Loading the system Font
        for i, byte in enumerate(self.font, 0x0): # Loading system Font to memory from 0x0 -> 0x200

            self.memory[i] = byte
        

    def CPU_cycle(self):

        if self.PC > self.end_of_rom_data: # Increments the Program Counter by 2 if under 0xFFF
            self.PC = 0x200

        if (self.memory[self.PC] != 0x0 and self.memory[self.PC + 0x1] !=0x0): # Reads ONLY non-empty Data

            print(self.memory[self.PC],":",self.memory[self.PC + 0x1]) # Groups the two bytes to a 16-bit number

        self.PC += 0x2

    def refresh_timers(self):

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1




    