import pygame


class Bird:
    """
    this is the class for the flappy bird
    """
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y, images):
        self.x = x
        self.y = y
        self.tilt = 0
        self.ticking_counter = 0
        self.velocity = 0
        self. height = self.y
        self.image_counter = 0
        self.img = images[0]
        self.imgs = images

    def jump(self):
        self.velocity = -10.5
        self.ticking_counter = 0
        self.height = self.y

    def move(self):
        self.ticking_counter += 1
        direction = self.velocity * self.ticking_counter + 1.5 * self.ticking_counter ** 2

        if direction >= 16:
            direction = 16

        if direction < 0:
            direction -= 2.5

        self.y = self.y + direction

        if direction < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.image_counter += 1
        if self.image_counter < self.ANIMATION_TIME:
            self.img = self.imgs[0]
        elif self.image_counter < self.ANIMATION_TIME * 2:
            self.img = self.imgs[1]
        elif self.image_counter < self.ANIMATION_TIME * 3:
            self.img = self.imgs[2]
        elif self.image_counter < self.ANIMATION_TIME * 4:
            self.img = self.imgs[1]
        elif self.image_counter < self.ANIMATION_TIME * 4 + 1:
            self.img = self.imgs[0]
            self.image_counter = 0

        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.image_counter = self.ANIMATION_TIME * 2

        # code for proper rotation of img(taken from stackoverflow)
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x , self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

