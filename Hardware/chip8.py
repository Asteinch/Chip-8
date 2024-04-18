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

        self.end_of_rom_data = 0xFFF

        self.current_opcode = 0x0000

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
        

        self.clock = pygame.time.Clock()
        self.load_essentials()

        self.start_time = time.time()

    def get_screen(self, buffer):
        self.frame_buffer = buffer

    
    def load_essentials(self):

        with open("rom.ch8", "rb") as file:    # Loading the rom to memory from 0x200 -> 0xFFF
            file_bytes = file.read()

            for i, byte in enumerate(file_bytes, 0x200): # Inherits each byte in the rom and adds to memory
                self.memory[i] = hex(byte)
            
            self.end_of_rom_data = i

        #Loading the system Font
        for i, byte in enumerate(self.font, 0x0): # Loading system Font to memory from 0x0 -> 0x200

            self.memory[i] = byte
        

    def fetch_opcodes(self):

        if self.PC > self.end_of_rom_data: # Increments the Program Counter by 2 if under 0xFFF
            self.PC = 0x200

        first_nibble = int(self.memory[self.PC], 16)   
        second_nibble = int(self.memory[self.PC+0x1], 16)

        opcode = (first_nibble << 8) | second_nibble # Merges the two bytes to one

        self.PC += 0x2

        self.current_opcode = hex(opcode)

  
    
    def execute_opcode(self):

        opcode = int(self.current_opcode, 16)

        nibble_1 = (opcode & 0xF000) >> 12
        nibble_2 = (opcode & 0x0F00) >> 8
        nibble_3 = (opcode & 0x00F0) >> 4
        nibble_4 = (opcode & 0x000F)


        print(nibble_1, nibble_2, nibble_3, nibble_4)

        match nibble_1:

            case 0xA:

                self.I = (nibble_2) << 8 | (nibble_3 << 4) | nibble_4
            
            case 0xC:

                rnd = random.randint(0, 255)
                kk = (nibble_3 << 4) | nibble_4

    

                self.V[nibble_2] = (rnd & kk)

            case 0x3:

                kk = (nibble_3 << 4) | nibble_4

                if kk == self.V[nibble_2]:
                    self.PC += 0x2
                
            case 0xD: # Horror

                x = (nibble_2 << 8) % 64
                y = (nibble_3 << 4) % 32

                self.V[0xF] = 0

                for i in range(0, nibble_4):

                    sprite_data = self.memory[self.I + i]
                    sprite_data = int(sprite_data, 16)
                    

                    for b in range(0, 8):

                        current_pixel = (sprite_data >> b) & 1

                        if (current_pixel == 1 and self.frame_buffer[y][x] == 1):

                            self.frame_buffer[y][x] = 0
                            self.V[0xF] = 1

                        elif ( current_pixel == 1 and self.frame_buffer[y][x] == 0):

                            self.frame_buffer[y][x] = 1

                        if x == 64:
                            break
                        x += 1

                    y += 1
                    if y == 32:
                        break

            case 0x7:

                self.V[nibble_2] += (nibble_3 << 4) | nibble_4

            case 0x1:

                self.PC = (nibble_2) << 8 | (nibble_3 << 4) | nibble_4

            case 0x6:

                self.V[nibble_2] = (nibble_3 << 4) | nibble_4

            case 0x8:

                self.V[nibble_2] = self.V[nibble_3]

            case 0x2:

                self.stack.insert(0, self.PC)

                self.PC = (nibble_2) << 8 | (nibble_3 << 4) | nibble_4

 





                        

                        

                        











    
    def refresh_timers(self):

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1






    