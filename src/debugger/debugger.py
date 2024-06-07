import pygame
import copy
from constants import *
from src.processor import Processor
pygame.init()
pygame.font.init()


class Debugger:

    def __init__(self):

        self.debug_cpu = Processor()
        self.debug_screen = pygame.display.set_mode((1920, 1080))
        self.debug_input_flag = False


        self.font = pygame.font.SysFont('Calibri', 30)
        self.white = (255, 255, 255)

        self.rows = [40 * i for i in range(1, 30)]
        self.frames = 0

        self.prev_values = []


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

        register_surfaces = [
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


        for index, r in enumerate(register_surfaces, 6):
            self.debug_screen.blit(r, (1100, self.rows[index]))

    def draw_memory(self, memory, pc):

        self.debug_screen.blit(self.font.render("MEMORY", True, self.white),(1400, self.rows[1]))

        memory_surfaces = []

        for i in range(-20, 22, 2):
            memory_surfaces.append(
                self.font.render(str(pc + i) +": " + hex((memory[pc + i] << 8) | memory[pc+i+0x1]), True, self.white)
            )

        pygame.draw.rect(self.debug_screen, "darkgreen", (1400, self.rows[12], 200, 30))
        for index, r in enumerate(memory_surfaces, 2):
            self.debug_screen.blit(r, (1400, self.rows[index]))

    def draw_stack(self, stack):

        stack_16 = [stack[i] for i in range(16)]

        stack_surface = self.font.render("STACK: " + str(stack_16), True, self.white)
        self.debug_screen.blit(stack_surface, (1100, self.rows[25]))

    def draw_timer(self, dt, st):

        sound_surface = self.font.render("SOUND TIMER: " + str(st), True, self.white)
        delay_surface = self.font.render("DELAY TIMER: " + str(dt), True, self.white)

        self.debug_screen.blit(sound_surface, (1100, self.rows[23]))
        self.debug_screen.blit(delay_surface, (1100, self.rows[24]))

    def draw_screen(self):

        self.draw_pc(self.debug_cpu.PC)
        self.draw_I(self.debug_cpu.I)
        self.draw_registers(self.debug_cpu.V)
        self.draw_memory(self.debug_cpu.memory, self.debug_cpu.PC)
        self.draw_stack(self.debug_cpu.stack)
        self.draw_timer(self.debug_cpu.delay_timer, self.debug_cpu.sound_timer)

    def input_hell(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and not self.debug_input_flag:

            self.debug_cpu.execute_opcode(self.debug_cpu.fetch_opcode())

            self.prev_values.append(copy.deepcopy([  

                                                            self.debug_cpu.PC, 
                                                            self.debug_cpu.current_opcode, 
                                                            self.debug_cpu.V, 
                                                            self.debug_cpu.stack,
                                                            self.debug_cpu.I,
                                                            self.debug_cpu.frame_buffer, 
                                                            self.debug_cpu.sound_timer, 
                                                            self.debug_cpu.delay_timer  
                                                            
                                                            ]))
                    
            self.frames += 1
            self.debug_input_flag = True

        if keys[pygame.K_LEFT] and self.frames > 0 and not self.debug_input_flag:

            values = self.debugger.prev_values.pop(-1)
 
            self.debug_cpu.PC = values[0]
            self.debug_cpu.current_opcode = values[1]
            self.debug_cpu.V = values[2]
            self.debug_cpu.stack = values[3]
            self.debug_cpu.I = values[4]
            self.debug_cpu.frame_buffer = values[5]
            self.debug_cpu.sound_timer = values[6]
            self.debug_cpu.delay_timer = values[7]

            self.frames -= 1
            self.debug_input_flag = True

        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] or keys[pygame.K_LSHIFT]:
            self.debug_input_flag = False


    def update(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                exit()

        self.debug_cpu.refresh_timers()
        self.debug_cpu.key_pad.get_all_pressed()

        self.display_emulator(self.debug_cpu.frame_buffer)
        self.draw_screen()

        frame_counter = self.font.render(str(self.frames), True, self.white)
        self.debug_screen.blit(frame_counter, (1100, self.rows[0]))

        pygame.display.update()
        self.debug_screen.fill("black")