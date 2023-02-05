import random
import pygame
import enemy
import sys

pygame.init()

game_speed = 1
fps = 30
screen_w = 800
screen_h = 600
score = 0
life = 5
default_round_length = -300
max_round = 8

big_font = pygame.font.Font('freesansbold.ttf', 80)
med_font = pygame.font.Font('freesansbold.ttf', 50)
small_font = pygame.font.Font('freesansbold.ttf', 20)

screen = pygame.display.set_mode((screen_w, screen_h))

pygame.display.set_caption("tower defence")
# icon = pygame.image.load('001-ufo.png')
# pygame.display.set_icon(icon)

background_img = pygame.image.load("background_leve1.png")

enemy1_imgs_path = [["enemy1_frame1_faceRight.xcf", "enemy1_frame2_faceRight.xcf"],
                    ["enemy1_frame1_faceLeft.xcf", "enemy1_frame2_faceLeft.xcf"],
                    ["enemy1_frame1_faceLeft.xcf", "enemy1_frame2_faceLeft.xcf"]]

enemy2_imgs_path = [["enemy2_frame1_faceRight.xcf", "enemy2_frame2_faceRight.xcf", "enemy2_frame3_faceRight.xcf"],
                    ["enemy2_frame1_faceForward.xcf", "enemy2_frame2_faceForward.xcf", "enemy2_frame3_faceForward.xcf"],
                    ["enemy2_frame1_faceLeft.xcf", "enemy2_frame2_faceLeft.xcf", "enemy2_frame3_faceLeft.xcf"]]


def define_path(enemy1: enemy, start_time, speed=1):
    # part A
    end = random.randint(560, 680)
    pathA_x = [i for i in range(start_time, end, int(speed * game_speed))]
    pathA_y = random.randint(110, 210)
    enemy1.pathA_x = pathA_x
    enemy1.pathA_y = pathA_y

    # part B
    end = random.randint(440, 530)
    pathB_x = pathA_x
    pathB_y = [i for i in range(pathA_y, end, int(speed * game_speed))]
    enemy1.pathB_y = pathB_y

    # part C
    start = pathB_x[len(pathB_x) - 1]
    pathC_x = [i for i in range(start, -20, int(-speed * game_speed))]
    enemy1.pathC_x = pathC_x


def life_update(enemies_list: list):
    global life
    for e in enemies_list:
        life += e.got_to_end()


def life_update2(group):
    life_update(group.sprites())


def Round(round_number, number_of_enemies: list, start_time=None, speeds=None):
    if speeds is None:
        speeds = [2, 2, 2, 2, 2, 2, 2]
    if start_time is None:
        start_time = [[random.randint(default_round_length, 0) for j in range(number_of_enemies[k])] for k in
                      range(len(number_of_enemies))]
    groups = [pygame.sprite.Group() for _ in range(len(number_of_enemies))]
    for i in range(len(number_of_enemies)):
        if i == 0:
            for j in range(number_of_enemies[i]):
                enemy1 = enemy.Enemy(screen, enemy1_imgs_path, scale=1)
                groups[i].add(enemy1)
                define_path(enemy1, start_time[i][j], 2)
        if i == 1:
            for j in range(number_of_enemies[i]):
                enemy2 = enemy.Enemy(screen, enemy2_imgs_path, scale=1, life=5)
                groups[i].add(enemy2)
                define_path(enemy2, start_time[i][j])
    return groups


def play_round(groups, num, text_on: bool):
    if text_on:
        text = big_font.render("ROUND " + str(num), True, (50, 100, 80))
        screen.blit(text, (200, 250))
        pygame.display.update()
        pygame.time.wait(1500)
    for group in groups:
        group.update()
        group.draw(screen)


# rounds
round1 = Round(1, [1], [[random.randint(-100, 0) for _ in range(1)]])
round2 = Round(2, [5], [[random.randint(-100, 0) for _ in range(5)]])
round3 = Round(3, [15], [[random.randint(-100, 0) for _ in range(15)]])
round4 = Round(4, [30], [[random.randint(-100, 0) for _ in range(30)]])
round5 = Round(5, [0, 1], [[], [random.randint(-100, 0) for _ in range(1)]])
round6 = Round(6, [10, 2],
               [[random.randint(-150, 0) for _ in range(10)], [random.randint(-160, -130) for _ in range(2)]])
round7 = Round(7, [20, 7],
               [[random.randint(-150, 0) for _ in range(20)], [random.randint(-160, -130) for _ in range(7)]])
round8 = Round(7, [20, 20],
               [[random.randint(-170, -30) for _ in range(20)], [random.randint(-160, 0) for _ in range(20)]])
rounds = [round1, round2, round3, round4, round5, round6, round7, round8]


def round_manager(round_num):
    return rounds[round_num - 1]


def game_loop():
    global score, life
    is_round_on = False

    round_num = 0
    current_round = round1
    clock = pygame.time.Clock()
    game_run = True
    game_playing = True
    is_text = True
    while game_run:
        while game_playing:
            # print(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if not is_round_on:
                round_num += 1
                if round_num != max_round:
                    current_round = round_manager(round_num)
                    is_round_on = True
                    is_text = True
                else:
                    pass  # win event !!

            screen.blit(background_img, (0, 0))

            score_text = small_font.render("score: " + str(score), True, (100, 100, 50))
            life_text = small_font.render("life: " + str(life), True, (200, 70, 50))

            screen.blit(life_text, (20, 40))
            screen.blit(score_text, (20, 20))

            play_round(current_round, round_num, is_text)
            is_text = False
            # enemies_group.draw(screen)
            # enemies_group.update()
            temp = False
            for group in current_round:
                life_update2(group)
                for enemy_ in group:
                    temp = temp or enemy_.is_on_screen()
            if not temp:
                is_round_on = temp

            pygame.display.update()
            clock.tick(fps)


game_loop()
