import pygame

import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = -5
BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 50
POWERUP_SIZE = 20
POWERUP_SPEED = 3
POWERUP_CHANCE = 0.2  

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 200)
CYAN = (50, 200, 200)
ORANGE = (255, 150, 50)
POWERUP_COLOR = (255, 215, 0)  

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick")
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    pygame.display.flip()