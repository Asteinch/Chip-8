import pygame

from constants import *

class Display:

    def __init__(self) -> None:
        
        self.display = pygame.display.set_mode((64 * PIXEL_SIZE, 32 * PIXEL_SIZE))

        self.frame_buffer = [[0x0] * 64 for _ in range(32)]

    def display_buffer(self):

        for i, rows in enumerate(self.frame_buffer):
            for j, cols in enumerate(rows):
                
                if self.frame_buffer[i][j] == 0x1:
                    pygame.draw.rect(self.display, PIXEL_ON_COLOR, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    pygame.draw.rect(self.display, PIXEL_OFF_COLOR, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    def update(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                exit()

        self.display_buffer()

        pygame.display.update()