#!/usr/bin/python

# SCALABILITY
# FRAME-RATE-LIMITING

import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255) 
BLACK = (0, 0, 0)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 600
SPEED_SCALE = 1.1
X = 0
Y = 1
MOVEMENT_SENSITIVITY = 0.3
FRICTION = .1
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 14
PADDING = 1


class Drawable:
    def __init__(self, surface, position=(0, 0)):
        self.set_position(position)
        self.surface = surface

    def get_rect(self):
        return self.surface.get_rect(topleft=self.position)

    def set_position(self, position):
        self.position = position

    def draw(self, dest):
        dest.blit(self.surface, self.position)

    def move(self, offset):
        self.position = (self.position[X] + offset[X],
                         self.position[Y] + offset[Y])

    def collides(self, other):
        other_rect = other.get_rect()
        self_rect = self.get_rect()
        if(other_rect.collidepoint(self_rect.midleft)):
            return "left"
        if(other_rect.collidepoint(self_rect.midright)):
            return "right"
        if(other_rect.collidepoint(self_rect.midtop)):
            return "top"
        if(other_rect.collidepoint(self_rect.midbottom)):
            return "bottom"

        return


class Square(Drawable):
    def __init__(self, surface, color, position=(0, 0)):
        Drawable.__init__(self, surface, position)
        self.surface.fill(color)


class Paddle(Square):
    def __init__(self, surface, color, position=(0, 0), velocity=(0, 0)):
        Square.__init__(self, surface, color, position)
        self.velocity = velocity

    def get_velocity(self):
        return self.velocity

    def step(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT]):
            self.velocity = (self.velocity[X] - MOVEMENT_SENSITIVITY,
                             self.velocity[Y])
        elif(keys[pygame.K_RIGHT]):
            self.velocity = (self.velocity[X] + MOVEMENT_SENSITIVITY,
                             self.velocity[Y])
        else:
            self.velocity = (self.velocity[X] * (1 - FRICTION), self.velocity[1])
        self.move(self.velocity)
        if(self.position[X] < 0):
            self.position = (0, self.position[Y])
            self.velocity = (0, self.velocity[Y])

        width = self.surface.get_width()
        if(self.position[X] + width > SCREEN_WIDTH):
            self.position = (SCREEN_WIDTH - width, self.position[Y])
            self.velocity = (0, self.velocity[Y])


class Ball(Square):
    def __init__(self, surface, color, position=(0, 0), velocity=(0, -1)):
        Square.__init__(self, surface, color, position)
        self.velocity = velocity

    def set_velocity(self, velocity):
        self.velocity = velocity

    def reverse_velocity(self, direction, scale=1):
        if(direction == "left" or direction == "right"):
            self.velocity = (-self.velocity[X] * scale, 
                             self.velocity[Y] * scale)
        if(direction == "top" or direction == "bottom"):
            self.velocity = (self.velocity[X] * scale, 
                             -self.velocity[Y] * scale)

    def inherit_velocity(self, parent):
        velocity_cap = 3
        parent_velocity = parent.get_velocity()
        self.velocity = (self.velocity[X] + parent_velocity[X],
                         self.velocity[Y] + parent_velocity[Y])
        if(self.velocity[X] > velocity_cap):
            self.velocity = (velocity_cap, self.velocity[Y])
        if(self.velocity[Y] > velocity_cap):
            self.velocity = (self.velocity[X], velocity_cap)

    def step(self):
        width = self.surface.get_width()
        height = self.surface.get_height()
        if(self.position[X] + self.velocity[Y] < 0 or
           self.position[X] + width + self.velocity[Y] > SCREEN_WIDTH):
            self.velocity = (-self.velocity[X], self.velocity[Y])

        if(self.position[Y] + self.velocity[Y] < 0 or
           self.position[Y] + height + self.velocity[Y] > SCREEN_HEIGHT):
            self.velocity = (self.velocity[X], -self.velocity[Y])

        self.move(self.velocity)


class Level:
    def __init__(self):
        self.blocks = []

    def draw(self, screen):
        for block in self.blocks:
            block.draw(screen)

    def remove(self, block):
        self.blocks.remove(block)

    def load(self, layout):
        self.blocks = []
        for row in range(len(layout)):
            for col in range(len(layout[row])):
                char = layout[row][col]
                if(char == '-'):
                    self.blocks.append(
                        Square(pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT)),
                               RED, position=(col * (BLOCK_WIDTH + PADDING),
                                              row * (BLOCK_HEIGHT + PADDING)))
                    )
        return self.blocks


def game_init():
    screen.get_rect()
    ball = Ball(pygame.Surface((3, 3)), GREEN, (315, 450))
    paddle = Paddle(pygame.Surface((30, 3)), BLUE, (290, 550))
    level = Level()
    layout = [
        '.--------.',
        '.-........',
        '.-........',
        '.-........',
        '.-........',
        '.-........',
        '.-........',
        '.--------.',
        '..........',
        '.--------.',
        '.-......-.',
        '.-......-.',
        '.-......-.',
        '.-......-.',
        '.-......-.',
        '.-......-.',
        '.--------.',
        '..........',
        '.-------..',
        '.-.....-..',
        '.-......-.',
        '.-......-.',
        '.-.....-..',
        '.-------..',
        '..........',
        '.-------..',
        '.-........',
        '.-........',
        '.-........',
        '.-------..',
        '.-........',
        '.-........',
        '.-........',
        '.-------..',
    ]

    level.load(layout)
    game_loop(screen, ball, paddle, level)


def game_loop(screen, ball, paddle, level):
    while True:
        handle_events()
        step_game(ball, paddle, level)
        draw_game(screen, ball, paddle, level)

        # force framerate
        pygame.time.Clock().tick(60)


def draw_game(screen, ball, paddle, level):
    screen.fill(BLACK)
    ball.draw(screen)
    paddle.draw(screen)
    level.draw(screen)
    pygame.display.flip()


def step_game(ball, paddle, level):
    ball.step()
    paddle.step()

    collision_direction = ball.collides(paddle)
    if(collision_direction):
        ball.reverse_velocity(collision_direction, SPEED_SCALE)
        ball.inherit_velocity(paddle)

    for block in level.blocks:
        collision_direction = ball.collides(block)
        if(collision_direction):
            level.remove(block)
            ball.reverse_velocity(collision_direction)
    return


def handle_events():
    #Ask for more events
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_ESCAPE]):
        cleanup()
    if(keys[pygame.K_r]):
        game_init()


def cleanup():
    exit(1)


pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
game_init()
