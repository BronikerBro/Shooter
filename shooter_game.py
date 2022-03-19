from pygame import *
from random import randint

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        fire_sound.set_volume(0.1)
        fire_sound.play()
        bullet = Bullet(img_bullet, self.rect.centerx - 7.5, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


lost = 0
kill = 0

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed



win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
mixer.init()
mixer.music.set_volume(0.05)
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()
font1 = font.Font(None, 30)
counter_lost = font1.render("Пропущено врагов: " + str(lost), True, (230, 45, 98))
counter_kill = font1.render("Убито врагов: " + str(kill), True, (230, 45, 98))
font2 = font.Font(None, 50)
monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    ship.fire()

    if not finish:
        keys = key.get_pressed()

        #if keys[K_SPACE]:
            #ship.fire()
        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        gruz200 = sprite.groupcollide(monsters, bullets, False, True)
        for g in gruz200:
            g.rect.x = randint(80, win_width - 80)
            g.rect.y = -50
            kill += 1
        privid_Kieva = sprite.spritecollide(ship, monsters, False)
        if lost >= 3:
            WorL = font2.render("Ви не змінили ситуацію =(", True, (255, 50, 30))
            window.blit(WorL, (150, 200))
            finish = True
        if kill >= 100:
            WorL = font2.render("Ви відбили наступ оккупантів", True, (230, 45, 98))
            window.blit(WorL, (150, 200))
            finish = True
        counter_lost = font1.render("Пропущено оккупантів: " + str(lost), True, (230, 45, 98))
        counter_kill = font1.render("Знищено оккупантів: " + str(kill), True, (122, 245, 0))
        window.blit(counter_lost, (50, 30))
        window.blit(counter_kill, (400, 30))
        for p in privid_Kieva:
            p.rect.x = randint(80, win_width - 80)
            p.rect.y = -50
            WorL = font2.render("Ви не змінили ситуацію =(", True, (255, 50, 30))
            window.blit(WorL, (150, 200))
            finish = True
        display.update()
    time.delay(50)
