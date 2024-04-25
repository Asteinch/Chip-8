import pygame,time, random

from Hardware.keypad import Keypad
from constants import *
    
class Chip8:

    def __init__(self) -> None:

        self.PC = 0x200

        self.memory = [0x0] * 4096
        self.V = [0x0] * 16    
        self.stack = [0x0] * 16

        self.I = 0x0

        self.delay_timer = 0x3C
        self.sound_timer = 0x3C

        self.key_pad = Keypad()

        self.current_opcode = 0x0000

        self.end_of_rom_data = 0xFFF

        self.font = FONT
        
        self.frame_buffer = [[0x0] * 64 for _ in range(32)]
        
        self.load_essentials()
    
    def load_essentials(self):

        with open("Roms/opcode.ch8", "rb") as file:    # Loading the rom to memory from 0x200 -> 0xFFF
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

            case 0x0:
                match (n1 << 12) |( n2 << 8) | (n3 << 4) | n4:

                    case 0x00E0:
                        self.frame_buffer = [[0x0] * 64 for _ in range(32)]

                    case 0x00EE:
                        self.PC = self.stack[0]
                        self.stack.pop(0)

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

            case 0x4:
                # 0x4xkk: increments program counter if kk and v[x] DONT match

                kk = (n3 << 4) | n4       

                if kk != self.V[n2]:
                    self.PC += 0x2
            
            case 0x5:
                # 5xy0: increments program counter if v[x] and v[y] match

                if self.V[n2] == self.V[n3]:
                    self.PC += 0x2

            case 0x6:
                # 0x6xkk: sets v[x] to kk

                self.V[n2] = (n3 << 4) | n4

            case 0x7:
                # 0x7xkk: increments v[x] with kk

                self.V[n2] += (n3 << 4) | n4

            case 0x8:

                match n4:

                    case 0x0:
                        # 0x8xy0: sets v[x] to v[y]

                        self.V[n2] = self.V[n3]

                    case 0x1:
                        # 0x8xy1: ORs v[x] and v[y]

                        self.V[n2] |= self.V[n3]

                    case 0x2:
                        # 0x8xy2: ANDs v[x] and v[y]

                        self.V[n2] &= self.V[n3]
                    
                    case 0x3:
                        # 0x8xy3: XORs v[x] and v[y]

                        self.V[n2] ^= self.V[n3]

                    case 0x4:
                        # 0x8xy4: if v[x] + v[y] > 255, v[f] wil be set to 1 and last 8 bits of v[x] + v[y] will be stored in v[x], else v[f] = 0

                        xy = self.V[n2] + self.V[n3]
                        if xy > 255:
                            self.V[0xF] = 1

                        self.V[0xF] = 0
                        self.V[n2] = xy

                    case 0x5:
                        # 0x8xy5: sets v[f] to 1 if v[x] > v[y] else 0. stores v[x] - v[y] in v[x]

                        self.V[0xF] = 1 if self.V[n2] > self.V[n3] else 0

                        self.V[n2] -= self.V[n3]

                    case 0x6:
                        # 0x8xy6: sets v[f] to least-significant in v[x] and divides v[x] by 2

                        least_significant_bit = self.V[n2] & 1

                        self.V[0xF] = least_significant_bit

                        self.V[n2] /= 2
                                                    

                    case 0x7:
                        # 0x8xy7: sets v[f] to 1 if v[y] > v[x] else 0. stores v[y] - v[x] in v[x]

                        self.V[0xF] = 1 if self.V[n3] > self.V[n2] else 0

                        self.V[n2] = self.V[n3] - self.V[n2]
                    
                    case 0xE:
                        # 0x8xyE: sets v[f] to most-significant in v[x] and multiplies v[x] by 2

                        most_significant_bit = (self.V[n2] >> (len(bin(self.V[n2])) - 2)) & 1


                        self.V[0xF] = most_significant_bit

                        self.V[n2] *= 2

                        
            case 0x9:
                # 0x9xy0: increments program counter if v[x] and v[y] dont match

                if self.V[n2] != self.V[n3]:
                    self.PC += 0x2


            case 0xA:
                # 0xAnnn: sets I to nnn

                self.I = (n2 << 8) | (n3 << 4) | n4

            case 0xB:
                # 0xBnnn: sets program counter to nnn plus v[0]

                nnn = (n2 << 8) | (n3 << 4) | n4

                self.PC = nnn + self.V[0x0]


            
            case 0xC:
                # 0xCxkk: ANDs kk and rnd(0, 255) and stores in v[x]

                rnd = random.randint(0, 255)
                kk = (n3 << 4) | n4

                self.V[n2] = (rnd & kk)


            case 0xD: # Horror
                # 0xDxyn: draws n tall sprite at x=v[x], y=v[y]

                x_pos = self.V[n2]%64
                y_pos = self.V[n3]%32

                self.V[0xF] = 0

                for y in range(0, n4):

                    pixel_byte = self.memory[self.I + y]

                    for x in range(0, 8):

                        pixel_bit = pixel_byte & (0b10000000 >> x)

                        if pixel_bit != 0:

                            if self.frame_buffer[(y_pos + y)%32][(x_pos+x)%64] == 1:

                                self.V[0xF] = 1
                            
                            self.frame_buffer[(y_pos + y)%32][(x_pos+x)%64] = not self.frame_buffer[(y_pos + y)%32][(x_pos+x)%64] 

            case 0xE:

                match (n3 >> 2) | n4:

                    case 0x9E:
                        if self.key_pad.keys[self.v[n2]] == 1:

                            self.PC += 0x2

                    case 0xA1:

                        if self.key_pad.keys[self.v[n2]] != 1:

                            self.PC += 0x2

            case 0xF:

                match (n3 >> 2) | 4:

                    case 0x07:

                        self.V[n2] = self.delay_timer

                    case 0x0A:
                        
                        key_been_pressed = False

                        while not key_been_pressed:

                            for i, key in enumerate(self.key_pad):

                                if key == 1:
                                    key_been_pressed = True
                                    break
                        
                        self.V[n2] = i

                    case 0x15:

                        self.delay_timer = self.V[n2]

                    case 0x18:

                        self.sound_timer = self.V[n2]

                    case 0x1E:

                        self.I += self.V[n2]

                    case 0x29:

                        for i, hex in enumerate(self.memory, 0x0):
                            if self.V[n2] == self.memory[i]:
                                self.I = i
                                break
                    case 0x55:

                        for i in range(n2 + 1):

                            self.memory[self.I + i - 1] = self.V[i - 1]

                    case 0x65:

                        for i in range(n2 + 1):

                            self.memory[i - 1] = self.I[ - 1]
                            

                     
    def refresh_timers(self):

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1
