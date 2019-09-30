# -*- coding: utf-8 -*-
import pygame
import random
from settings import *
import time

class BattleManager:
    def __init__(self, screen, player, enemy):
        self.player = player
        self.enemy = enemy
        self.screen = screen
        self.turn = 0
        self.escape_times = 0
        self.over = 0
        self.background = pygame.image.load("Sprites/battlefield.png").convert_alpha()
        self.yajyuu = enemy.imageb
        self.mouse = Mouse()

    def run(self):
        #进入战斗前的动画效果
        pygame.event.set_blocked([pygame.KEYDOWN])
        for i in range(20):
            pygame.draw.rect(self.screen,BLACK,[0,0,640,24*i])
            pygame.display.flip()
            pygame.time.delay(50)
        pygame.event.set_allowed([pygame.KEYDOWN])
        print("battle start")

        while(self.player.battling == 1):
            if self.enemy.dead():
                print("%s dead"%(self.enemy.name))
                self.player.battling = 0
                break
            self.turn += 1
            self.events()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    # 事件为退出
                self.player.battling = 0
                self.over = 1
                return

            elif event.type == pygame.KEYDOWN:
                choice = self.mouse.choose(event.key)
                pygame.event.set_blocked([pygame.KEYDOWN])
                if choice == ATTACK:
                    self.one_turn()
                elif choice == BAG:
                    if len(self.player.bag.itemList) > 0:
                        self.player.bag.use(self.player.bag.itemList[0], self.player)
                elif choice == ESCAPE:
                    self.escape()
                pygame.event.set_allowed([pygame.KEYDOWN])

    def one_turn(self):
        p1 = random.randint(50,100)
        p2 = random.randint(50,100)
        if(self.player.Spd * p1 >= self.enemy.Spd * p2):
            self.player.attack(self.enemy)
            if self.enemy.Hp > 0:
                self.enemy.attack(self.player)
            else:
                self.player.battling = 0
        else:
            self.enemy.attack(self.player)
            self.player.attack(self.enemy)

    def escape(self):
        if self.player.level -  self.enemy.level >= 10:
            self.enemy.escape()
            self.player.battling = 0
        else:
            escape_rate = self.escape_times * 30 + int(self.player.level * 100 / (self.player.level + self.enemy.level))
            if escape_rate >= 100:
                self.enemy.escape()
                self.player.battling = 0
            else:
                escape_random = random.randint(0,100)
                if escape_rate > escape_random:
                    self.enemy.escape()
                    self.player.battling = 0
                else:
                    self.escape_times += 1
                    self.turn += 1
                    text = "逃跑失败了"
                    self.draw_text(text,32,WHITE,320,360)
                    self.enemy.attack(self.player)

    def draw(self):
        self.screen.blit(self.background, (0,0))
        yajyuu_rect = self.yajyuu.get_rect()
        yajyuu_rect.center = (320,150)
        self.screen.blit(self.yajyuu, yajyuu_rect)
        if self.turn == 1:
            pygame.event.set_blocked([pygame.KEYDOWN])
            #sound = pygame.mixer.Sound("D:/python/project/24sai.wav")
            #sound.play()
            text = "野生的%s出现了"%(self.enemy.name)
            self.draw_text(text,32,WHITE,320,360)
            pygame.event.set_allowed([pygame.KEYDOWN])
        if self.player.battling == 0:
            if self.enemy.Hp <= 0:
                text = "%s死亡了"%(self.enemy.name)
                #sound = pygame.mixer.Sound("D:/python/project/yarimasune.wav")
                #sound.play()
                self.draw_text(text,32,WHITE,320,360)
                text = "玩家获得了%d经验值"%(self.enemy.Exp)
                self.draw_text(text,32,WHITE,320,360)
                self.player.Exp += self.enemy.Exp
                if self.player.Exp >= self.player.nextExp:
                    self.player.levelup()
                    text = "玩家升至了%d级"%(self.player.level)
                    self.draw_text(text,32,WHITE,320,360)
            else:
                text = "玩家逃跑了"
                self.draw_text(text,32,WHITE,320,360)
        else:
            self.mouse.draw(self.screen)
            pygame.display.flip()

    def draw_text(self, text, size, color, x, y):
        info_back = pygame.Surface((620,160))
        info_back.fill(BLACK)
        self.screen.blit(info_back, (10,300))

        font_name = pygame.font.match_font(FONT_NAME)
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
        pygame.time.delay(1500)

class Mouse:
    def __init__(self):
        self.image = pygame.Surface((32,32))
        self.image = pygame.image.load("Sprites/mouse.png").convert_alpha()
        self.state = ATTACK

    def choose(self, key):
        if self.state == ATTACK:
            if key == pygame.K_SPACE:
                return ATTACK
            elif key == pygame.K_RIGHT:
                self.state = BAG
            elif key == pygame.K_DOWN:
                self.state = SKILL
        elif self.state == BAG:
            if key == pygame.K_SPACE:
                return BAG
            elif key == pygame.K_LEFT:
                self.state = ATTACK
            elif key == pygame.K_DOWN:
                self.state = ESCAPE
        elif self.state == SKILL:
            if key == pygame.K_RIGHT:
                self.state = ESCAPE
            elif key == pygame.K_UP:
                self.state = ATTACK
        elif self.state == ESCAPE:
            if key == pygame.K_SPACE:
                return ESCAPE
            elif key == pygame.K_LEFT:
                self.state = SKILL
            elif key == pygame.K_UP:
                self.state = BAG

    def draw(self, screen):
        if self.state == ATTACK:
            screen.blit(self.image, (60,320))
        elif self.state == BAG:
            screen.blit(self.image, (330,320))
        elif self.state == SKILL:
            screen.blit(self.image, (60,400))
        elif self.state == ESCAPE:
            screen.blit(self.image, (330,400))
