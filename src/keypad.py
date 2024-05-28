import pygame

class Keypad:

    def __init__(self):

        self.keys = [0x0] * 16

        self.key_binds = {
            0x1 : pygame.K_1,
            0x2 : pygame.K_2,
            0x3 : pygame.K_3,
            0xC : pygame.K_4,
            0x4 : pygame.K_q,
            0x5 : pygame.K_w,
            0x6 : pygame.K_e,
            0xD : pygame.K_r,
            0x7 : pygame.K_a,
            0x8 : pygame.K_s,
            0x9 : pygame.K_d,
            0xE : pygame.K_f,
            0xA : pygame.K_z,
            0x0 : pygame.K_x,
            0xB : pygame.K_c,
            0xF : pygame.K_v
        }

    def get_all_pressed(self):

    
        keys = pygame.key.get_pressed()

        for i in range(0x0, 0xF + 1):

            self.keys[i] = 1 if keys[self.key_binds[i]] else 0

    
