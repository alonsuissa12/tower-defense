import pygame

purple = (155, 70, 239)
light_purple = (176, 156, 217)
black = (0, 0, 0)


class button:
    def __init__(self, surface, text, x, y, width, height, text_size=17, active_color=light_purple,
                 inactive_color=purple, text_color=black):
        self.screen = surface
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font('freesansbold.ttf', text_size)
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text_color = text_color
        self.clicked = False

    def text_to_button(self):
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (self.x + (self.width / 2), self.y + (self.height / 2))
        self.screen.blit(text, text_rect.topleft)

    def click(self):
        pass

    def is_clicked(self):
        click = self.clicked
        self.clicked = False
        return click

    def draw(self):
        cur = pygame.mouse.get_pos()
        if (self.x <= cur[0] <= self.x + self.width) and (self.y <= cur[1] <= self.y + self.height):
            if pygame.mouse.get_pressed()[0] == 1:
                if not self.clicked:
                    self.click()
                    self.clicked = True
            else:
                self.clicked = False
            pygame.draw.rect(self.screen, self.active_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.screen, self.inactive_color, (self.x, self.y, self.width, self.height))
        self.text_to_button()

