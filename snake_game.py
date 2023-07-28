import pygame
import time
import random
from collections import deque
from queue import PriorityQueue


class SnakeGame:
    def __init__(self):
        pygame.init()

        self.cell_size = 20
        self.grid_size = (30, 30)
        self.window_size = (self.grid_size[0] * self.cell_size, self.grid_size[1] * self.cell_size)
        self.game_window = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.snake_body = deque([[5, 5], [4, 5]])
        self.direction = 'RIGHT'
        self.score = 0
        self.fruit_spawn = True
        self.toggle_ai = False

        self.colors = {
            "black": pygame.Color(0, 0, 0),
            "white": pygame.Color(255, 255, 255),
            "red": pygame.Color(255, 0, 0),
            "green": pygame.Color(0, 255, 0),
        }

        self.snake_head = pygame.transform.scale(pygame.image.load("assets/snake_head.png"),
                                                 (self.cell_size - 1, self.cell_size - 1))
        apple = pygame.transform.scale(pygame.image.load("assets/carrot.png"), (self.cell_size, self.cell_size))
        carrot = pygame.transform.scale(pygame.image.load("assets/apple.png"), (self.cell_size, self.cell_size))
        melon = pygame.transform.scale(pygame.image.load("assets/melon.png"), (self.cell_size, self.cell_size))
        beet = pygame.transform.scale(pygame.image.load("assets/beet.png"), (self.cell_size, self.cell_size))

        self.fruits = [apple, carrot, melon, beet]
        self.fruit_position = self.random_fruit_position()
        self.fruit = random.choice(self.fruits)

    def random_fruit_position(self):
        while True:
            new_pos = [random.randrange(0, self.grid_size[0]), random.randrange(0, self.grid_size[1])]
            if new_pos not in self.snake_body:
                return new_pos

    def draw_text(self, content, font, size, color, pos1):
        font = pygame.font.SysFont(font, size)
        surface = font.render(content, True, color)
        rect = surface.get_rect()
        rect.midtop = pos1
        self.game_window.blit(surface, rect)

    def game_over(self):
        self.draw_text('Your Score is : ' + str(self.score), 'times new roman', 50, self.colors['red'],
                       self.game_window.get_rect().midtop)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        quit()

    def draw_rect(self, color, position):
        pygame.draw.rect(self.game_window, color,
                         pygame.Rect(position[0] * self.cell_size,
                                     position[1] * self.cell_size, self.cell_size - 1, self.cell_size - 1))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.toggle_ai:
                        self.toggle_ai = True
                    else:
                        self.toggle_ai = False

            if not self.toggle_ai:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != 'DOWN':
                        self.direction = 'UP'
                    if event.key == pygame.K_DOWN and self.direction != 'UP':
                        self.direction = 'DOWN'
                    if event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                        self.direction = 'LEFT'
                    if event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                        self.direction = 'RIGHT'

    def is_collision(self):
        if self.snake_body[0][0] < 0 or self.snake_body[0][0] > self.grid_size[0] - 1 or self.snake_body[0][1] < 0 \
                or self.snake_body[0][1] > self.grid_size[1] - 1 or self.snake_body[0] in list(self.snake_body)[1:]:
            return True

    def a_star(self, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {start: None}
        cost_so_far = {start: 0}
        snake_body = [tuple(body_part) for body_part in self.snake_body]

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in [(current[0] + 1, current[1]), (current[0] - 1, current[1]), (current[0], current[1] + 1),
                         (current[0], current[1] - 1)]:
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    if 0 <= next[0] < self.grid_size[0] and 0 <= next[1] < self.grid_size[1] and next not in snake_body:
                        cost_so_far[next] = new_cost
                        priority = new_cost + heuristic(goal, next)
                        frontier.put(next, priority)
                        came_from[next] = current

        current = goal
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]

        return path[::-1]

    def find_path(self):
        return self.a_star(tuple(self.snake_body[0]), tuple(self.fruit_position))

    def draw_path(self, path):
        for i in range(len(path)):
            pygame.draw.rect(self.game_window, (255, 255, 255),
                             pygame.Rect(path[i][0] * self.cell_size + 8,
                                         path[i][1] * self.cell_size + 8, 4, 4))

    def follow_path(self, path):
        if len(path) < 2:
            return
        dx = path[1][0] - path[0][0]
        dy = path[1][1] - path[0][1]
        if dx == 1:
            self.direction = 'RIGHT'
        elif dx == -1:
            self.direction = 'LEFT'
        elif dy == 1:
            self.direction = 'DOWN'
        elif dy == -1:
            self.direction = 'UP'

    def update_snake_position(self):
        direction_dict = {'UP': [self.snake_body[0][0], self.snake_body[0][1] - 1],
                          'DOWN': [self.snake_body[0][0], self.snake_body[0][1] + 1],
                          'LEFT': [self.snake_body[0][0] - 1, self.snake_body[0][1]],
                          'RIGHT': [self.snake_body[0][0] + 1, self.snake_body[0][1]]}
        self.snake_body.appendleft(direction_dict[self.direction])

    def handle_fruit_eating(self):
        if self.snake_body[0] == self.fruit_position:
            self.score += 10
            self.fruit_spawn = False
        else:
            self.snake_body.pop()

    def spawn_fruit(self):
        if not self.fruit_spawn:
            self.fruit_position = self.random_fruit_position()
            self.fruit = random.choice(self.fruits)
            self.fruit_spawn = True

    def draw_game_objects(self):
        for index, pos in enumerate(self.snake_body):
            if index == 0:
                self.game_window.blit(self.snake_head, (pos[0] * self.cell_size, pos[1] * self.cell_size))
            else:
                self.draw_rect(self.colors["green"], pos)

        self.game_window.blit(self.fruit,
                              (self.fruit_position[0] * self.cell_size, self.fruit_position[1] * self.cell_size))

    def display_game_info(self):
        self.draw_text('Score : ' + str(self.score), 'times new roman', 17, self.colors["white"], (40, 0))
        self.draw_text('Time : ' + str(pygame.time.get_ticks() // 1000), 'times new roman', 17, self.colors["white"],
                       (self.window_size[0] - 40, 0))
        if self.toggle_ai:
            ai = "True"
        else:
            ai = "False"
        self.draw_text("Toggle AI:" + ai, 'times new roman', 17, self.colors["white"],
                       (self.window_size[0] / 2, 0))

    def play_game(self):
        while True:
            self.game_window.fill((40, 40, 40))
            if self.toggle_ai:
                path = self.find_path()
                self.draw_path(path)
                self.follow_path(path)
                self.handle_input()
            else:
                self.handle_input()

            self.update_snake_position()
            self.handle_fruit_eating()
            self.spawn_fruit()
            self.draw_game_objects()

            if self.is_collision():
                self.game_over()

            self.display_game_info()
            pygame.display.update()
            self.clock.tick(20)


if __name__ == "__main__":
    SnakeGame().play_game()
