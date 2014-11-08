#!/usr/bin/python

import pygame

pygame.init()

height = 300
width = 600
screen = pygame.display.set_mode([width, height])
ball = pygame.image.load("../resources/ball.png").convert_alpha()
screen.blit(ball, (0, 0))
while True:
    pygame.display.flip()
    continue
