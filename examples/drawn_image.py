#!/usr/bin/python

import pygame

pygame.init()

height = 300
width = 600
screen = pygame.display.set_mode([width, height])
ball = pygame.image.load("../resources/ball.png").convert_alpha()

# Surfaces are "blit" or "drawn" to other surfaces in this case the screen
screen.blit(ball, (0, 0))
while True:
    # Here we switch buffers
    pygame.display.flip()
