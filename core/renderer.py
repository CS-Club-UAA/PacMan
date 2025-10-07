# This file handles all rendering tasks using Pygame.

import pygame


class Renderer:
    def __init__(self, screen):
        self.screen = screen

    # This is temporary space for the reTile function
    def reTile(self, color, rect):
        tile_size = min(width, height) // settings["maze_size"]
        pass

    def draw_circle(self, color, pos, radius):
        pygame.draw.circle(self.screen, color, pos, radius)
