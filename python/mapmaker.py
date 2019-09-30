# -*- coding: utf-8 -*-
import pygame
import random
import os
from settings import *
import time

vec = pygame.math.Vector2

class Mapmaker:
    #地图生成类
    def __init__(self, W, H, Rw, Rh, Rl, p):
        #初始化
        self.map = [[0 for col in range(W+1)] for row in range(H+1)]
        self.weight = W    #地图宽度
        self.height = H    #地图高度
        self.room_wm = Rw    #房间宽度上限
        self.room_hm = Rh    #房间高度上限
        self.road_lm = Rl    #道路长度上限
        self.percent = p    #权重
        self.rooms= []    #房间列表
        self.walls = []    #墙壁列表
        for i in range(6):    #在房间中央固定生成一个初始房间
            for j in range(6):
                self.map[int(H/2)+j-3][int(W/2)+i-3] = 2
                if i==0 or i==5 or j==0 or j==5:
                    x = int(W/2)+ i - 3
                    y = int(H/2) + j -3
                    self.walls.append([y,x])
        for i in range(4):
            for j in range(4):
                self.map[int(H/2)+j-2][int(W/2)+i-2] = 1
        leftupx = int(H/2)
        leftupy = int(W/2)
        self.rooms.append([leftupx-3,leftupy-3,6,6])
        self.walls.remove([leftupx-3,leftupy-3])    #拆掉四个角的墙
        self.walls.remove([leftupx-3,leftupy+2])
        self.walls.remove([leftupx+2,leftupy-3])
        self.walls.remove([leftupx+2,leftupy+2])
        self.map[leftupx-3][leftupy-3] = self.map[leftupx-3][leftupy+2] = self.map[leftupx+2][leftupy-3] = self.map[leftupx+2][leftupy+2] = 3


    def run(self):
        #运行
        start = time.clock()    #开始时间，用于性能测试
        random_count_a = 0    #选择墙壁次数
        random_count_b = 0    #生成房间次数
        count = 0    #生成房间个数，用于性能测试
        while(random_count_a < RANDOM_MAP_A):    #选择墙壁次数未达到上限时
            wall = self.choose_wall()    #随机选择新墙壁
            while(random_count_b < RANDOM_MAP_B):    #选定墙壁后预生成房间次数未到上限时
                (rw,rh,dir) = self.check_room(wall)    #预生成房间
                if rw == -1:    #如果生成失败
                    random_count_b += 1
                else:    #成功则跳出循环
                    random_count_b = 0
                    break
            if random_count_b == RANDOM_MAP_B:    #预生成房间失败次数达到上限
                random_count_a += 1
                random_count_b = 0
                continue
            self.room_maker(wall,rw,rh,dir)    #正式生成新房间
            count+=1
        end = time.clock()
        print(count,end-start)
        return end-start, count

    '''def run(self):
    #原始算法，用于性能对比
        start = time.clock()
        random_count_a = 0
        random_count_b = 0
        count = 0
        while(count<=36):
            wall = self.choose_wall()
            (rw,rh,dir) = self.check_room(wall)
            if rw == -1:
                continue
            else:
                self.room_maker(wall,rw,rh,dir)
                count+=1
        end = time.clock()
        print(count,end-start)
        return end-start, count'''


    def choose_wall(self):
        #随机选择墙壁
        wall = random.choice(self.walls)
        return wall

    def check_room(self, wall):
        #预生成房间，检测房间是否可以被容纳
        room_w = random.randint(4, self.room_wm)    #房间宽
        room_h = random.randint(4, self.room_hm)    #房间高
        wx = wall[0]
        wy = wall[1]
        direct = 0
        start = []
        leftupx = leftupy = 0
        #判断房间的生成方向
        if self.map[wx+1][wy] == 0:
            direct = DOWN
        elif self.map[wx-1][wy] == 0:
            direct = UP
        elif self.map[wx][wy+1] == 0:
            direct = RIGHT
        elif self.map[wx][wy-1] == 0:
            direct = LEFT
        else:
            return -1,-1,-1

        #根据房间的生成方向分别判断
        if direct == UP:
            start = [wx-1,wy]
            leftupx = start[0] - room_h + 1    #计算出房间左上角坐标值
            leftupy = start[1] - int(room_w/2)
            if leftupx < 0:    #数组越界情况为生成失败
                return -1,-1,-1
            if leftupy < 0 or leftupy + room_w >= self.weight:
                return -1,-1,-1
            for i in range(room_h):
                for j in range(room_w):
                    if self.map[leftupx+i][leftupy+j] != 0:    #当前区域无法生成
                        return -1,-1,-1

        elif direct == DOWN:
            start = [wx+1,wy]
            leftupx = start[0]
            leftupy = start[1] - int(room_w/2)
            if leftupx + room_h >= self.height:
                return -1,-1,-1
            if leftupy < 0 or leftupy + room_w >= self.weight:
                return -1,-1,-1
            for i in range(room_h):
                for j in range(room_w):
                    if self.map[leftupx+i][leftupy+j] != 0:
                        return -1,-1,-1

        elif direct == LEFT:
            start= [wx,wy-1]
            leftupx = start[0] - int(room_h/2)
            leftupy = start[1] - room_w + 1
            if leftupx < 0 or leftupx + room_h >= self.height:
                return -1,-1,-1
            if leftupy < 0:
                return -1,-1,-1
            for i in range(room_h):
                for j in range(room_w):
                    if self.map[leftupx+i][leftupy+j] != 0:
                        return -1,-1,-1

        elif direct == RIGHT:
            start= [wx,wy+1]
            leftupx = start[0] - int(room_h/2)
            leftupy = start[1]
            if leftupx < 0 or leftupx + room_h >= self.height:
                return -1,-1,-1
            if leftupy + room_w >= self.weight:
                return -1,-1,-1
            for i in range(room_h):
                for j in range(room_w):
                    if self.map[leftupx+i][leftupy+j]  != 0:
                        return -1,-1,-1

        return room_w, room_h, direct


    def room_maker(self, wall, rw, rh, direct):
        #正式生成新房间
        room_w = rw
        room_h = rh
        wx = wall[0]
        wy = wall[1]
        self.map[wx][wy] = 1
        start = []
        leftupx = leftupy = 0

        if direct == UP:
            start = [wx-1,wy]
            for i in range(room_h):
                for j in range(room_w):
                    self.map[start[0]-i][start[1]+j-int(room_w/2)] = 1
            leftupx = start[0] - room_h + 1
            leftupy = start[1] - int(room_w/2)
            self.rooms.append([leftupx, leftupy, room_w, room_h])
        elif direct == DOWN:
            start = [wx+1,wy]
            for i in range(room_h):
                for j in range(room_w):
                    self.map[start[0]+i][start[1]+j-int(room_w/2)] = 1
            leftupx = start[0]
            leftupy = start[1] - int(room_w/2)
            self.rooms.append([leftupx, leftupy, room_w, room_h])
        elif direct == LEFT:
            start= [wx,wy-1]
            for i in range(room_w):
                for j in range(room_h):
                    self.map[start[0]+j-int(room_h/2)][start[1]-i] = 1
            leftupx = start[0] - int(room_h/2)
            leftupy = start[1] - room_w + 1
            self.rooms.append([leftupx, leftupy, room_w, room_h])
        elif direct == RIGHT:
            start= [wx,wy+1]
            for i in range(room_w):
                for j in range(room_h):
                    self.map[start[0]+j-int(room_h/2)][start[1]+i] = 1
            leftupx = start[0] - int(room_h/2)
            leftupy = start[1]
            self.rooms.append([leftupx, leftupy, room_w, room_h])

        for i in range(leftupx, leftupx+room_h):
            for j in range(leftupy, leftupy+room_w):
                if i == leftupx or i == leftupx+room_h-1 or j == leftupy or j == leftupy+room_w-1:
                    self.walls.append([i, j])
                    self.map[i][j] = 2
        self.map[leftupx][leftupy] = self.map[leftupx][leftupy+room_w-1] = 3
        self.map[leftupx+room_h-1][leftupy] = self.map[leftupx+room_h-1][leftupy+room_w-1] = 3
        self.map[start[0]][start[1]] = 1
        self.walls.remove(start)
        self.walls.remove([leftupx,leftupy])
        self.walls.remove([leftupx,leftupy+room_w-1])
        self.walls.remove([leftupx+room_h-1,leftupy+room_w-1])
        self.walls.remove([leftupx+room_h-1,leftupy])
        self.walls.remove(wall)
        # 拆新房间墙
        if self.map[start[0]][start[1]+1] == 1:
            x = start[0] - 1
            y = start[1]
            while self.map[x][y] != 3:
                self.map[x][y] = 3
                self.walls.remove([x,y])
                x = x - 1
            x = start[0] + 1
            y = start[1]
            while self.map[x][y] != 3:
                self.map[x][y] = 3
                self.walls.remove([x,y])
                x = x + 1
        elif self.map[start[0]+1][start[1]] == 1:
            x = start[0]
            y = start[1] - 1
            while self.map[x][y] != 3:
                self.map[x][y] = 3
                self.walls.remove([x,y])
                y = y - 1
            x = start[0]
            y = start[1] + 1
            while self.map[x][y] != 3:
                self.map[x][y] = 3
                self.walls.remove([x,y])
                y = y + 1
        # 拆旧房间墙
        if self.map[wall[0]][wall[1]+1] == 1:
            x = wall[0] - 1
            y = wall[1]
            while self.map[x][y] != 3:
                self.map[x][y] = 3
                self.walls.remove([x,y])
                x = x - 1
            x = wall[0] + 1
            y = wall[1]
            while self.map[x][y] != 3:
                self.map[x][y] = 3
                self.walls.remove([x,y])
                x = x + 1
        elif self.map[wall[0]+1][wall[1]] == 1:
            x = wall[0]
            y = wall[1] - 1
            while self.map[x][y] != 3:
                self.map[x][y] = 3
                self.walls.remove([x,y])
                y = y - 1
            x = wall[0]
            y = wall[1] + 1
            while self.map[x][y] != 3:
                self.map[x][y] = 3
                self.walls.remove([x,y])
                y = y + 1

    def generate_ladder(self):
        #随机房间内的中心坐标
        room = random.choice(self.rooms)
        posy = (room[0] + int(room[3]/2) - 1) * GRID
        posx = (room[1] + int(room[2]/2) - 1) * GRID
        return vec(posx,posy)

    def generate_enemy(self):
        #随机房间内的随机坐标
        room = random.choice(self.rooms)
        randomy = random.randint(1,room[3]-2)
        randomx = random.randint(1,room[2]-2)
        posy = (room[0] + randomy) * GRID
        posx = (room[1] + randomx) * GRID
        return vec(posx,posy)

    def getMap(self):
        return self.map


m = Mapmaker(60,30,10,10,5,0.5)
m.run()
fo = open("result.txt", "w")
print(os.getcwd())
for i in range(len(m.map)):
    print(m.map[i],file = fo)
m.generate_ladder()
#print(m.rooms)
#print(m.walls)
fo.close()
