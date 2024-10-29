import pygame
import sys
import time
import random
""" --- """
import matplotlib.pyplot as plt
import time

#地图大小
LENGTH = 500
WIDTH = 500
#方块大小
BLOCK_SIZE = 50
#起始位置
INIT_X = 100
INIT_Y = 20

INIT_X_1 = 100
INIT_Y_1 = 20
#红黄蓝绿
num_to_color = {0:(255,255,255),1:(255,0,0),2:(255,255,0),3:(0,255,0),4:(0,0,255)}
map = [[0 for i in range(LENGTH)] for j in range(WIDTH)]
s = False

def init(map,num):
    # for i in range(BLOCK_SIZE):
    #     for j in range(BLOCK_SIZE):
    #         map[WIDTH - BLOCK_SIZE + j][INIT_X + i] = TYPE_1

    for i in range(BLOCK_SIZE):
        for j in range(BLOCK_SIZE):
            map[INIT_Y_1 + i][INIT_X_1 + j] = num
    return map

def add_init(map,num):
    new = [[0 for i in range(LENGTH)] for j in range(WIDTH)]
    for i in range(BLOCK_SIZE):
        for j in range(BLOCK_SIZE):
            new[INIT_Y_1 + i][INIT_X_1 + j] = num
    #添加到老map中
    for i in range(WIDTH):
        for j in range(LENGTH):
            if new[i][j] == 0:
                continue
            map[i][j] = new[i][j]
    return map
#单独统计某一行和列
def r_and_c_sum(map,start_row,x):
    lis = []
    for i in range(WIDTH):
        sum = 0
        for j in range(start_row,start_row+x):
            sum += map[i][j]
        lis.append(sum)
    return lis

def change(map_,index):

    for j in range(BLOCK_SIZE):
        temp = map_[index][INIT_X+j]
        for i in range(index,0,-1):
            map_[i][INIT_X+j] = map_[i-1][INIT_X+j]
        map_[0][INIT_X+j] = temp
    return map_
def update_game(map_):
    global chance_index
    chance_index = 0
    # print(INIT_X, BLOCK_SIZE)
    lis = r_and_c_sum(map_, INIT_X, BLOCK_SIZE)[::-1]
    a = 1
    for i in range(1,len(lis)):
        if a ==0:
            break
        if lis[i] !=0:
            tmp = i
            tmp_lis = []
            for j in range(tmp):
                tmp_lis.append(lis[j])
            # print("tmp_lis",tmp_lis)
            if 0 in tmp_lis:
                chance_index = tmp
                a = 0
            else:
                continue
    if chance_index==0:
        #表明没有找到
        chance_index = 0
    else:
        chance_index =WIDTH-chance_index
    # print("chance_index",chance_index)
    map_ = change(map_,chance_index)
    return map_
def g_update(map,lis):
    t = 0
    #实现类似重力的更新方式,i从下往上扫描
    for i in range(WIDTH-2,0,-1):
        if lis[i] == 0:
            continue
        # print(i)
        for j in range(LENGTH-1):
            if map[i][j]==0:
                continue
            #如果下方为0，下降
            if map[i+1][j] == 0:
                tmp = map[i][j]
                map[i][j] = 0
                map[i+1][j] = tmp
                t+=1
            #向左滑
            if map[i][j-1] == 0 and map[i+1][j-1]==0 and j!=0:
                tmp = map[i][j]
                map[i][j] = 0
                map[i+1][j-1] = tmp
                t+=1
            #向右滑
            if map[i][j+1] == 0 and map[i+1][j+1]==0 and j != LENGTH-1:
                tmp = map[i][j]
                map[i][j] = 0
                map[i+1][j+1] = tmp
                t+=1
    return map,t
def rotate(map_, x, y, r_x, r_y, fangxiang):
    # 复制原始地图，避免直接修改原地图
    new_map = [row.copy() for row in map_]
    if fangxiang == -1:
        for i in range(r_x):
            for j in range(r_y):
                # 计算旋转后的坐标
                new_i = j
                new_j = r_x - 1 - i
                new_map[x + new_i][y + new_j] = map_[x + i][y + j]
    elif fangxiang == 1:
        for i in range(r_x):
            for j in range(r_y):
                # 计算旋转后的坐标
                new_i = r_y - 1 - j
                new_j = i
                new_map[x + new_i][y + new_j] = map_[x + i][y + j]
    return new_map

def move(map_, y, x, r_x, r_y, fangxiang):
    new_map = [row.copy() for row in map_]
    if fangxiang == -1:
        for i in range(r_x):
            if y < len(map_):
                tmp = map_[x + i][y-1]
                for j in range(y, y + r_y):
                    if j > 0:
                        new_map[x + i][j - 1] = map_[x + i][j]
                    else:
                        # 处理左边界情况，这里设为0
                        new_map[x + i][j] = 0
                new_map[x + i][y + r_y - 1] = tmp
    elif fangxiang == 1:
        for i in range(r_x):
            if y + r_y < len(map_[0]):
                tmp = map_[x + i][y + r_y]
                for j in range(y + r_y - 1, y - 1, -1):
                    if j < len(map_[0]) - 1:
                        new_map[x + i][j + 1] = map_[x + i][j]
                    else:
                        # 处理右边界情况，这里设为0
                        new_map[x + i][j] = 0
                new_map[x + i][y] = tmp
    return new_map
NUM=random.randint(0,4)
map = init(map,NUM)
""" --- """
# 游戏窗口大小
WIDTH_1 = 800
HEIGHT_1 = 600
# 方块颜色
BLOCK_COLOR = (255, 0, 0)

# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH_1, HEIGHT_1))
pygame.display.set_caption("俄罗斯沙块")

def draw_block(map):
    for i in range(WIDTH):
        for j in range(LENGTH):
            if map[i][j] != 0:
                color = num_to_color[map[i][j]]
                pygame.draw.rect(screen, color, (j, i, 1, 1))

def get_lis(map_):
    lis_ = []
    for i in range(WIDTH):
        for j in range(LENGTH):
            if map_[i][j] == TYPE_1:
                lis_.append([j,i])
    return lis_




clock = pygame.time.Clock()
running = True

step = 0
while running:
    # start_time = time.time()


    map = update_game(map)

    step+=1

    # lis = get_lis(map)
    # print(lis)
    if chance_index==0:
        step = 0
        map,t = g_update(map,r_and_c_sum(map,INIT_X,BLOCK_SIZE))
        if t == 0:
            NUM = random.randint(0,4)
            map = add_init(map,NUM)
            INIT_X = 100
            INIT_Y = 20
            INIT_X_1 = 100
            INIT_Y_1 = 20


    screen.fill((0, 0, 0))
    draw_block(map)
    pygame.display.flip()
    clock.tick(240)
    #记录当前坐标
    current_x = INIT_X
    current_y = INIT_Y + step
    # print(current_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if chance_index !=0:
                # 按键按下
                if event.key == pygame.K_UP:
                    map = rotate(map,current_y,current_x,BLOCK_SIZE,BLOCK_SIZE,-1)
                    # print("处理上移事件")
                elif event.key == pygame.K_DOWN:
                    map = rotate(map,  current_y, current_x,BLOCK_SIZE, BLOCK_SIZE, 1)
                    # print("处理下移事件")
                elif event.key == pygame.K_LEFT:
                    for _ in range(20):
                        if INIT_X<=0:
                            print("到达左边")
                            break
                        current_x = INIT_X
                        map = move(map,current_x,current_y,BLOCK_SIZE,BLOCK_SIZE,-1)
                        INIT_X -=1
                    # print("处理左移事件")
                elif event.key == pygame.K_RIGHT:
                    for _ in range(20):
                        if INIT_X+BLOCK_SIZE>=LENGTH:
                            print("到达右边")
                            break
                        current_x = INIT_X
                        map = move(map, current_x, current_y, BLOCK_SIZE, BLOCK_SIZE, 1)
                        INIT_X +=1

                    # print("处理右移事件")
    # end_time = time.time()
    # print("time",end_time-start_time)

pygame.quit()
sys.exit()