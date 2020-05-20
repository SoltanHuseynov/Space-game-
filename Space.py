#windows
win_width=500
win_height=500
#jet
jet_width=50
jet_height=50
#metor
metor_width=30
metor_height=30

#windows color
black=(0,0,0)

#metor FBS
FBS=30

#bullet
bullet_width=10
bullet_height=20


import os
system=os.getcwd()
metor1=system+"\\game_image\\metor1.png"
metor2=system+"\\game_image\\metor2.png"
jet=system+"\\game_image\\jet.png"
bullet12=system+"\\game_image\\bullet.png"
bullet_song=system+"\\game_song\\bullet_song.ogg"
bullet_attac=system+"\\game_song\\bullet_attac.ogg"
space_song=system+"\\game_song\\space_song.mp3"
import pygame
import random
import time

pygame.init()
pygame.mixer.init()
clock=pygame.time.Clock()
metor=[pygame.image.load(metor1),pygame.image.load(metor2)]
windows=pygame.display.set_mode((win_width,win_height))

    

class Enemiys(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=metor[0].convert()
        self.image.set_colorkey(black)
        self.image=pygame.transform.scale(self.image,(metor_width,metor_height))
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(win_width-self.rect.x)
        self.rect.y=random.randrange(-100,-40)
        self.imagey=random.randrange(1,15)
    def update(self):
        self.rect.y+=self.imagey
        if self.rect.y > win_height:
            self.rect.x=random.randrange(win_width-self.rect.x)
            self.rect.y=random.randrange(-100,-50)
            self.imagey=random.randrange(1,15)
    def update1(self):
        liste=random.randint(1,5)
        if liste ==3 or liste == 2:
            self.image=metor[1].convert()
            self.image.set_colorkey(black)
            self.image=pygame.transform.scale(self.image,(metor_width,metor_height))

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load(bullet12).convert()
        self.image.set_colorkey(black)
        self.image=pygame.transform.scale(self.image,(bullet_width,bullet_height))
        self.rect=self.image.get_rect()
        self.rect.x=x+20
        self.rect.y=y
        self.speedy=-10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y <0:
            self.kill()
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(jet).convert()
        self.image.set_colorkey(black)
        self.image=pygame.transform.scale(self.image,(jet_width,jet_height))
        self.rect=self.image.get_rect()
        self.rect.x=250
        self.rect.y=450
    def update(self):
        Key=pygame.key.get_pressed()
        if Key[pygame.K_d]:
            if self.rect.x < win_width -50:
               self.rect.x+=10
        if Key[pygame.K_a]:
            if self.rect.x > 0:
               self.rect.x-=10
        if Key[pygame.K_SPACE]:
            if self.rect.y >400:
               self.rect.y -=20
            else: 
                if self.rect.y < 400:
                    self.rect.y=450

    def shuot(self):
        bullet=Bullet(self.rect.x,self.rect.y)
        all_player.add(bullet)
        all_bullet.add(bullet)

def quit_update():
    for quit in pygame.event.get():
        if quit.type==pygame.QUIT:
            exit()

all_enemiy=pygame.sprite.Group()
all_bullet=pygame.sprite.Group()
all_player=pygame.sprite.Group()

player=Player()
all_player.add(player)

for i in range(random.randrange(1,30)):
    enemiy=Enemiys()
    all_player.add(enemiy)
    all_enemiy.add(enemiy)
    

#score setting
scor=0
scorfont=pygame.font.SysFont("monospace",20)
def scor_update():
    global scor,scorfont,bell,bellfont,bullet_song,enemiy

    crap1=pygame.sprite.groupcollide(all_enemiy,all_bullet,True,True)
    if crap1:
        pygame.mixer.music.load(bullet_song)
        pygame.mixer.music.play()
        scor+=1
        if scor  >=10:
            enemiy.update1()
    scortext=scorfont.render("Scor:"+str(scor),1,(255,0,0))
    windows.blit(scortext,(0,0))
    for s in crap1:
        enemiy=Enemiys()
        all_player.add(enemiy)
        all_enemiy.add(enemiy)

#bell setting
bell=10
bellfont=pygame.font.SysFont("monospace",20)
def bell_update():
    global bell,bellfont,windows,enemiy,scor
    carp2=pygame.sprite.spritecollide(player,all_enemiy,True)
    if carp2:
        bell -=1
        if bell <=0:
            time.sleep(0.5)
            exit()
    
    belltext=bellfont.render("Bell:"+str(bell),1,(255,0,0))
    windows.blit(belltext,(400,0))
    for z in carp2:
        enemiy=Enemiys()
        all_player.add(enemiy)
        all_enemiy.add(enemiy)
    
def quit_update():
    global bullet_attac
    for quit in pygame.event.get():
        if quit.type==pygame.QUIT:
            exit()
        if quit.type==pygame.MOUSEBUTTONUP:
            pygame.mixer.music.load(bullet_attac)
            pygame.mixer.music.play()
            player.shuot()

while True:
    windows.fill(black)

    quit_update()
    clock.tick(FBS)
    #player
    all_player.update()

    all_player.draw(windows)
    #scor
    scor_update()
    #bell
    bell_update()

    pygame.display.update()

