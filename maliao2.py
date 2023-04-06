import pygame
import sys

# 初始化
pygame.init()
clock = pygame.time.Clock()

# 屏幕大小
screen_width = 1024
screen_height = 551

# 创建屏幕
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("简易马里奥")

# 加载背景图像
background = pygame.image.load("images/background.png").convert()

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, width=50, height=50, image_file='images/character.png'):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (width, height))  # 添加这一行
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.rect.width = width
        self.rect.height = height
        self.is_jumping = False  # 添加这一行
        self.on_pipe = False  # 添加这一行
        self.velocity_y = 0  # 添加这一行

    def collide_with_pipe(self, pipes):
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                # 从上方碰撞
                if self.velocity_y > 0 and self.rect.bottom <= pipe.rect.top + 5:
                    self.on_pipe = True
                    self.is_jumping = False
                    self.velocity_y = 0
                    self.rect.bottom = pipe.rect.top
                # 从下方碰撞
                elif self.velocity_y < 0 and self.rect.top >= pipe.rect.bottom - 5:
                    self.rect.top = pipe.rect.bottom
                    self.velocity_y = 0
                # 从左侧碰撞
                elif self.rect.right >= pipe.rect.left and self.rect.left < pipe.rect.left:
                    self.rect.right = pipe.rect.left
                # 从右侧碰撞
                elif self.rect.left <= pipe.rect.right and self.rect.right > pipe.rect.right:
                    self.rect.left = pipe.rect.right
            else:
                self.on_pipe = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.is_jumping or not self.on_pipe:
            self.rect.y += self.velocity_y
            self.velocity_y += 1
            if self.rect.y >= screen_height - 100:
                self.is_jumping = False
                self.rect.y = screen_height - 100
                self.velocity_y = 0

        if self.on_pipe:
            if self.rect.bottom <= pipe.rect.top:
                self.rect.bottom = pipe.rect.top
            else:
                self.on_pipe = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -15

# 水管类
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_file):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.rect.width = width
        self.rect.height = height

# 创建玩家和水管
player = Player()
pipe = Pipe(561, 446, 50, 200, 'images/smallpipe.png')
big_pipe = Pipe(817, 420, 50, 200, 'images/bigpipe.png')
all_sprites = pygame.sprite.Group()
all_sprites.add(player, pipe, big_pipe)

# 游戏循环
running = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    all_sprites.update()

    pipes = [pipe, big_pipe]
    player.collide_with_pipe(pipes)

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)