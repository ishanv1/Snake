import pygame
import random

class Food(object):
    FOOD_UNIT = 15

    def __init__(self, game_surface):
        """
        A piece of snake food.
        """
        game_rect = game_surface.get_rect()
        self.surface = pygame.Surface((self.FOOD_UNIT, self.FOOD_UNIT))

        # Give the food piece a random, solid RGB color.
        r = random.randint(0x00, 0xFF)
        g = random.randint(0x00, 0xFF)
        b = random.randint(0x00, 0xFF)
        self.surface.fill((r, g, b))

        # Place the food piece randomly on the screen.
        self.pos = [random.randint(0, game_rect.width),
                    random.randint(0, game_rect.height)]
        self.surface.scroll(self.pos[0], self.pos[1])
        game_surface.blit(self.surface, self.surface.get_rect())


    def update(self, game_surface):
        """
        Redraw the food.
        """
        rect = self.surface.get_rect().move(self.pos)
        game_surface.blit(self.surface, rect)


    def get_rect(self):
        return self.surface.get_rect().move(self.pos)
