# -*- coding: utf-8 -*-
import pygame
import os
from pygame.locals import *
from settings import *
from sprites import *
from battle import *
from mapmaker import *

vec = pygame.math.Vector2

class Camera:   #i相机类
    def __init__(self, map):
        self.mx = map.width * GRID - SCREEN_WIDTH    #宽度最大范围
        self.my = map.height * GRID - SCREEN_HEIGHT    #长度最大范围

    def update(self, player):
        self.player = player
        self.px = player.pos.x    #获取玩家当前位置
        self.py = player.pos.y
        self.offset_x = max(0, self.px - SCREEN_WIDTH/2)    #计算坐标系之间的偏移量，此处处理左上边缘部分
        self.offset_y = max(0, self.py - SCREEN_HEIGHT/2)
        self.offset_x = min(self.offset_x, self.mx)    #处理右下边缘部分
        self.offset_y = min(self.offset_y, self.my)

class Map(pygame.sprite.Sprite):
    def __init__(self, mapcore, w, h):
        super().__init__()
        self.map = [[0 for col in range(w)] for row in range(h)]
        self.map = mapcore    #获取地图数据
        self.msize = GRID
        self.width = w
        self.height = h
        self.camera = None
        self.imgs = [None] * 32
        self.imgs[0] = pygame.image.load("Sprites/wall.png").convert_alpha()    #获取地图贴图
        self.imgs[1] = pygame.image.load("Sprites/ground.png").convert_alpha()
        self.imgs[2] = self.imgs[3] = self.imgs[0]

    def draw(self, screen):
        offset_x = self.camera.offset_x
        offset_y = self.camera.offset_y
        startx = int(offset_x / GRID)    #计算地图绘制的起点
        starty = int(offset_y / GRID)
        for i in range(starty,starty+16):    #此处要比窗口长宽均多一格，防止数组越界
            for j in range(startx,startx+21):
                #绘制地图
                screen.blit(self.imgs[self.map[i][j]], (j*self.msize - offset_x,i*self.msize - offset_y))

    def setCamera(self, camera):
        self.camera = camera

class Game:
    # 游戏类
    def __init__(self):
        # 初始化
        self.running = True    # 开始运行程序
        pygame.init()    # 初始化pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))    #  生成窗口
        pygame.display.set_caption(TITLE)    # 设置标题
        self.clock = pygame.time.Clock()    # 创建时钟对象
        self.playing = False    #游戏状态
        self.player = None    # 初始化空玩家
        self.map = None
        self.camera = None
        self.messagebox = None
        self.floor = 1    #当前层数

    def new(self):
        # 生成新游戏
        self.all_sprites = pygame.sprite.Group()    # 创建所有精灵组
        self.player = Player(self)    # 创建玩家对象
        self.messagebox = Messege(self.player, self.screen)    #创建消息栏
        self.enemy = []
        self.herb = Item(self)    #创建药草对象
        self.ladder = Ladder(self)    #创建梯子对象
        self.all_sprites.add(self.player)    # 将玩家加入组
        self.all_sprites.add(self.ladder)    #将梯子加入组
        self.all_sprites.add(self.herb)    #将药草加入组
        mapmaker = Mapmaker(20,20,10,10,5,0.5)    #生成一个长宽均为20，房间长宽上限为10的地图
        mapmaker.run()    #地图生成中
        mapcore = mapmaker.getMap()
        self.map = Map(mapcore,20,20)    #创建地图对象
        self.player.pos = mapmaker.generate_enemy()    #随机获取玩家位置
        self.herb.pos = mapmaker.generate_enemy()    #随机获取道具位置
        self.ladder.pos = mapmaker.generate_ladder()    #随机获取梯子位置
        for i in range(self.floor):    #根据层数来生成相应数量的敌人
            self.enemy.append(Enemy(0,self))    #生成敌人
            self.all_sprites.add(self.enemy[i])    #将敌人加入精灵组
            self.enemy[i].pos = mapmaker.generate_enemy()    #随机获取敌人位置
        self.camera = Camera(self.map)    #创建相机对象
        self.all_sprites.add(self.messagebox)    #考虑到绘制顺序，将消息栏最后加入组
        self.run()    # 运行游戏

    def run(self):
        # 游戏循环
        self.playing = True    #游戏运行标志
        while(self.playing):
            self.clock.tick(FPS)    # 设置帧数
            self.events()    #处理游戏事件
            self.update()    #游戏状态更新
            self.draw()    #游戏整体绘制

    def events(self):
        # 游戏事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    # 事件为退出
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        # 更新所有精灵
        self.all_sprites.update()    #执行所有精灵的更新方法
        self.camera.update(self.player)    #更新相机的状态
        self.map.setCamera(self.camera)    #将相机传递给地图
        for e in self.enemy:    #遍历敌人，判断与玩家的碰撞
            hit_enemy = pygame.sprite.collide_rect(self.player, e)
            if hit_enemy:
                e.rect.topleft = (-256,-256)
                self.player.battling = 1    #进入战斗状态
                self.battle = BattleManager(self.screen,self.player,e)    #创建战斗管理对象
                self.battle.run()    #运行战斗
                if self.battle.over == 1:    #如果战斗强行结束，则关闭游戏
                    self.running = False
                    self.playing = False
        hit_item = pygame.sprite.collide_rect(self.player, self.herb)    #判断玩家和道具的碰撞
        if hit_item:
            self.herb.pos = vec(-256,-256)
            self.herb.rect.topleft = vec(-256,-256)
            self.player.bag.pickup(self.herb)    #玩家拾取道具
        hit_ladder = pygame.sprite.collide_rect(self.player, self.ladder)    #判断玩家和梯子的碰撞
        if hit_ladder:
            #黑屏300ms
            self.screen.fill(BLACK)
            pygame.display.flip()
            pygame.time.delay(300)

            self.floor += 1    #层数加1
            self.ladder.rect.topleft = vec(-256,-256)
            self.ladder.pos = vec(-256,-256)
            cur_w = 15+self.floor*5    #计算下一层地图的规模
            cur_h = 15+self.floor*5
            mapmaker = Mapmaker(cur_w,cur_h,10,10,5,0.5)    #根据计算出的规模，生成新的地图
            mapmaker.run()
            mapcore = mapmaker.getMap()
            self.map.map = mapcore
            self.map.width = cur_w
            self.map.height = cur_h
            self.ladder.pos = mapmaker.generate_ladder()
            self.player.pos = mapmaker.generate_enemy()
            self.herb.pos = mapmaker.generate_enemy()
            print(self.player.pos)
            self.camera.__init__(self.map)    #更新相机状态
            for e in self.enemy:
                self.all_sprites.remove(e)    #移除所有前一层的敌人
            self.enemy = []
            for i in range(self.floor):
                num = random.randint(min(self.floor-2,3),min(3,self.floor-1))    #根据层数来调整敌人的强度
                self.enemy.append(Enemy(num,self))
                self.all_sprites.add(self.enemy[i])
                self.enemy[i].pos = mapmaker.generate_enemy()
            self.player.downstairs()    #玩家下楼

    def draw(self):
        # 绘制
        self.screen.fill(BLACK)    # 背景涂黑
        self.map.draw(self.screen)
        for sprite in self.all_sprites:    #对每个精灵都执行绘制方法
            sprite.draw(self.screen)
        pygame.display.flip()    # 将绘制结果更新到屏幕

g = Game()
while(g.running):
    g.new()
pygame.quit()
