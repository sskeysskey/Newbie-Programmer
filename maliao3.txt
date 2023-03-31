import pygame
import sys

# 初始化
pygame.init()
clock = pygame.time.Clock()

#   全局变量
score = 0 # 分数

#   角色图片
player_left = pygame.image.load('images/character_left.png')
player_right = pygame.image.load('images/character_right.png')

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
    def __init__(self, x=0, y=0, width=50, height=50):
        super().__init__()
        self.image = pygame.transform.scale(player_right, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.rect.width = width
        self.rect.height = height
        self.jumping = False  # 添加这一行
        self.on_brick = False
        self.on_pipe = False  # 添加这一行
        self.velocity_y = 0  # 添加这一行
    
    def collide_with_brick(self, bricks):
        colliding = False
        self.on_brick = False
        for brick in bricks:
            if self.rect.colliderect(brick.rect):
                colliding = True
                # 从上方碰撞
                if self.velocity_y >= 0 and self.rect.bottom <= brick.rect.top + 5:
                    self.on_brick = True
                    self.jumping = False
                    self.velocity_y = 0
                    self.rect.bottom = brick.rect.top
                # 从下方碰撞
                elif self.rect.colliderect(brick.rect) and self.velocity_y < 0:
                    self.rect.top = brick.rect.bottom
                    all_sprites.remove(brick)
                    self.velocity_y = 0
                    return True
                # 从左侧碰撞
                elif self.rect.right >= brick.rect.left and self.rect.left < brick.rect.left:
                    self.rect.right = brick.rect.left
                # 从右侧碰撞
                elif self.rect.left <= brick.rect.right and self.rect.right > brick.rect.right:
                    self.rect.left = brick.rect.right
        self.on_brick = colliding

    def collide_with_pipe(self, pipes):
        colliding = False
        self.on_pipe = False
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                colliding = True
                # 从上方碰撞
                if self.velocity_y >= 0 and self.rect.bottom <= pipe.rect.top + 5:
                    self.on_pipe = True
                    self.jumping = False
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
        self.on_pipe = colliding


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.jumping or not self.on_pipe:
            self.rect.y += self.velocity_y
            self.velocity_y += 1
            if self.rect.y >= screen_height - 100:
                self.jumping = False
                self.rect.y = screen_height - 100
                self.velocity_y = 0

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.velocity_y = -18

# 砖块类
class Brick(pygame.sprite.Sprite):
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

#金币类
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_file):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (width, height))  # 缩放图像
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.rect.width = width
        self.rect.height = height
        self.velocity_y = -10
        self.value = 1

    def update(self):
        self.rect.y += self.velocity_y
        if self.velocity_y < 10:
            self.velocity_y += 1

# 创建玩家/水管/砖块
player = Player()
pipe = Pipe(561, 446, 50, 200, 'images/smallpipe.png')
big_pipe = Pipe(817, 420, 50, 200, 'images/bigpipe.png')
brick = Brick(255, 394, 50, 50, 'images/coinbrick.png')
all_sprites = pygame.sprite.Group()
all_sprites.add(player, pipe, big_pipe, brick)

# 游戏循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    bricks = [brick]
    #player.collide_with_brick(bricks)

    if player.collide_with_brick(bricks):
        coin = Coin(brick.rect.x, brick.rect.y - 50, 30, 30, 'images/coin.png')
        all_sprites.add(coin)
        score += coin.value

    pipes = [pipe, big_pipe]
    player.collide_with_pipe(pipes)

    all_sprites.update()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    score_font = pygame.font.Font(pygame.font.get_default_font(), 30)
    score_text = score_font.render('Score:' + str(score), True, (255, 255, 0))
    screen.blit(score_text, (20, 20))
    pygame.display.flip()
    clock.tick(60)
