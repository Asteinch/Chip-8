import pygame,time, random
    
class Chip8:

    def __init__(self) -> None:

        self.PC = 0x200

        self.memory = [0x0] * 4096
        self.V = [0x0] * 16    
        self.stack = [0x0] * 16

        self.I = 0x0

        self.delay_timer = 0x3C
        self.sound_timer = 0x3C

        self.current_opcode = 0x0000

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
        
        self.frame_buffer = [[0x0] * 64 for _ in range(32)]
        
        self.load_essentials()

    
    def load_essentials(self):

        with open("rom.ch8", "rb") as file:    # Loading the rom to memory from 0x200 -> 0xFFF
            file_bytes = file.read()

            for i, byte in enumerate(file_bytes, 0x200): # Inherits each byte in the rom and adds to memory
                self.memory[i] = byte
            
            self.end_of_rom_data = i

        #Loading the system Font
        for i, byte in enumerate(self.font, 0x0): # Loading system Font to memory from 0x0 -> 0x200

            self.memory[i] = byte
        

    def fetch_opcode(self):

        if self.PC > self.end_of_rom_data: # Resets program counter if it reached the end of rom
            self.PC = 0x200

        first_nibble = self.memory[self.PC] 
        second_nibble = self.memory[self.PC+0x1]

        self.current_opcode = (first_nibble << 8) | second_nibble # Merges the two bytes to one

        self.PC += 0x2

    
    def execute_opcode(self):

        opcode = self.current_opcode

        n1 = (opcode & 0xF000) >> 12
        n2 = (opcode & 0x0F00) >> 8
        n3 = (opcode & 0x00F0) >> 4
        n4 = (opcode & 0x000F)

        match n1:

            case 0x1:
                # 0x1nnn: sets program counter to nnn

                self.PC = (n2) << 8 | (n3 << 4) | n4

            case 0x2:
                # 0x2nnn: adds program counter to stack and sets program coutner to nnn

                self.stack.insert(0, self.PC)

                self.PC = (n2) << 8 | (n3 << 4) | n4

            case 0x3:
                # 0x3xkk: increments program counter if kk and v[x] match

                kk = (n3 << 4) | n4

                if kk == self.V[n2]:
                    self.PC += 0x2
        
            case 0x6:
                # 0x6xkk: sets v[x] to kk

                self.V[n2] = (n3 << 4) | n4

            case 0x7:
                # 0x8xkk: increments v[x] with kk

                self.V[n2] += (n3 << 4) | n4

            case 0x8:
                # 0x8xy0: sets v[x] to v[y]

                self.V[n2] = self.V[n3]
          
            case 0xA:
                # 0xAnnn: sets I to nnn

                self.I = (n2) << 8 | (n3 << 4) | n4
            
            case 0xC:
                # 0xCxkk: ANDs kk and rnd(0, 255) and stores in v[x]

                rnd = random.randint(0, 255)
                kk = (n3 << 4) | n4

                self.V[n2] = (rnd & kk)


            case 0xD: # Horror
                # 0xDxyn: draws n tall sprite at x=v[x], y=v[y]

                x_pos = self.V[n2]
                y_pos = self.V[n3]

                self.V[0xF] = 0

                for y in range(0, n4):

                    pixel_byte = self.memory[self.I + y]

                    for x in range(0, 8):

                        pixel_bit = pixel_byte & (0b10000000 >> x)

                        if pixel_bit != 0:

                            if self.frame_buffer[y_pos+y][x_pos+x] == 1:

                                self.V[0xF] = 1
                            
                            self.frame_buffer[y_pos+y][x_pos+x] = not self.frame_buffer[y_pos+y][x_pos+x]
         


    def refresh_timers(self):

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1
