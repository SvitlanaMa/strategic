import pygame
from lvls import *
from screeninfo import get_monitors
from random import randint
monitors = get_monitors()
for monitor in monitors:
    win_w , win_h = monitor.width,monitor.height
    print(monitor.width,monitor.height)
    exit
wall_group = pygame.sprite.Group()
tank_group = pygame.sprite.Group()
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
        window.blit(self.image, (self.rect.x - (camera.rect.x + camera.speed) ,self.rect.y - (camera.rect.y + camera.speed)))
bullets = []
class Camera():
    def __init__(self , x ,y , w, h , speed , player) :
        self.rect = pygame.Rect(x,y,w,h)
        self.speed = speed
        self.player = player
 #       self.move_rect = pygame.Rect(self.player.rect.x - 25 , player_1.rect.y - 25 , (self.rect.w / 50 * 4) , (self.rect.h / 50 * 4)  )
    def move(self):
 #           if not self.move_rect.colliderect(player_1.rect) :
            self.rect.x = self.player.rect.x - win_w/3
            self.rect.y = self.player.rect.y - win_h/2

class bullet(GameObject):
    def __init__(self, x, y, w, h, image , dx , dy):
        super().__init__(x, y, w, h, image)
        self.dx , self.dy = dx , dy
        bullets.append(self)
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
    def shoot(self) :
        self.cooldown -= 1
        if pygame.mouse.get_pressed()[0] and self.cooldown <= 0 : 
            self.cooldown = 50
            x2, y2 = pygame.mouse.get_pos()
            x2 += camera.rect.x
            y2 += camera.rect.y
            vect = pygame.Vector2(x2, y2) - pygame.Vector2(self.rect.x , self.rect.y)
            norm_vect = vect.normalize()*self.bul_speed
            dx , dy = int(norm_vect[0]) , int(norm_vect[1])
            bullet1 = bullet(self.rect.x , self.rect.y , 15,15 ,player_pict, dx , dy)




    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_d]:
          #  if  self.rect.x <=570 :
            self.rect.x += self.speed
            self.image = pygame.transform.rotate(self.image_const , 180)

            # if  self.direction > 178 and self.direction < 182:
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
            # else :
            #     self.direction += 2
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
        if k[pygame.K_a]:
#            if self.rect.x >= 0 :
            self.rect.x -= self.speed
            self.image = pygame.transform.rotate(self.image_const ,0)
            # if self.direction != 0 :
            #     self.direction -= 2
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
        if k[pygame.K_w] :
            self.rect.y -= self.speed
            self.image = pygame.transform.rotate(self.image_const ,270)
            # if  self.direction > 88 and self.direction < 92:
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
            # else:
            #     self.direction -= 2 
            #     self.image = pygame.transform.rotate(self.image_const ,self.direction)
        if  k[pygame.K_s] :
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
    def update(self):
        window.blit(self.image1, (self.rect.x - (camera.rect.x + camera.speed) ,self.rect.y - (camera.rect.y + camera.speed)))
        window.blit(self.image2, (self.rect.x - (camera.rect.x + camera.speed) ,self.rect.y - (camera.rect.y + camera.speed)))

player_pict = pygame.image.load("player_1.png")
base_pict = pygame.image.load("base.png")
base = GameObject(500,500,150,150,base_pict)

class enemy(tank):
    def __init__(self, x, y, w, h, image, image2, speed):
        super().__init__(x, y, w, h, image, image2, speed)
        self.x2, self.y2 = base.rect.x , base.rect.y
        vect = pygame.Vector2(self.x2, self.y2) - pygame.Vector2(self.rect.x , self.rect.y)
        norm_vect = vect.normalize()*self.speed
        self.dx , self.dy = int(norm_vect[0]) , int(norm_vect[1])

    def enemy_move(self):
        vect = pygame.Vector2(self.x2, self.y2) - pygame.Vector2(self.rect.x , self.rect.y)
        norm_vect = vect.normalize()*self.speed
        self.dx , self.dy = int(norm_vect[0]) , int(norm_vect[1])
        if not pygame.sprite.groupcollide(tank_group , wall_group , False , False):
            if not self.rect.colliderect(base.rect):
                self.rect.x += self.dx
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
tank_track1 = pygame.image.load("tank_track_1.png")
tank_track1 = tank_track1.convert_alpha()
tank_corp1 = pygame.image.load("tank_corp_1.png")
tank_corp1 = tank_corp1.convert_alpha()
player_1 = player(400,500,50,50,5 , player_pict , 5 , 50 ) 
tank1 = tank(300,300,50,50,tank_track1 , tank_corp1 , 5)
tank2 = enemy(randint(0,win_w),randint(0,win_h),50,50,tank_track1 , tank_corp1 , 5)
game = True
blocks = []
x,y = 0,0
FPS = 120
block_w , block_h = int(win_w/50) , int(win_h/45)
for bl in lvl1 :
    for l in bl:
        if l == "0":
            block = GameObject(x,y,block_w,block_h,bl_winter_pict_1)
            blocks.append(block)
        if l == "1":
            block = GameObject(x,y,block_w,block_h,bl_winter_pict_2)
            wall_group.add(block)
            blocks.append(block)
        if l == "3":
            block = GameObject(x,y,block_w,block_h,bl_winter_pict_3)
            blocks.append(block)
        x += block_w
    y += block_h
    x = 0       
camera = Camera(0,0,win_w,win_h , 4 , player_1)
while game  :
    window.fill((0,0,0))
    for block in blocks :
        if block.rect.colliderect(camera.rect) :
            block.update()
    base.update()
    player_1.update()
    player_1.move()
    camera.move()
    player_1.shoot()
    tank2.enemy_move()
    tank2.update()
    print(tank2.dx , tank2.dy)
   # print(tank2.rect.x , tank2.rect.y)
    for bullet1 in bullets :
        bullet1.move()
        bullet1.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            game = False
            # if event.type == pygame.KEYDOWN and pygame.K_a:
            #     player_1.rect.x -= 5
    pygame.display.update()
    clock.tick(FPS)


    #https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
    #class Player(GameSprite): #переделать под 2й
#     def __init__(self, x, y, width, height, color
#         self.vect = pygame.Vector2(x, y)
#         self.x2 = x
#         self.y2 = y
#     def move(self):
#         if pygame.mouse.get_pressed()[0]:
#             self.x2, self.y2 = pygame.mouse.get_pos()
#         if self.x2 != self.rect.x or self.y2 != self.rect.y:
#             vect = pygame.Vector2(self.x2, self.y2) - sel
# if self.x2 != self.rect.x or self.y2 != self.rect.y:
#             vect = pygame.Vector2(self.x2, self.y2) - self.vect
#             if vect.length() < self.speed:
#                 self.rect.x, self.rect.y = self.x2, self.y2
#                 self.vect = vect #pygame.Vector2(self.x2, self.y2)
#             else:, speed):
#         super().__init__(x, y, width, height, color)
#         self.speed = speed 
#                 norm_vect = vect.normalize()*self.speed
#                 self.rect.x += int(norm_vect[0])
#                 self.rect.y += int(norm_vect[1])
#                 self.vect = pygame.Vector
# else:
#                 norm_vect = vect.normalize()*self.speed
#                 self.rect.x += int(norm_vect[0])
#                 self.rect.y += int(norm_vect[1])
#                 self.vect = pygame.Vector2(self.rect.x, self.rect.y)