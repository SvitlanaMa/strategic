import pygame
from lvls import *
import heapq
from time import time
from screeninfo import get_monitors
from random import randint
monitors = get_monitors()
for monitor in monitors:
    win_w , win_h = monitor.width,monitor.height
    print(monitor.width,monitor.height)
    exit
wall_group = pygame.sprite.Group()
tank_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
pygame.init()
#win_w , win_h = 900,820 #block = 18,18 | 106.6 , 60
clock = pygame.time.Clock()
window = pygame.display.set_mode((win_w,win_h))
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image,): 
        super().__init__()
        self.rect = pygame.Rect(x,y,w,h)
        self.image = pygame.transform.scale(image,(w,h))
    def update(self):
        window.blit(self.image, (self.rect.x - camera.rect.x  ,self.rect.y - camera.rect.y ))
bullets = []
iron_count = 0 
class Game_pict() :
    def __init__(self,x,y,w,h,image) :
        self.rect = pygame.Rect(x,y,w,h)
        self.image = pygame.transform.scale(image,(w,h))
    def update(self):
        window.blit(self.image, (self.rect.x  ,self.rect.y ))
bur_list = []
class bur(GameObject):
    def __init__(self, x, y, w, h, image):
        super().__init__(x, y, w, h, image)
        bur_list.append(self)
    def g_iron(self ):
        global iron_count
        iron_count += 1
class Camera():
    def __init__(self , x ,y , w, h , speed , player) :
        self.rect = pygame.Rect(x,y,w,h)
        self.speed = speed
        self.player = player
 #       self.move_rect = pygame.Rect(self.player.rect.x - 25 , player_1.rect.y - 25 , (self.rect.w / 50 * 4) , (self.rect.h / 50 * 4)  )
    def move_right(self):
 #           if not self.move_rect.colliderect(player_1.rect) :
            self.rect.x += player_1.speed
    def move_left(self):
        self.rect.x -= player_1.speed
    def move_up(self):
        self.rect.y -= player_1.speed
    def move_down(self):
        self.rect.y += player_1.speed
            #print(self.rect.x , self.rect.y)
class bullet(GameObject):
    def __init__(self, x, y, w, h, image , dx , dy):
        super().__init__(x, y, w, h, image)
        self.dx , self.dy = dx , dy
        bullets.append(self)
        bullets_group.add(self)
        self.i = 0
    def move(self):
        distanse = 150
        if self.i <= distanse :
            self.rect.x += self.dx
            self.rect.y += self.dy
            self.i += 1
        else :
            i = 0 
            bullets.remove(self)
class player(GameObject):
    def __init__(self, x, y, w, h,speed ,  image , bul_speed , shoot_cooldown):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.bul_speed = bul_speed
        self.image_const = pygame.transform.scale(image , (self.rect.w , self.rect.h))
        self.direction = 0
        self.images = []
        self.cooldown = shoot_cooldown
        self.chose_bur = False
    def shoot(self) :
        self.cooldown -= 1
        if pygame.mouse.get_pressed()[2] and self.cooldown <= 0 : 
            self.cooldown = 50
            x2, y2 = pygame.mouse.get_pos()
            x2 += camera.rect.x
            y2 += camera.rect.y
            vect = pygame.Vector2(x2, y2) - pygame.Vector2(self.rect.x , self.rect.y)
            norm_vect = vect.normalize()*self.bul_speed
            dx , dy = int(norm_vect[0]) , int(norm_vect[1])
            bullet1 = bullet(self.rect.x , self.rect.y , 15,15 ,bullet_pict, dx , dy)
    def chose(self):
        x , y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and bur_but.rect.collidepoint(x , y):
            self.chose_bur = True
    def build_bur(self):
        x , y = pygame.mouse.get_pos()
        block_bur = bur(x , y , 45 , 45 ,bur_pict)
    def blit(self):
        if self.chose_bur :
            x3 , y3 = pygame.mouse.get_pos()
            print(x3,y3)
            window.blit(pygame.transform.scale(bur_pict, (45,45)),( x3, y3 ))
            if pygame.mouse.get_pressed()[0] :
                for iron in ore_list:
                    if iron.rect.collidepoint(x3 + camera.rect.x,y3 + camera.rect.y):
                        print(x3 , y3 , )
                        print(x3 + (camera.rect.x - win_w/ 3 - player_1.rect.x ), y3 + camera.rect.y )
                        block_bur = bur(x3 + camera.rect.x, y3  + camera.rect.y, 45 , 45 ,bur_pict)
                        self.chose_bur = False

        


    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_d]:
          #  if  self.rect.x <=570 :
            self.rect.x += self.speed
            self.image = pygame.transform.rotate(self.image_const , 180)
            camera.move_right()
            # if  self.direction > 178 and self.direction < 182:
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
            # else :
            #     self.direction += 2
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
        if k[pygame.K_a]:
            camera.move_left()
#            if self.rect.x >= 0 :
            self.rect.x -= self.speed
            self.image = pygame.transform.rotate(self.image_const ,0)
            # if self.direction != 0 :
            #     self.direction -= 2
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
        if k[pygame.K_w] :
            camera.move_up()
            self.rect.y -= self.speed
            self.image = pygame.transform.rotate(self.image_const ,270)
            # if  self.direction > 88 and self.direction < 92:
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
            # else:
            #     self.direction -= 2 
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
        if  k[pygame.K_s] :
            camera.move_down()
            self.rect.y += self.speed
            self.image = pygame.transform.rotate(self.image_const ,90)
            # if  self.direction > 268 and self.direction < 272:
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
            # else :
            #     self.direction += 2 
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
soldiers = []
class tank(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image ,image2 ,speed):
        self.rect = pygame.Rect(x,y,w,h)
        self.speed = speed
        self.image1 = pygame.transform.scale(image ,( w,h))
        self.image2 = pygame.transform.scale(image2 , (w , h ))
        super().__init__()
        tank_group.add(self)
    # def draw(self):
    #     window.blit(self.image1, (self.rect.x - (camera.rect.x + camera.speed) ,self.rect.y - (camera.rect.y + camera.speed)))
    #     window.blit(self.image2, (self.rect.x - (camera.rect.x + camera.speed) ,self.rect.y - (camera.rect.y + camera.speed)))

player_pict = pygame.image.load("player_1.png")
base_pict = pygame.image.load("base.png")
base = GameObject(500,500,150,150,base_pict)
tank_list = []
class enemy(tank):
    def __init__(self, x, y, w, h, image, image2, speed , hp):
        super().__init__(x, y, w, h, image, image2, speed)
        self.hp = hp
        self.x2, self.y2 = base.rect.x , base.rect.y
        vect = pygame.Vector2(self.x2, self.y2) - pygame.Vector2(self.rect.x , self.rect.y)
        norm_vect = vect.normalize()*self.speed
        self.dx , self.dy = int(norm_vect[0]) , int(norm_vect[1])
        self.collide_left = False
        self.collide_right = False
        self.collide_up = False
        self.collide_down = False
        tank_list.append(self)
    def update(self):
        window.blit(self.image1, (self.rect.x - (camera.rect.x + camera.speed) ,self.rect.y - (camera.rect.y + camera.speed)))
        window.blit(self.image2, (self.rect.x - (camera.rect.x + camera.speed) ,self.rect.y - (camera.rect.y + camera.speed)))
    def hp_check(self) :
        if self.hp <= 0 :
            tank_group.remove(self) 
            tank_list.remove(self)
        if pygame.sprite.groupcollide(tank_group , bullets_group , False , True) :
            self.hp -= 1
            print(1)
            print(self.hp)
    def find_rode (self):
        if self.collide_left :
            self.x2, self.y2 = self.rect.x , self.rect.y + 32
            vect = pygame.Vector2(self.x2, self.y2) - pygame.Vector2(self.rect.x , self.rect.y)
            norm_vect = vect.normalize()*self.speed
            self.dx , self.dy = int(norm_vect[0]) , int(norm_vect[1])
            return self.dx , self.dy
    def find_base(self):
        self.x2 , self.y2 = base.rect.x , base.rect.y 
        vect = pygame.Vector2(self.x2, self.y2) - pygame.Vector2(self.rect.x , self.rect.y)
        norm_vect = vect.normalize()*self.speed
        self.dx , self.dy = int(norm_vect[0]) , int(norm_vect[1])
        return self.dx , self.dy
    def try_left (self):
        self.rect.x -= 8
        if not pygame.sprite.groupcollide(wall_group , tank_group , False , False) :
            self.collide_left = False
            return self.collide_left
        else: self.rect.x += 8
    def enemy_move(self):
        if pygame.sprite.groupcollide(tank_group , wall_group , False, False) :
            for i in wall_list:
                if i.rect.colliderect(self.rect) :
                    if self.rect.x > i.rect.x :
                        self.collide_left = True
        self.find_base()
        if self.collide_left == True:
            self.find_rode()
            self.try_left()
        if not self.rect.colliderect(base.rect):
            if not self.collide_left :
                self.rect.x += self.dx
            else : self.rect.x -= self.dx
            if not self.collide_up :
                self.rect.y += self.dy
        else :
            self.rect.x = randint(0,win_w)
            self.rect.y = randint(0,win_h)
            if pygame.sprite.groupcollide(tank_group , wall_group , False , False):
                pass
bl_winter_pict_1 = pygame.image.load("block_winter_3.png")
bl_winter_pict_1 = bl_winter_pict_1.convert_alpha()
bl_winter_pict_2 = pygame.image.load("block_winter_1.png")
bl_winter_pict_2 = bl_winter_pict_2.convert_alpha()
bl_winter_pict_3 = pygame.image.load("block_winter_4.png")
bl_winter_pict_3 = bl_winter_pict_3.convert_alpha()
bur_pict = pygame.image.load("bur.png")
bur_build_pict = bur_pict.set_alpha(65)
ore_bl_pict = pygame.image.load("ore_bl.png")
info_pict = pygame.image.load("info_pict.png")
info_pict.set_alpha(150)
iron_pict = pygame.image.load("iron.png")
tank_track1 = pygame.image.load("tank_track_1.png")
tank_track1 = tank_track1.convert_alpha()
tank_corp1 = pygame.image.load("tank_corp_1.png")
tank_corp1 = tank_corp1.convert_alpha()
bullet_pict = pygame.image.load("bullet.png")
font = pygame.font.SysFont("Arial",30)
font1 = pygame.font.SysFont("Arial",20)
player_1 = player(400,500,50,50,5 , player_pict , 5 , 50 ) 
tank1 = enemy(800,500,50,50,tank_track1 , tank_corp1 , 5, 3)
game = True
blocks = []
x,y = 0,0
FPS = 120
bur_but = Game_pict(win_w - 150 , win_h - 150 , 35,35, bur_pict)
block_w , block_h = int(win_w/50) , int(win_h/45)
wall_list = []
if tank1.rect.colliderect(player_1.rect) :
    a = tank1.rect.clip(player_1.rect)
ore_list = []
for bl in lvl1 :
    for l in bl:
        if l == "0":
            block = GameObject(x,y,block_w,block_h,bl_winter_pict_1)
            blocks.append(block)
        if l == "1":
            block = GameObject(x,y,block_w,block_h,bl_winter_pict_2)
            wall_group.add(block)
            wall_list.append(block)
            blocks.append(block)
        if l == "2" :
            block = GameObject(x,y,block_w,block_h,ore_bl_pict)
            ore_list.append(block)
            blocks.append(block)
        if l == "3":
            block = GameObject(x,y,block_w,block_h,bl_winter_pict_3)
            blocks.append(block)
        x += block_w
    y += block_h
    x = 0       
camera = Camera(0,0,win_w,win_h , 4 , player_1)
start_time = time()
while game  :
    game_time = int(time() - start_time)
    time_lb = font.render(f"Час{game_time}", True , (255,255,255))
    window.fill((0,0,0))
    for block in blocks :
        if block.rect.colliderect(camera.rect) :
            block.update()
    for bur1 in bur_list:
        bur1.update()
        bur1.g_iron()
    base.update()
    player_1.update()
    player_1.chose()
    player_1.blit()
    player_1.move()
    player_1.shoot()
    for tank1 in tank_list :
        tank1.update()
        tank1.enemy_move()
        tank1.hp_check()
    window.blit(info_pict , (win_w/2 - 200 , 0))
    iron_lb = font1.render(f"Заліза {iron_count}", True , (255,255,255))
    window.blit(iron_pict , (win_w/2 - 109 , 20))
    window.blit(iron_lb , (win_w / 2 - 90 , 15))
    window.blit(time_lb,(win_w / 2 - 15 ,100))
    window.blit(pygame.transform.rotate(info_pict , 180), (win_w - 300 , win_h - 170))
    bur_but.update()
    #tank_group.enemy_move()
   # print(tank2.rect.x , tank2.rect.y)
    for bullet1 in bullets :
        bullet1.move()
        bullet1.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            game = False
             
    pygame.display.update()
    clock.tick(FPS)