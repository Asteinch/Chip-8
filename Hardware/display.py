import pygame

from constants import *

class Display:

    def __init__(self) -> None:
        
        self.display = pygame.display.set_mode((64 * PIXEL_SIZE, 32 * PIXEL_SIZE))


    def display_buffer(self, buffer):

        for i, rows in enumerate(buffer):
            for j, cols in enumerate(rows):
                
                if buffer[i][j] == 0x1:
                    pygame.draw.rect(self.display, PIXEL_ON_COLOR, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    pygame.draw.rect(self.display, PIXEL_OFF_COLOR, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    def update(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                exit()


        pygame.display.update()