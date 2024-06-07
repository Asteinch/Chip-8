from src.processor import *
from src.display import *
from src.debugger.debugger import *

import copy


import pygame,time
from pygame.locals import *

class Main:

    def __init__(self) -> None:
        
        self.processor = Processor()
        #self.display = Display()
        self.debugger = Debugger()


        self.debug = True

        self.debug_input_flag = False

        self.EMU_CLOCK = USEREVENT + 1 # 60 Hz. for the timers and display
        self.CPU_CLOCK = USEREVENT + 2 # 720 Hz. For the CPU

        pygame.time.set_timer(self.EMU_CLOCK, round((1/EMU_CLOCK_RATE)*1000))
        pygame.time.set_timer(self.CPU_CLOCK, round((1/CPU_CLOCK_RATE)*1000))

        self.clock = pygame.time.Clock()

    def loop(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == self.EMU_CLOCK:

                    self.processor.key_pad.get_all_pressed()
                    self.debugger.display_emulator(self.processor.frame_buffer)
                    self.processor.refresh_timers()

                    self.debugger.draw_pc(self.processor.PC)
                    self.debugger.draw_I(self.processor.I)
                    self.debugger.draw_registers(self.processor.V)
                    self.debugger.draw_memory(self.processor.memory, self.processor.PC)
                    self.debugger.update()

                if event.type == self.CPU_CLOCK and not self.debug:

                    self.processor.execute_opcode(self.processor.fetch_opcode())

                if self.debug:

                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_RIGHT] and not self.debug_input_flag:

                        self.processor.execute_opcode(self.processor.fetch_opcode())

                        self.debugger.prev_values.append(copy.deepcopy([  

                                                            self.processor.PC, 
                                                            self.processor.current_opcode, 
                                                            self.processor.V, 
                                                            self.processor.stack,
                                                            self.processor.I,
                                                            self.processor.frame_buffer, 
                                                            self.processor.sound_timer, 
                                                            self.processor.delay_timer  
                                                            
                                                            ]))
                    
                        self.debugger.frames += 1
                        self.debug_input_flag = True

                    if keys[pygame.K_LEFT] and self.debugger.frames > 0 and not self.debug_input_flag:

                        values = self.debugger.prev_values.pop(-1)
 
                        self.processor.PC = values[0]
                        self.processor.current_opcode = values[1]
                        self.processor.V = values[2]
                        self.processor.stack = values[3]
                        self.processor.I = values[4]
                        self.processor.frame_buffer = values[5]
                        self.processor.sound_timer = values[6]
                        self.processor.delay_timer = values[7]

                        self.debugger.frames -= 1
                        self.debug_input_flag = True

                    if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] or keys[pygame.K_LSHIFT]:
                        self.debug_input_flag = False




                self.clock.tick(MAX_CLOCK)
                          
main = Main()
main.loop()
