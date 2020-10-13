import random
import pygame


class greenPipe:
    """
    class represents the pipes in the game
    """
    GAP = 200
    VELOCITY = 5

    def __init__(self, x, image):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        # one pipe needs to be upside down
        self.PIPE_TOP = pygame.transform.flip(image, False, True)
        self.PIPE_BOTTOM = image
        # if bird passed pipe
        self.passed = False
        self.setPipe_height()

    def setPipe_height(self):
        self.height = random.randrange(50, 430)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        # if birds dont collide this returns none
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(bottom_mask, top_offset)
        # checking if bird collides with any pipes on screen
        if t_point or b_point:
            return True
        return False
