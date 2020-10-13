import pygame


class theBase:
    """
    this class is the ground of the game,the movable ground
    """
    Velocity = 5

    def __init__(self, y,image):
        self.y = y
        self.x1 = 0
        self.WIDTH = image.get_width()
        self.image = image
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.Velocity
        self.x2 -= self.Velocity

        # we cycle between the base image as soon as one leaves the screen we replace it with another
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.image, (self.x1, self.y))
        win.blit(self.image, (self.x2, self.y))

    def blitRotateCenter(surf, image, topleft, angle):
        """
        Rotate a surface and blit it to the window
        :param surf: the surface to blit to
        :param image: the image surface to rotate
        :param topLeft: the top left position of the image
        :param angle: a float value for angle
        :return: None
        """
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

        surf.blit(rotated_image, new_rect.topleft)