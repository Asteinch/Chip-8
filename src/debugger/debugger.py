import pygame
from constants import *
pygame.init()
pygame.font.init()


class Debugger:

    def __init__(self):

        self.debug_screen = pygame.display.set_mode((1920, 1080))

        self.font = pygame.font.SysFont('Calibri', 30)

        self.white = (255, 255, 255)

        self.rows = [40 * i for i in range(1, 30)]

        self.prev_values = []

        self.frames = 0


    def display_emulator(self, buffer):

        for i, rows in enumerate(buffer):
            for j, cols in enumerate(rows):
                
                if buffer[i][j] == 0x1:
                    pygame.draw.rect(self.debug_screen, PIXEL_ON_COLOR, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    pygame.draw.rect(self.debug_screen, PIXEL_OFF_COLOR, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    def draw_pc(self, pc):

        surface = self.font.render("PC: " + str(pc), True, self.white)
        self.debug_screen.blit(surface, (1100, self.rows[3]))
        
    def draw_I(self, I):

        surface = self.font.render("I: " + str(I), True, self.white)
        self.debug_screen.blit(surface, (1100, self.rows[4]))
    def draw_registers(self, v):

        self.debug_screen.blit(self.font.render("REGISTERS", True, self.white),(1100, self.rows[1]))

        text_surfaces = [
            self.font.render("V[0]: " + str(v[0]), True, self.white),
            self.font.render("V[1]: " + str(v[1]), True, self.white),
            self.font.render("V[2]: " + str(v[2]), True, self.white),
            self.font.render("V[3]: " + str(v[3]), True, self.white),
            self.font.render("V[4]: " + str(v[4]), True, self.white),
            self.font.render("V[5]: " + str(v[5]), True, self.white),
            self.font.render("V[6]: " + str(v[6]), True, self.white),
            self.font.render("V[7]: " + str(v[7]), True, self.white),
            self.font.render("V[8]: " + str(v[8]), True, self.white),
            self.font.render("V[9]: " + str(v[9]), True, self.white),
            self.font.render("V[A]: " + str(v[10]), True, self.white),
            self.font.render("V[B]: " + str(v[11]), True, self.white),
            self.font.render("V[C]: " + str(v[12]), True, self.white),
            self.font.render("V[D]: " + str(v[13]), True, self.white),
            self.font.render("V[E]: " + str(v[14]), True, self.white),
            self.font.render("V[F]: " + str(v[15]), True, self.white)
        ]


        for index, r in enumerate(text_surfaces, 6):
            self.debug_screen.blit(r, (1100, self.rows[index]))

    def draw_memory(self, memory, pc):

        self.debug_screen.blit(self.font.render("MEMORY", True, self.white),(1400, self.rows[1]))

        text_surfaces = []

        for i in range(-20, 22, 2):
            text_surfaces.append(
                self.font.render(str(pc + i) +": " + hex((memory[pc + i] << 8) | memory[pc+i+0x1]), True, self.white)
            )

        pygame.draw.rect(self.debug_screen, "darkgreen", (1400, self.rows[12], 200, 30))
        for index, r in enumerate(text_surfaces, 2):
            self.debug_screen.blit(r, (1400, self.rows[index]))

    def update(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                exit()

        frame_counter = self.font.render(str(self.frames), True, self.white)
        self.debug_screen.blit(frame_counter, (1100, self.rows[0]))

        pygame.display.update()
        self.debug_screen.fill("black")