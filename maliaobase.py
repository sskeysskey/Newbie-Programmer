import pygame
import sys

# 初始化
pygame.init()
clock = pygame.time.Clock()

# 屏幕大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 颜色
WHITE = (255, 255, 255)

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 100
        self.is_jumping = False
        self.velocity_y = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.is_jumping:
            self.rect.y += self.velocity_y
            self.velocity_y += 1
            if self.rect.y >= SCREEN_HEIGHT - 100:
                self.is_jumping = False
                self.rect.y = SCREEN_HEIGHT - 100
                self.velocity_y = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -15

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("简易马里奥")

# 创建玩家
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# 游戏循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    all_sprites.update()

    screen.fill(WHITE)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)