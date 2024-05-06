import pygame,time, random, math
pygame.mixer.init()

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

        self.beep = pygame.mixer.Sound("beep.wav")

        self.key_pad = Keypad()

        self.current_opcode = 0x0000

        self.end_of_rom_data = 0xFFF

        self.font = FONT
        
        self.frame_buffer = [[0x0] * 64 for _ in range(32)]
        
        self.load_essentials()
    
    def load_essentials(self):

        with open("Roms/ufo.ch8", "rb") as file:    # Loading the rom to memory from 0x200 -> 0xFFF
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
                        self.PC = self.stack.pop(0)

            case 0x1:
                # 0x1nnn: sets program counter to nnn

                nnn = (n2) << 8 | (n3 << 4) | n4
                self.PC = nnn

            case 0x2:
                # 0x2nnn: adds program counter to stack and sets program coutner to nnn

                self.stack.insert(0, self.PC)

                nnn = (n2) << 8 | (n3 << 4) | n4
                self.PC = nnn

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

                kk = (n3 << 4) | n4

                self.V[n2] = kk

            case 0x7:
                # 0x7xkk: increments v[x] with kk

                kk = (n3 << 4) | n4

                self.V[n2] += kk
                self.V[n2] %= 256

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

                        self.V[0xF] = 1 if self.V[n2] + self.V[n3] > 0xFF else 0

                        self.V[n2] += self.V[n3]
                        self.V[n2] %= 256

                    case 0x5:
                        # 0x8xy5: sets v[f] to 1 if v[x] > v[y] else 0. stores v[x] - v[y] in v[x]

                        self.V[0xF] = 1 if self.V[n2] > self.V[n3] else 0

                        self.V[n2] -= self.V[n3]
                        self.V[n2] %= 256                       

                    case 0x6:
                        # 0x8xy6: sets v[f] to least-significant in v[x] and divides v[x] by 2

                        lst = self.V[n2] & 1

                        self.V[0xF] = lst

                        self.V[n2] /= 2
                        self.V[n2] = math.floor(self.V[n2])
                        self.V[n2] %= 256                                                          

                    case 0x7:
                        # 0x8xy7: sets v[f] to 1 if v[y] > v[x] else 0. stores v[y] - v[x] in v[x]

                        self.V[0xF] = 1 if self.V[n3] > self.V[n2] else 0

                        self.V[n2] = self.V[n3] - self.V[n2]
                        self.V[n2] %= 256        
                    
                    case 0xE:
                        # 0x8xyE: sets v[f] to most-significant in v[x] and multiplies v[x] by 2

                        msb = self.V[n2]

                        while msb > 0b11111111:  # Ensure it's an 8-bit number
                            msb >>= 1

                        msb &= 0b10000000

                        msb = 1 if msb else 0
                    
                        self.V[0xF] = msb

                        self.V[n2] *= 2
                        self.V[n2] %= 256     
                        
            case 0x9:
                # 0x9xy0: increments program counter if v[x] and v[y] dont match

                if self.V[n2] != self.V[n3]:
                    self.PC += 0x2


            case 0xA:
                # 0xAnnn: sets I to nnn

                nnn = (n2 << 8) | (n3 << 4) | n4

                self.I = nnn

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

                match (n3 << 4) | n4:

                    case 0x9E:

                        #0xEx9E: increments progranm counter if key at v[x] is pressed

                        if self.key_pad.keys[self.V[n2]] == 1:

                            self.PC += 0x2

                    case 0xA1:

                        #0xExA1: increments progranm counter if key at v[x] is not pressed

                        if self.key_pad.keys[self.V[n2]] != 1:

                            self.PC += 0x2

            case 0xF:

                match (n3 << 4) | n4:

                    case 0x07:
                        # 0xFx07: sets v[x] to the value in delay timer

                        self.V[n2] = self.delay_timer

                    case 0x0A:
                        # 0xFx0A: waits for key to be pressed, sets v[x] to the index of that key

                        key_been_pressed = False

                        while not key_been_pressed:

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    exit()
                                
                                self.key_pad.get_all_pressed()

                                for i, key in enumerate(self.key_pad.keys):

                                    if key == 1:
                                        key_been_pressed = True
                                        break

                        self.V[n2] = i



                    case 0x15:
                        # 0xFx15: sets delay timer to v[x]

                        self.delay_timer = self.V[n2]

                    case 0x18:
                        # 0xFx18: sets sound timer to v[x]
                        self.sound_timer = self.V[n2]

                    case 0x1E:
                        # 0xFx1E: increments I with v[x] and sets flag to one if overflow, else 0

                        self.I += self.V[n2]
                        self.V[0xF] = 1 if self.I > 0x0FF else 0

                    case 0x29:
                        # 0xFx29: sets I to the location of the hex sprite with value v[x] in memory

                        self.I = self.V[n2] * 5

                    case 0x33:
                        # 0xFx33: split v[x] digits and adds them to memory starting from I. example: 126 -> 1, 2, 6

                        number = self.V[n2]
                        string_of_number = str(number)

                        for i, digit in enumerate(string_of_number):

                            self.memory[self.I+i] = int(digit)


                    case 0x55:
                        # 0xFx55: adds register v[0] -> v[x] to memory startng from adress I

                        for i in range(0, n2 + 1):

                            self.memory[self.I + i] = self.V[i]

                    case 0x65:
                        # 0xfx65: adds values form memory starting at I to v[0] -> v[x]

                        for i in range(0, n2 + 1):

                            self.V[i] = self.memory[self.I + i]

                            
         
    def refresh_timers(self):

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1
            self.beep.play()
