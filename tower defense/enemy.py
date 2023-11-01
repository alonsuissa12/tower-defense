import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, screen, img: list, x=1000, y=1000, pathA_x=None, pathA_y=1000, pathB_y=None,
                 pathC_x=None, scale=1, life=2):
        super().__init__()
        if pathB_y is None:
            pathB_y = [1000]
        if pathC_x is None:
            pathC_x = [1000]
        if pathA_x is None:
            pathA_x = [1000]
        self.scale = scale
        self.images_list = img
        self.image_index = 0.0
        self.life = life
        self.x = x
        self.y = y
        self.part = 'A'
        self.index = 0
        self.pathA_x = pathA_x
        self.pathC_x = pathC_x
        self.pathA_y = pathA_y
        self.pathB_y = pathB_y
        self.screen = screen
        temp_img = pygame.image.load(img[0][int(self.image_index)])
        self.image = pygame.transform.scale(temp_img, (temp_img.get_width() * scale, temp_img.get_height() * scale))
        self.rect = self.image.get_rect()

    def update(self):
        self.move()

    def move(self):
        if self.part == 'A':
            self.image_update(0)
            self.x = self.pathA_x[self.index]
            self.y = self.pathA_y
            self.index += 1
            if self.index == len(self.pathA_x):
                self.index = 0
                self.part = 'B'

        elif self.part == 'B':
            self.image_update(1)
            self.y = self.pathB_y[self.index]
            self.index += 1
            if self.index == len(self.pathB_y):
                self.index = 0
                self.part = 'C'

        elif self.part == 'C':
            self.image_update(2)
            self.x = self.pathC_x[self.index]
            self.index += 1
            if self.index == len(self.pathC_x):
                self.index = 0
                self.part = 'D'
        self.rect.center = (self.x, self.y)

    def image_update(self, part: int):
        temp_img = pygame.image.load(self.images_list[part][int(self.image_index)])
        self.image = pygame.transform.scale(temp_img,
                                            (temp_img.get_width() * self.scale, temp_img.get_height() * self.scale))
        self.image_index = self.image_index + 0.25
        if self.image_index >= len(self.images_list[part]):
            self.image_index = 0

    def hit(self):
        self.life -= 1
        if self.life == 0:
            self.kill()

    def got_to_end(self):
        if self.x <= -10 and self.y > 300:
            self.kill()

            return -1
        return 0

    def is_on_screen(self) -> bool:
        if (self.x <= -5 and self.y > 300) or not self.alive():
            return False
        return True
