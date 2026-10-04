#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, player_w, player_h):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(player_w, player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 20, self.rect.centerx, self.rect.top, 10, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global fail_enemy
        self.rect.y += self.speed
        if self.rect.y >= 520:
            self.rect.y = -10
            self.rect.x = randint(10,600)
            fail_enemy += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()



window = display.set_mode((700,500))
display.set_caption(" ")
background = transform.scale(image.load('galaxy.jpg'),(700,500))
mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()

clock = time.Clock()
font.init()
font_yay = font.SysFont('Arial', 38)

fail_enemy = 0
score = 0
failed = font_yay.render('Бебебе проиграл', False, (255, 255, 255))
hooray = font_yay.render('О нет выиграл((', False, (255, 255, 255))

player = Player('rocket.png', 10, 300, 410, 80, 80)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(1,5), randint(10, 600), -10, 70, 40)
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1,2):
    asteroid = Enemy('asteroid.png', randint(1,5), randint(10, 600), -10, 70, 40)
    asteroid.add(asteroids)
finish = False

reload_time = False
fire_num = 0
life = 4

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if fire_num <5 and reload_time == False:
                    fire_num+=1 
                    fire_sound.play()
                    player.fire()
                if fire_num >=5 and reload_time == False:
                    last_time = timer()
                    reload_time = True
    if not finish:
        window.blit(background,(0,0))

        TEXT_fail_enemy = font_yay.render('Missed:'+ str(fail_enemy), True, (255, 255, 255))
        TEXT_score = font_yay.render('Score:'+ str(score), True, (255, 255, 255))
        window.blit(TEXT_fail_enemy,(5,10))
        window.blit(TEXT_score,(5,52))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        collides = sprite.groupcollide( monsters, bullets, True, True)

        for c in collides:
            score = score+1
            monster = Enemy('ufo.png', randint(1,5), randint(10, 600), -10, 70, 40)
            monsters.add(monster)
        if sprite.spritecollide( player, monsters, False) or sprite.spritecollide( player, asteroids, False) or fail_enemy>=3:
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life -= 1
        if reload_time == True:
            now_time = timer()
            if now_time-last_time < 2:
                reload = font_yay.render('WAIT...RELOADING', True, (255, 255, 255))
                window.blit(reload ,(260,460))
            else: 
                fire_num = 0
                reload_time = False
        if score >= 10:
            finish = True
            window.blit(hooray, (230,300))
        if fail_enemy > 10 or life <= 0:
            finish = True
            window.blit(failed, (230,300))
        if life == 4:
            life_color = (34, 255, 0)
        if life == 3:
            life_color = (251, 255, 0)
        if life == 2:
            life_color = (255, 136, 0)
        if life == 1:
            life_color = (255, 0, 0)
        life_text = font_yay.render('Life:'+ str(life), True, life_color)
        window.blit(life_text,(5,94))
        display.update()

    else:
        finish = False
        fail_enemy = 0
        score = 0
        life = 4
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(1,5), randint(10, 600), -10, 70, 40)
            monsters.add(monster)
        
    time.delay(50)
    display.update()

    #TODO УУ ОРАНЖЕВЫЙЙ
