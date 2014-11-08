#!/usr/bin/python

import pygame

pygame.init()

width = 600
height = 300
screen = pygame.display.set_mode([width, height])
while True:
    # It's okay if you don't know what this does I'll get to this call
    # But it's important to have at the end of your render loop
    screen.flip()
    continue
