# -*- coding: utf-8 -*-
import pygame
import random
from settings import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    # 玩家类
    def __init__(self, game):
        # 初始化玩家
        super().__init__()
        self.game = game
        self.image = pygame.Surface((32,32))
        self.image = pygame.image.load("Sprites/chrA07.png").convert_alpha()
        self.rect = self.image.get_rect()    # 取得位置
        self.rect.topleft = vec(320,240)
        self.pos = vec(960,960)
        self.des = vec(960,960)
        self.count = 0
        self.vel = vec(0, 0)
        self.walking = 0
        self.battling = 0

        self.name = "Player"
        self.level = 1
        self.floor = 1
        self.maxHp = 10
        self.Hp = 10
        self.Atk = 2
        self.Def = 1
        self.Spd = 2
        self.Exp = 0
        self.nextExp = LEVEL_EXP[0]
        self.bag = Bag()

    def walk(self):
        keys = pygame.key.get_pressed()    # 获取输入
        w = self.game.map.width
        h = self.game.map.height
        if self.walking == 0:
            if keys[pygame.K_LEFT]:    # 左键
                left = vec(int(self.pos.x-GRID)>>GRID_SHIFT ,int(self.pos.y)>>GRID_SHIFT)
                if self.game.map.map[int(left.y%h)][int(left.x%w)] == 1:
                    self.des = self.pos - vec(32,0)
                    self.vel.x = -PLAYER_SPEED
                    self.walking = 1
            elif keys[pygame.K_RIGHT]:
                right = vec(int(self.pos.x+GRID)>>GRID_SHIFT ,int(self.pos.y)>>GRID_SHIFT)
                if self.game.map.map[int(right.y%h)][int(right.x%w)] == 1:
                    self.des = self.pos + vec(32,0)
                    self.vel.x = PLAYER_SPEED
                    self.walking = 1
            elif keys[pygame.K_UP]:    # 上键
                up = vec(int(self.pos.x)>>GRID_SHIFT ,int(self.pos.y-GRID)>>GRID_SHIFT)
                if self.game.map.map[int(up.y%h)][int(up.x%w)] == 1:
                    self.des = self.pos - vec(0,32)
                    self.vel.y = -PLAYER_SPEED
                    self.walking = 1
            elif keys[pygame.K_DOWN]:    # 下键
                down = vec(int(self.pos.x)>>GRID_SHIFT ,int(self.pos.y+GRID)>>GRID_SHIFT)
                if self.game.map.map[int(down.y%h)][int(down.x%w)] == 1:
                    self.des = self.pos + vec(0,32)
                    self.vel.y = PLAYER_SPEED
                    self.walking = 1
        if self.walking == 1:
            self.pos += self.vel
            self.count += PLAYER_SPEED
            if(self.count==GRID):
                self.walking = 0
                self.vel = vec(0, 0)
                self.count = 0

        #self.rect.topleft = self.pos

    def attack(self, target):
        p = random.randint(90, 110)
        damage = int((self.Atk - target.Def/2)* p/100)
        target.Hp -= damage
        #sound = pygame.mixer.Sound("D:/python/project/aa.wav")
        #sound.play()
        print("%s attacked %s, damage %d"%(self.name, target.name, damage))
        text = "%s攻击了%s，造成%d点伤害"%(self.name, target.name, damage)
        self.draw_text(text,32,WHITE,320,360)

    def levelup(self):
        self.Exp -= self.nextExp
        self.nextExp = LEVEL_EXP[self.level]
        self.level += 1
        self.maxHp += 5
        self.Hp = self.maxHp
        self.Atk += 2
        self.Def += 2
        self.Spd += 1

    def draw_text(self, text, size, color, x, y):
        info_back = pygame.Surface((620,160))
        info_back.fill(BLACK)
        self.game.screen.blit(info_back, (10,300))
        font_name = pygame.font.match_font(FONT_NAME)
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.game.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(1500)

    def update(self):
        # 更新玩家
        if self.battling == 0:
            self.walk()
        else:
            print(self.battling)

    def downstairs(self):
        self.floor += 1
        self.count = 0
        self.walking = 0
        self.vel = vec(0,0)

    def draw(self, screen):
        offset_x = self.game.camera.offset_x
        offset_y = self.game.camera.offset_y
        self.rect.left = self.pos.x-offset_x
        self.rect.top = self.pos.y-offset_y
        screen.blit(self.image, (self.rect.left, self.rect.top))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, number,game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((32,32))
        self.imageb = pygame.Surface((32,32))
        if number==0:
            self.image = pygame.image.load("Sprites/000_map.png").convert_alpha()
            self.imageb = pygame.image.load("Sprites/000.png").convert_alpha()
        elif number==1:
            self.image = pygame.image.load("Sprites/001_map.png").convert_alpha()
            self.imageb = pygame.image.load("Sprites/001.png").convert_alpha()
        elif number==2:
            self.image = pygame.image.load("Sprites/002_map.png").convert_alpha()
            self.imageb = pygame.image.load("Sprites/002.png").convert_alpha()
        elif number==3:
            self.image = pygame.image.load("Sprites/003_map.png").convert_alpha()
            self.imageb = pygame.image.load("Sprites/003.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = vec(160,288)
        self.pos = vec(928,896)
        self.chasing = 0
        self.walking = 0
        self.vel = vec(0,0)
        self.count = 0
        self.number = number
        self.name = MONSTER[number][0]
        self.level = MONSTER[number][1]
        self.Hp = MONSTER[number][2]
        self.Atk = MONSTER[number][3]
        self.Def = MONSTER[number][4]
        self.Spd = MONSTER[number][5]
        self.Exp = MONSTER[number][6]
        self.Gold = MONSTER[number][7]
        self.escaped = 0
        self.fly = 0

    def update(self):
        player = self.game.player
        distx = abs(player.pos.x - self.pos.x)
        disty = abs(player.pos.y - self.pos.y)
        if player.walking == 1 and distx <= 160 and disty <= 160:
            self.chasing = 1
        if self.chasing == 1:
            self.chase(player)

    def chase(self, player):
        if self.walking == 0:
            rand = random.randint(0,1)
            if self.fly == 1:
                if self.pos.x == player.des.x:
                    self.vel.y = self.sign(player.des.y, self.pos.y) * MONSTER_SPEED
                elif self.pos.y == player.des.y:
                    self.vel.x = self.sign(player.des.x, self.pos.x) * MONSTER_SPEED
                else:
                    if rand == 0:
                        self.vel.x = self.sign(player.des.x, self.pos.x) * MONSTER_SPEED
                    else:
                        self.vel.y = self.sign(player.des.y, self.pos.y) * MONSTER_SPEED

            else:
                w = self.game.map.width
                h = self.game.map.height
                if self.pos.x == player.des.x:
                    signy = self.sign(player.des.y, self.pos.y)
                    updown = vec(int(self.pos.x)>>GRID_SHIFT ,int(self.pos.y+signy*GRID)>>GRID_SHIFT)
                    if self.game.map.map[int(updown.y%h)][int(updown.x%w)] == 1:
                        self.vel.y = signy * MONSTER_SPEED
                        self.walking = 1
                    else:
                        self.chasing = 0
                elif self.pos.y == player.des.y:
                    signx = self.sign(player.des.x, self.pos.x)
                    leftright = vec(int(self.pos.x+signx*GRID)>>GRID_SHIFT ,int(self.pos.y)>>GRID_SHIFT)
                    if self.game.map.map[int(leftright.y%h)][int(leftright.x%w)] == 1:
                        self.vel.x = signx * MONSTER_SPEED
                        self.walking = 1
                    else:
                        self.chasing = 0
                else:
                    signx = self.sign(player.des.x, self.pos.x)
                    leftright = vec(int(self.pos.x+signx*GRID)>>GRID_SHIFT ,int(self.pos.y)>>GRID_SHIFT)
                    signy = self.sign(player.des.y, self.pos.y)
                    updown = vec(int(self.pos.x)>>GRID_SHIFT ,int(self.pos.y+signy*GRID)>>GRID_SHIFT)
                    if self.game.map.map[int(updown.y%h)][int(updown.x%w)] != 1:
                        if self.game.map.map[int(leftright.y%h)][int(leftright.x%w)] != 1:
                            self.vel = vec(0,0)
                            self.chasing = 0
                        else:
                            self.vel.x = signx * MONSTER_SPEED
                            self.walking = 1
                    elif self.game.map.map[int(leftright.y%h)][int(leftright.x%w)] != 1:
                        self.vel.y = signy * MONSTER_SPEED
                        self.walking = 1
                    elif rand == 0:
                        self.vel.x = self.sign(player.des.x, self.pos.x) * MONSTER_SPEED
                        self.walking = 1
                    else:
                        self.vel.y = self.sign(player.des.y, self.pos.y) * MONSTER_SPEED
                        self.walking = 1


        if self.walking == 1:
            self.pos += self.vel
            self.count += MONSTER_SPEED
            if(self.count==GRID):
                self.vel = vec(0, 0)
                self.count = 0
                self.walking = 0
                self.chasing = 0

    def sign(self, a, b):
        if a > b:
            return 1
        elif a == b:
            return 0
        else:
            return -1

    def attack(self, target):
        p = random.randint(90,110)
        damage = int((self.Atk - target.Def/2)* p/100)
        target.Hp -= damage

        #sound = pygame.mixer.Sound("D:/python/project/191919.wav")
        #sound.play()

        print("%s attacked %s, damage %d, player Hp %d"%(self.name, target.name, damage, target.Hp))
        text = "%s攻击了%s，造成%d点伤害"%(self.name, target.name, damage)
        self.draw_text(text,32,WHITE,320,360)

    def dead(self):
        if self.Hp <= 0:
            return True
        return False

    def escape(self):
        self.escaped = 1

    def draw_text(self, text, size, color, x, y):
        info_back = pygame.Surface((620,160))
        info_back.fill(BLACK)
        self.game.screen.blit(info_back, (10,300))
        font_name = pygame.font.match_font(FONT_NAME)
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.game.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(1500)

    def draw(self, screen):
        if self.dead():
            return
        if self.escaped == 1:
            return
        offset_x = self.game.camera.offset_x
        offset_y = self.game.camera.offset_y
        self.rect.left = self.pos.x-offset_x
        self.rect.top = self.pos.y-offset_y
        screen.blit(self.image, (self.rect.left, self.rect.top))

class Item(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.name = "药草"
        self.image = pygame.Surface((32,32))
        self.image = pygame.image.load("Sprites/grass.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = vec(160,288)
        self.pos = vec(894,960)
        self.cure = 5

    def use(self, target):
        target.Hp += self.cure
        if target.Hp > target.maxHp:
            cure = self.cure - target.Hp + target.maxHp
            target.Hp = target.maxHp
        else:
            cure = self.cure
        text = "%s使用了%s，回复了%d点体力"%(target.name, self.name, cure)
        self.draw_text(text,32,WHITE,320,360)

    def draw_text(self, text, size, color, x, y):
        info_back = pygame.Surface((620,160))
        info_back.fill(BLACK)
        self.game.screen.blit(info_back, (10,300))
        font_name = pygame.font.match_font(FONT_NAME)
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.game.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(1500)

    def draw(self, screen):
        offset_x = self.game.camera.offset_x
        offset_y = self.game.camera.offset_y
        self.rect.left = self.pos.x-offset_x
        self.rect.top = self.pos.y-offset_y
        screen.blit(self.image, (self.pos.x-offset_x, self.pos.y-offset_y))

class Bag():
    def __init__(self):
        self.itemList = []
        self.maxItem = 10

    def pickup(self, item):
        self.itemList.append(item)
        item.rect.topleft = vec(-32,-32)

    def use(self, item, target):
        if item in self.itemList:
            item.use(target)
            self.itemList.remove(item)

class Ladder(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((32,32))
        self.image = pygame.image.load("Sprites/ladder.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = vec(160,288)
        self.pos = vec(928,960)

    def draw(self, screen):
        offset_x = self.game.camera.offset_x
        offset_y = self.game.camera.offset_y
        self.rect.left = self.pos.x-offset_x
        self.rect.top = self.pos.y-offset_y
        screen.blit(self.image, (self.pos.x-offset_x, self.pos.y-offset_y))

class Messege(pygame.sprite.Sprite):
    def __init__(self, player, screen):
        super().__init__()
        self.player = player
        self.screen = screen

    def draw_text(self, text, size, color, x, y):
        font_name = pygame.font.match_font(FONT_NAME)
        font = pygame.font.Font(font_name, size)
        font.set_bold(True)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self, screen):
        p = self.player
        text = "%d层 等级：%d HP：%d/%d"%(p.floor, p.level, p.Hp, p.maxHp)
        self.draw_text(text,24,BLACK,320,0)
