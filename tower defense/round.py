import random

import pygame
import enemy


class Round(pygame.sprite.Sprite):

    def __init__(self, screen, num_of_enemies: list, images_paths: list, speeds=None, round_lengths=None, game_speed=1,
                 scales=None):
        super().__init__()
        if speeds is None:
            speeds = [2, 2]
        if scales is None:
            scales = [1.5, 1.5]
        if round_lengths is None:
            round_lengths = [-300]
        self.speeds = speeds
        self.round_length = round_lengths
        self.screen = screen
        self.scales = scales
        self.num_of_enemies = num_of_enemies
        self.groups = [pygame.sprite.Group(), pygame.sprite.Group()]
        self.images_paths = images_paths
        self.game_speed = game_speed
        self.create_enemies_group()

    def create_enemies_group(self):
        for i in range(len(self.num_of_enemies)):
            if i == 0:
                enemy1 = enemy.Enemy(self.screen, self.images_paths[i], self.scales[i])
                self.groups[i].add(enemy1)
                self.define_path(enemy1, self.round_length[i], self.speeds[i])

    def play_round(self):
        for group in self.groups:
            group.update()
            group.draw(self.screen)

