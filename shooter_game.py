from pygame import *
from random import randint
import math

win_width = 700
win_height = 500
win = display.set_mode((win_width, win_height))

backgroundd = transform.scale(image.load('city.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('city.mp3')
mixer.music.play()

wind_s = mixer.Sound('wind.wav')

firere = mixer.Sound('hit.mp3')

bullets = sprite.Group()

lost = 0
score = 0
life = 3

font.init()
font1 = font.SysFont('Arial', 36)

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, speed, ggimage, growx, growy):
        super().__init__()
        self.image = transform.scale(image.load(ggimage), (growx, growy))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    lastfire = 0
    slow = 300 
    lastspeedup = 0
    bro_stop = 1000
    speeding = 100
    def update(self):
        keys = key.get_pressed()
        off_set = 5
        left = keys[K_LEFT]
        if self.rect.x > off_set and left:
            self.rect.x -= self.speed
        right = keys[K_RIGHT]
        if self.rect.x < win_width - 65 - off_set and right:
            self.rect.x += self.speed
        firerere = keys[K_SPACE]
        if firerere:
            nowtime = time.get_ticks()
            if nowtime - self.lastfire >= self.slow:
                self.lastfire = nowtime
                firere.play()
                self.fire()
        shiftt = keys[K_LSHIFT]
        if shiftt:
            if right:
                self.speed_up_right(1)
            elif left:
                self.speed_up_right(-1)

    def speed_up_right(self, napravlenie):
        nowtime = time.get_ticks()
        if nowtime - self.lastspeedup >= self.bro_stop:
            self.lastspeedup = nowtime
            stops = self.rect.x + napravlenie * self.speeding
            if stops < win_width and stops > 0:
                self.rect.x = stops
                self.lastspeedup = nowtime
            else:
                pass


    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 15, 'bullet.png', 7, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__ (self, *args):
        super().__init__(*args)
        self.ugol = 0
        self.start_tochka = self.rect.x
    def update(self):
        self.rect.y += self.speed
        self.ugol += 0.03
        self.rect.x = self.start_tochka + int(math.sin(self.ugol) * 10)
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(50, win_width - 50)
            lost = lost + 1
            wind_s.play()
        

class Asters(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(50, win_width - 50)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

        

space_ship = Player(285, 420, 9, 'rocket.png', 65, 80)
angry_dudes = sprite.Group()
for i in range(5):
    very_evil_dude = Enemy(randint(50, win_width - 50), 0, randint(1, 3), 'ufo.png', 80, 50)
    angry_dudes.add(very_evil_dude)
asters = sprite.Group()
for i in range(3):
    aster = Asters(randint(50, win_width - 50), 0, randint(1, 3), 'asteroid.png', 80, 50)
    asters.add(aster)

game = True
finish = False

FPS = 60

clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        win.blit(backgroundd, (0, 0))
        space_ship.update()
        space_ship.reset()
        bullets.update()
        bullets.draw(win)
        angry_dudes.update()
        angry_dudes.draw(win)
        if score >= 30:
            asters.update()
            asters.draw(win)
        loser = font1.render("Пропустил: " + str(lost), 1, (100, 100, 100))
        win.blit(loser, (5, 40))
        winner = font1.render("Счет: " + str(score), 1, (100, 100, 100))
        win.blit(winner, (5, 40 - 30))
        if life == 3:
            mrt = font1.render("Исправность: " + str(life), 1, (0, 255, 0))
        if life == 2:
            mrt = font1.render("Исправность: " + str(life), 1, (255, 255, 0))
        if life == 1:
            mrt = font1.render("Исправность: " + str(life), 1, (255, 0, 0))
        win.blit(mrt, (5, 70))
        sprites_list = sprite.groupcollide(angry_dudes, bullets, True, True)
        for e in sprites_list:
            new_dude = Enemy(randint(50, win_width - 50), 0, randint(1, 3), 'ufo.png', 80, 50)
            angry_dudes.add(new_dude)
            score += 1
        
        if sprite.spritecollide(space_ship, asters, False) or sprite.spritecollide(space_ship, angry_dudes, False):
            life -= 1
            sprite.spritecollide(space_ship, asters, True)
            sprite.spritecollide(space_ship, angry_dudes, True)

        if score >= 40:
            yay = font1.render("Ты победил", 1, (0, 255, 0))
            win.blit(yay, (win_width - 425, 200))
            finish = True

        if lost >= 3 or life == 0:
            noo = font1.render("Ты проиграл", 1, (255, 0, 0))
            win.blit(noo, (win_width - 425, 200))
            finish = True


        display.update()
        clock.tick(FPS)

    else:
        for e in angry_dudes:
            e.kill()
        for e in bullets:
            e.kill()
        time.delay(2000)
        for i in range(5):
            very_evil_dude = Enemy(randint(50, win_width - 50), 0, randint(1, 3), 'ufo.png', 80, 50)
            angry_dudes.add(very_evil_dude)
        score = 0
        lost = 0
        life = 3
        finish = False


























