import pygame
import time
import random

pygame.init()

window_size = (900, 600)
game_window = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
snake_body = [[100, 50],
              [90, 50]]
direction = 'RIGHT'
score = 0
fruit_spawn = True

colors = {
    "black": pygame.Color(0, 0, 0),
    "white": pygame.Color(255, 255, 255),
    "red": pygame.Color(255, 0, 0),
    "green": pygame.Color(0, 255, 0),
}

snake_head = pygame.transform.scale(pygame.image.load("assets/snake_head.png"), (18, 18))
apple = pygame.transform.scale(pygame.image.load("assets/carrot.png"), (18, 20))
carrot = pygame.transform.scale(pygame.image.load("assets/apple.png"), (18, 20))
melon = pygame.transform.scale(pygame.image.load("assets/melon.png"), (20, 20))
beet = pygame.transform.scale(pygame.image.load("assets/beet.png"), (20, 20))
potato = pygame.transform.scale(pygame.image.load("assets/potato.png"), (20, 20))

fruits = [apple, carrot, melon, beet]


def random_fruit_position():
    return [random.randrange(1, window_size[0] // 20) * 20,
            random.randrange(1, window_size[1] // 20) * 20]


fruit_position = random_fruit_position()
fruit = random.choice(fruits)


def draw_text(content, font, size, color, pos1):
    font = pygame.font.SysFont(font, size)
    surface = font.render(content, True, color)
    rect = surface.get_rect()
    rect.midtop = pos1
    game_window.blit(surface, rect)


def game_over():
    draw_text('Your Score is : ' + str(score), 'times new roman', 50, colors['red'], game_window.get_rect().midtop)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()


def draw_rect(color, position):
    pygame.draw.rect(game_window, color, pygame.Rect(position[0], position[1], 18, 18))


def handle_input():
    global direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'


while True:
    handle_input()

    if direction == 'UP':
        snake_body.insert(0, [snake_body[0][0], snake_body[0][1] - 20])
    if direction == 'DOWN':
        snake_body.insert(0, [snake_body[0][0], snake_body[0][1] + 20])
    if direction == 'LEFT':
        snake_body.insert(0, [snake_body[0][0] - 20, snake_body[0][1]])
    if direction == 'RIGHT':
        snake_body.insert(0, [snake_body[0][0] + 20, snake_body[0][1]])

    if pygame.Rect(snake_body[0][0], snake_body[0][1], 20, 20).colliderect(
            pygame.Rect(fruit_position[0], fruit_position[1], 20, 20)):
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = random_fruit_position()
        fruit = random.choice(fruits)
        fruit_spawn = True

    game_window.fill((40, 40, 40))
    for index, pos in enumerate(snake_body):
        if index == 0:
            game_window.blit(snake_head, pos)
        else:
            draw_rect(colors["green"], pos)

    game_window.blit(fruit, fruit_position)

    if snake_body[0][0] < 0 or snake_body[0][0] > window_size[0] - 20 or snake_body[0][1] < 0 \
            or snake_body[0][1] > window_size[1] - 20 or snake_body[0] in snake_body[1:]:
        game_over()

    draw_text('Score : ' + str(score), 'times new roman', 20, colors["white"], (40, 0))
    draw_text('Time : ' + str(pygame.time.get_ticks() // 1000), 'times new roman', 20, colors["white"],
              (window_size[0] - 60, 0))
    pygame.display.update()
    clock.tick(20)
