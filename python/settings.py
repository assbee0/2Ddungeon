SCREEN_WIDTH = 640           # 屏幕宽
WIDTH = SCREEN_WIDTH
SCREEN_HEIGHT = 480           # 屏幕高
HEIGHT = SCREEN_HEIGHT
TITLE = "不可思议迷宫"                 # 标题
FPS = 60                               # 帧数
FONT_NAME = "幼圆"

BLUE = (0,0,255)                    # 蓝色
BLACK = (0,0,0)                      # 黑色
WHITE = (255,255,255)          # 白色

GRID = 32
GRID_SHIFT = 5

PLAYER_SPEED = 2      #玩家移动速度，为GRID的约数
MONSTER_SPEED = 2       #敌人移动速度，为GRID的约数

    #名字, 级， 血，攻，防，速，经，金
MONSTER =[
    ['Slim', 1,    2,    2,    1,     1,    3,    1],
    ['Chick', 2,    4,    3,    1,     2,    5,    2],
    ['Lion', 3,    8,     5,    1,    5,     8,    8],
    ['Kuma', 4,    10,     5,    5,    2,     10,    8]
]

ATTACK = 0
BAG = 1
SKILL = 2
ESCAPE = 3

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

RANDOM_MAP_A = 700
RANDOM_MAP_B = 10

LEVEL_EXP = [5, 11, 17, 24, 30, 37, 45, 53, 61, 71,
                     81, 92, 105, 118, 134, 152, 172, 196, 223, 255, 292]
