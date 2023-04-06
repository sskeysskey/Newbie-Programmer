import pygame
import sys
import random

# 初始化
pygame.init()
clock = pygame.time.Clock()

# 屏幕大小
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20

# 颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 贪吃蛇类
class Snake:
    def __init__(self):
        self.body = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = pygame.K_RIGHT

    def move(self):
        x, y = self.body[0]
        if self.direction == pygame.K_UP:
            y -= GRID_SIZE
        elif self.direction == pygame.K_DOWN:
            y += GRID_SIZE
        elif self.direction == pygame.K_LEFT:
            x -= GRID_SIZE
        elif self.direction == pygame.K_RIGHT:
            x += GRID_SIZE
        self.body.insert(0, (x, y))

    def eat(self, food):
        if self.body[0] == food.position:
            self.body.append(self.body[-1])
            food.randomize()
            return True
        return False

    def collides(self):
        head = self.body[0]
        return (head in self.body[1:]) or (head[0] < 0) or (head[1] < 0) or (head[0] >= SCREEN_WIDTH) or (head[1] >= SCREEN_HEIGHT)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize()

    def randomize(self):
        self.position = (random.randrange(0, SCREEN_WIDTH // GRID_SIZE) * GRID_SIZE, random.randrange(0, SCREEN_HEIGHT // GRID_SIZE) * GRID_SIZE)

# 屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("贪吃蛇")

snake = Snake()
food = Food()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                snake.direction = event.key

    snake.move()

    if snake.collides():
        pygame.quit()
        sys.exit()

    if snake.eat(food):
        pass

    screen.fill(WHITE)

    for x, y in snake.body:
        pygame.draw.rect(screen, GREEN, (x, y, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, RED, (food.position[0], food.position[1], GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    clock.tick(10)