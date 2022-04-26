from pygame import *

# класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


# класс-наследник для спрайта-врага (перемещается сам)
class Enemy(GameSprite):
    def update(self):
        if self.rect.y <= 280:
            self.side = "bottom"
        elif self.rect.y >= win_height - 85:
            self.side = "top"
        if self.side == "top":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed


# класс для спрайтов-препятствий
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height

        # картинка стены - прямоугольник нужных размеров и цвета
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))

        # каждый спрайт должен хранить свойство rect - прямоугольник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        # draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))


# Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("pictures/background.jpg"), (win_width, win_height))

# Персонажи игры:
player = Player('pictures/hero.png', 5, win_height - 80, 4)
monster = Enemy('pictures/cyborg.png', win_width - 220, 280, 2)
final = GameSprite('pictures/treasure.png', win_width - 120, win_height - 80, 0)

w1 = Wall(154, 205, 50, 100, 20, 350, 10)
w2 = Wall(154, 205, 50, 100, 480, 360, 10)
w3 = Wall(154, 205, 50, 100, 20, 10, 350)
w4 = Wall(154, 205, 50, 275, 130, 10, 350)
w5 = Wall(154, 205, 50, 450, 20, 10, 350)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

# музыка
mixer.init()
mixer.music.load('music/ocean.mp3')
mixer.music.play()

money = mixer.Sound('music/money.ogg')
kick = mixer.Sound('music/kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monster.update()

        player.reset()
        monster.reset()
        final.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()

        # Ситуация "Проигрыш"
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or \
                sprite.collide_rect(player,w2) or sprite.collide_rect(
                player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

        # Ситуация "Выигрыш"
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()

    display.update()
    clock.tick(FPS)
