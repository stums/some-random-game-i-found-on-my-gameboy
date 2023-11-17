# Import Modules
from pygame import *
from random import *
from time import time as timer
# Constant Variables
WIDTH, HEIGHT = 700, 500

# Game Settings
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("The Invasion of Mars")
background = transform.scale(image.load("galaxy.jpg"),(WIDTH,HEIGHT))





life1 = 3
life2 = 3
# Font
font.init()
style = font.SysFont("verdana", 30)
style2 = font.SysFont("verdana", 80)
congrat_p1 = style.render("Congratulations Player 1, You win!",True,(255,255,255))
congrat_p2 = style.render("Congratulations Player 2, You win!",True,(255,255,255))

# Music
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

gun_sound = mixer.Sound("fire.ogg")


bullet_one = transform.rotate(image.load("bullet.png"), 270)
bullet_two = transform.rotate(image.load("bullet.png"), 90)

###########################################################
# Parent Class
class SpriteClass(sprite.Sprite):
    def __init__(self, img, x, y, w, h, s):
        self.image = transform.scale(img,(w, h))
        self.rect = self.image.get_rect().inflate(-30,-30)
        self.rect.x = x
        self.rect.y = y
        self.speed = s
        
    def display(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
   
class Players(SpriteClass):
    def controls_one(self):
        keys = key.get_pressed()  
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < HEIGHT - 100:
            self.rect.y += self.speed
            
    def shoot_one(self):
        bullet1 = Bullet(bullet_one, self.rect.right, self.rect.centery, 50,15, 80)   
        player_one_bullets.add(bullet1)   
            
            
    def controls_two(self):
        keys = key.get_pressed()  
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < HEIGHT - 100:
            self.rect.y += self.speed
            
    def shoot_two(self):
        bullet2 = Bullet(bullet_two, self.rect.left, self.rect.centery, 50,15, 80)   
        player_two_bullets.add(bullet2)
    
  
class Bullet(sprite.Sprite):
    def __init__(self, img, x, y, w,h ,s):
        super().__init__()
        self.image = transform.scale(img, (w,h))
        self.rect = self.image.get_rect().inflate(-30,-30)
        self.rect.x = x
        self.rect.y = y
        self.speed = s
        
    def bullet_to_right(self):
        self.rect.x += self.speed
        if self.rect.x >= WIDTH:
            self.kill()
            
    def bullet_to_left(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()
        
class Asteroid(sprite.Sprite):
    def __init__(self,img,x,y,w,h,s):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect().inflate(-30,-30)
        self.rect.x = x
        self.rect.y = y
        self.speed = s

    def asteroid_left_to_right(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.rect.x = -50
            self.rect.y = randint(0,HEIGHT)


    def asteroid_right_to_left(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.x = WIDTH + 50
            self.rect.y = randint(0,HEIGHT)

    
# Create Objects
player_one = Players(transform.rotate(image.load("image-removebg-preview.png"),0), 50, HEIGHT/2, 130,100,20)
player_two = Players(transform.rotate(image.load("stuf-removebg-preview.png"),0), 450, HEIGHT/2, 130,100,20)


player_one_bullets = sprite.Group()
player_two_bullets = sprite.Group()
asteroids_to_right = sprite.Group()
asteroids_to_left = sprite.Group()

for i in range(1,1):
    asteroid_to_right = Asteroid("asteroid.png",0-50,randint(0,HEIGHT),50,50,randint(1,5))
    asteroid_to_left = Asteroid("asteroid.png",WIDTH+50,randint(0,HEIGHT),50,50,randint(1,5))
    asteroids_to_right.add(asteroid_to_right)
    asteroids_to_left.add(asteroid_to_left)
# Game Loop
p1_fire = 0
p2_fire = 0
reloader1 = False
reloader2 = False

run = True
end = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
            
        if e.type == KEYDOWN:
            if e.key == K_m:
                if p2_fire < 10 and reloader2 == False:
                    p2_fire += 1
                    player_two.shoot_two()
                    gun_sound.play()
                if p2_fire >= 10 and reloader2 == False:
                    reloader2 = True
                    start_time2 = timer()
            if e.key == K_z:
                if p1_fire < 10 and reloader1 == False:
                    p1_fire += 1    
                    player_one.shoot_one()
                    gun_sound.play()
                if p1_fire >= 10 and reloader1 == False:
                    reloader1 = True
                    start_time1 = timer()


    if end != True:

        screen.blit(background, (0,0))
        player_one.display()
        player_two.display()
        
        
        for bullet in player_one_bullets:
            bullet.bullet_to_right()
            
        for bullet in player_two_bullets:
            bullet.bullet_to_left()
        
        for quoc_anh in asteroids_to_left:
            quoc_anh.asteroid_right_to_left()

        for quoc_anh in asteroids_to_right:
            quoc_anh.asteroid_left_to_right()

        asteroids_to_left.draw(screen)
        asteroids_to_right.draw(screen)

        player_one_bullets.draw(screen)
        player_two_bullets.draw(screen)
        
        if reloader1 == True:
            current1 = timer()
            if current1 - start_time1 <5:
                reload_text = style.render("Reloading...",1,(250,10,10))
                screen.blit(reload_text,(10,HEIGHT -70))
            else:
                p1_fire = 0
                reloader1 = False

        if reloader2 == True:
            current2 = timer()
            if current2 - start_time2 <5:
                reload_text2 = style.render("Reloading...",1,(250,10,10))
                screen.blit(reload_text2,(550,HEIGHT -70))
            else:
                p2_fire = 0
                reloader2 = False

                
        
        player_one.controls_one()
        player_two.controls_two()

        if life1 == 0:
            end = True
            screen.blit(congrat_p2,(WIDTH / 4, HEIGHT / 4))

        if life2 == 0:
            end = True
            screen.blit(congrat_p1,(WIDTH / 4, HEIGHT / 4))

        if sprite.spritecollide(player_one,asteroids_to_left,True) or sprite.spritecollide(player_one,player_two_bullets,True):
            life1 -= 1

        if sprite.spritecollide(player_two,asteroids_to_right,True) or sprite.spritecollide(player_two,player_one_bullets,True):
            life2 -= 1

        if life1 == 3:
            life_color = (0,150,0)
        if life1 == 2:
            life_color = (150,150,0)
        if life1 == 1:
            life_color = (150,0,0)

        if life2 == 3:
            life2_color = (0,150,0)
        if life2 == 2:
            life2_color = (150,150,0)
        if life2 == 1:
            life2_color = (150,0,0)


        

        p1_life = style2.render(str(life1),True,life_color)
        screen.blit(p1_life,(50,50))
        p2_life = style2.render(str(life2),True,life2_color)
        screen.blit(p2_life,(650,50))
        display.update()
        
    else:
        end = False
        player_one = Players(transform.rotate(image.load("image-removebg-preview.png"),0), 50, HEIGHT/2, 130,100,20)
        player_two = Players(transform.rotate(image.load("stuf-removebg-preview.png"),0), 450, HEIGHT/2, 130,100,20)

        for b in player_one_bullets:
            b.kill()
        for b in player_two_bullets:
            b.kill()

        for a in asteroids_to_left:
            a.kill()
        for a in asteroids_to_right:
            a.kill()

        for i in range(1,1):
            asteroid_to_right = Asteroid("asteroid.png",0-50,randint(0,HEIGHT),50,50,randint(5,20))
            asteroid_to_left = Asteroid("asteroid.png",WIDTH+50,randint(0,HEIGHT),50,50,randint(5,20))
            asteroids_to_right.add(asteroid_to_right)
            asteroids_to_left.add(asteroid_to_left)

        life1 = 3
        life2 = 3
        p1_fire = 0
        p2_fire = 0


        time.delay(2000)
    
    time.delay(50)