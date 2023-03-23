from pygame import *
from random import randint
from time  import time as timer
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial.py', 36)


img_back = "namek.jpg" 
img_hero = "goku.png"
img_enemy = "friza.png"
img_bullet = "power.png"
img_asteroid = "asteroid.png"

score = 0 
lost = 0 
life = 3
max_lost = 3
goal = 10
rel_time = False
num_fire = 0

class Game(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,speed,size_x,size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        wind.blit(self.image, (self.rect.x, self.rect.y))


class Player(Game):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 550:
            self.rect.x += self.speed   
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 6, 100, 100)
        bullets.add(bullet)


ww = 700
wh = 500

wind = display.set_mode((ww,wh))
display.set_caption("shoot")
background = transform.scale(image.load(img_back), (ww,wh))
player = Player(img_hero, 5,wh - 80, 60, 100, 60)

class Enemy(Game):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > wh:
            self.rect.x = randint(80, ww - 80)
            self.rect.y = 0 
            lost = lost + 1


class Bullet(Game):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_asteroid, randint(90, ww - 80), -40, randint(9,20), 80,60)
    asteroids.add(asteroid)

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, ww - 80), -40, randint(3,6), 50,60)
    monsters.add(monster)

finish = False
game = True
clock = time.Clock()
fps = 60
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        wind.blit(background,(0,0))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        wind.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        wind.blit(text_lose, (10, 50))


        player.update()
        monsters.update() 
        asteroids.update()
        bullets.update()
        player.reset()
        monsters.draw(wind)
        bullets.draw(wind)
        asteroids.draw(wind)
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, ww - 80), -40, 10, 50,60)
            monsters.add(monster)

          
        if sprite.spritecollide(player,monsters,False) or sprite.spritecollide(player,asteroids,False):
            sprite.spritecollide(player,monsters,True) 
            sprite.spritecollide(player,asteroids,True)
            life = life - 1
        
        
        if life == 0 or lost >= max_lost:
            finish = True
            wind.blit(lose,(200, 200))

           
        if score >= goal:
            finish = True
            wind.blit(win,(100, 150))
       
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render("Wait",1,(150,0,0))
                wind.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (0,150,150)
        text_life = font1.render(str(life), 1,life_color)
        wind.blit(text_life, (650, 10))

       
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(2100)
        for i in range(1, 3):
            asteroid = Enemy(img_asteroid, randint(90, ww - 80), -40, randint(1,5), 80,60)
            asteroids.add(asteroid)
            
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, ww - 80), -40, randint(1,5), 50,60)
            monsters.add(monster)
    display.update()
    time.delay(50)


