import pygame
import random

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Втеча з лабіринту')

background_color = (0, 0, 0)
cell_size = 40

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.0)
pygame.mixer.music.play(-1)

sound_key = pygame.mixer.Sound('sound_key.mp3')
sound_key.set_volume(1.0)

sound_door = pygame.mixer.Sound('sound_door.mp3')
sound_door.set_volume(1.0)

player_img = [pygame.image.load(f'{i}.png') for i in range(1, 5)]
player_img = [pygame.transform.scale(player, (cell_size, cell_size)) for player in player_img]
player_id = 0

wall_img = pygame.image.load('wall.png')
wall_img = pygame.transform.scale(wall_img, (cell_size, cell_size))

key_img = pygame.image.load('key.png')
key_img = pygame.transform.scale(key_img, (cell_size, cell_size))

door_img = pygame.image.load('door.png')
door_img = pygame.transform.scale(door_img, (cell_size, cell_size))

background_image = pygame.image.load('maze.png')
background_image = pygame.transform.scale(background_image, (800, 600))

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

free_cells = []
for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == 0:
            free_cells.append([x, y])

key_position = random.choice(free_cells[:-1])
door_position = free_cells[-1]

clock = pygame.time.Clock()
fps = 15
player_x, player_y = 1, 1
key_exists = False


def draw_button(screen, text, color, x, y, w, h):
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + (w - text_surface.get_width()) / 2, y + (h - text_surface.get_height()) / 2))


def how_to_play():
    font = pygame.font.SysFont(None, 32)
    running_info = True

    while running_info:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_info = False
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running_info = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running_info = False

        screen.blit(background_image, (0, 0))

        screen.blit(font.render("Як грати:", True, (255, 255, 255)), (50, 60))
        screen.blit(font.render("UP    - вверх на 1 клітинку", True, (255, 255, 255)), (50, 110))
        screen.blit(font.render("DOWN  - вниз на 1 клітинку", True, (255, 255, 255)), (50, 150))
        screen.blit(font.render("LEFT  - вліво на 1 клітинку", True, (255, 255, 255)), (50, 190))
        screen.blit(font.render("RIGHT - вправо на 1 клітинку", True, (255, 255, 255)), (50, 230))
        screen.blit(font.render("Мета: знайти ключ і дійти до дверей", True, (255, 255, 255)), (50, 290))
        screen.blit(font.render("ESC або клік мишкою - назад", True, (255, 255, 255)), (50, 350))

        pygame.display.flip()


def main_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 <= x <= 650 and 150 <= y <= 250:
                    menu = False
                elif 150 <= x <= 650 and 250 <= y <= 350:
                    how_to_play()
                elif 150 <= x <= 650 and 350 <= y <= 450:
                    menu = False
                    exit()

        screen.blit(background_image, (0, 0))
        draw_button(screen, "Почати гру", (0, 150, 0), 150, 150, 500, 100)
        draw_button(screen, "Як грати", (0, 120, 200), 150, 250, 500, 100)
        draw_button(screen, "Вийти", (200, 0, 0), 150, 350, 500, 100)
        pygame.display.flip()


def win():
    win = True
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 <= x <= 650 and 200 <= y <= 300:
                    win = False
                elif 150 <= x <= 650 and 350 <= y <= 450:
                    win = False
                    exit()

        screen.blit(background_image, (0, 0))
        draw_button(screen, "Вітаю! Ти пройшов гру!", (0, 150, 0), 150, 200, 500, 100)
        draw_button(screen, "Вийти", (200, 0, 0), 150, 350, 500, 100)
        pygame.display.flip()


main_menu()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_x > 0 and maze[player_y][player_x - 1] == 0:
                player_x -= 1
            if event.key == pygame.K_RIGHT and player_x < len(maze[0]) - 1 and maze[player_y][player_x + 1] == 0:
                player_x += 1
            if event.key == pygame.K_UP and player_y > 0 and maze[player_y - 1][player_x] == 0:
                player_y -= 1
            if event.key == pygame.K_DOWN and player_y < len(maze) - 1 and maze[player_y + 1][player_x] == 0:
                player_y += 1
    screen.fill(background_color)
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:
                screen.blit(wall_img, (x * cell_size, y * cell_size))

    if not key_exists:
        if [player_x, player_y] == key_position:
            key_exists = True
            sound_key.play()
        else:
            screen.blit(key_img, (key_position[0] * cell_size, key_position[1] * cell_size))

    screen.blit(door_img, (door_position[0] * cell_size, door_position[1] * cell_size))
    screen.blit(player_img[player_id], (player_x * cell_size, player_y * cell_size))
    player_id = (player_id + 1) % len(player_img)

    if key_exists and [player_x, player_y] == door_position:
        sound_door.play()
        running = False

    pygame.display.flip()
    clock.tick(fps)

win()
pygame.quit()