import pygame
import sys
import time
import random
""" --- """
import matplotlib.pyplot as plt
import time
import heapq
import time
from collections import deque
class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.f < other.f

# 计算启发函数（曼哈顿距离）
def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

# A*寻路算法
def astar(start, goal, grid,type):
    open_list = []
    closed_list = []

    heapq.heappush(open_list, start)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]

        closed_list.append(current_node)

        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = Node(current_node.x + i, current_node.y + j, current_node)

            if neighbor.x < 0 or neighbor.x >= len(grid) or neighbor.y < 0 or neighbor.y >= len(grid[0]):
                continue

            if grid[neighbor.x][neighbor.y] != type:
                continue

            if neighbor in closed_list:
                continue

            neighbor.g = current_node.g + 1
            neighbor.h = heuristic(neighbor, goal)
            neighbor.f = neighbor.g + neighbor.h

            if any(node for node in open_list if node == neighbor and node.g <= neighbor.g):
                continue

            heapq.heappush(open_list, neighbor)

    return None


#地图大小
LENGTH = 500
WIDTH = 500
#方块大小
BLOCK_SIZE = 30
#起始位置
li = [100,150,200,300]
INIT_X = random.choice(li)
INIT_Y = 20

INIT_X_1 = 250
INIT_Y_1 = 30
STEP = 17
N = 3
SPEED =160
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
            map[INIT_Y_1 + i][INIT_X_1 + j] =num
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
    try:
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
    except:
        return new_map
    return new_map
def check(map, x, y, type):
    dx = [-1, 1, 0, 0]
    dy = [0, 1, -1, 0]
    q = deque([(x, y)])
    while q:
        cur_x, cur_y = q.popleft()
        if cur_x < 0 or cur_y < 0 or cur_x > len(map) - 1 or cur_y > len(map)-1:
            continue
        if map[cur_x][cur_y]!= type:
            continue
        map[cur_x][cur_y] = 0
        for i in range(4):
            new_x = cur_x+dx[i]
            new_y = cur_y + dy[i]
            if 0 <= new_x < len(map) and 0 <= new_y < len(map):
                q.append((new_x, new_y))
    return map

def start_check(map, i):
    print(map)
    y = i[0]
    TYP = map[y][0]
    print("y",y)
    print("type",TYP)
    map = check(map, y, 0, TYP)
    return map
def xiaochu(map):
    #找到左边出现不为0的且第一次出现的点的坐标
    L_lis_1 = []
    L_lis_2 = []
    L_lis_3 = []
    L_lis_4 = []
    """todo"""
    if map[WIDTH-1][0]!=0:
        if map[WIDTH-1][0] ==1:
            L_lis_1.append([WIDTH-1,0])
        elif map[WIDTH-1][0] ==2:
            L_lis_2.append([WIDTH-1,0])
        elif map[WIDTH-1][0] ==3:
            L_lis_3.append([WIDTH-1,0])
        elif map[WIDTH-1][0] ==4:
            L_lis_4.append([WIDTH-1,0])
    for i in range(WIDTH-2,0,-1):
        if map[i][0] != 0:
            if map[i][0] != map[i+1][0]:
                if map[i][0] ==1:
                    L_lis_1.append([i,0])
                elif map[i][0] ==2:
                    L_lis_2.append([i,0])
                elif map[i][0] ==3:
                    L_lis_3.append([i,0])
                elif map[i][0] ==4:
                    L_lis_4.append([i,0])

    R_lis_1 = []
    R_lis_2 = []
    R_lis_3 = []
    R_lis_4 = []
    """todo"""
    Right = LENGTH -1
    if map[WIDTH-1][Right]!=0:
        if map[WIDTH-1][Right] ==1:
            R_lis_1.append([WIDTH-1,Right])
        elif map[WIDTH-1][Right] ==2:
            R_lis_2.append([WIDTH-1,Right])
        elif map[WIDTH-1][Right] ==3:
            R_lis_3.append([WIDTH-1,Right])
        elif map[WIDTH-1][Right] ==4:
            R_lis_4.append([WIDTH-1,Right])
    for i in range(WIDTH-2,0,-1):
        if map[i][Right] != 0:
            if map[i][Right] != map[i+1][Right]:
                if map[i][Right] ==1:
                    R_lis_1.append([i,Right])
                elif map[i][Right] ==2:
                    R_lis_2.append([i,Right])
                elif map[i][Right] ==3:
                    R_lis_3.append([i,Right])
                elif map[i][Right] ==4:
                    R_lis_4.append([i,Right])
    #L_1 to R_1
    for i in L_lis_1:
        for j in R_lis_1:
            # x 是到上边距离
            # y 是到左边距离
            start = Node(i[0], i[1])
            end = Node(j[0], j[1])
            if astar(start, end, map,1) != None:
                return i
    #L_2 to R_2
    for i in L_lis_2:
        for j in R_lis_2:
            # x 是到上边距离
            # y 是到左边距离
            start = Node(i[0], i[1])
            end = Node(j[0], j[1])
            if astar(start, end, map,2) != None:
                return i
    #L_3 to R_3
    for i in L_lis_3:
        for j in R_lis_3:
            # x 是到上边距离
            # y 是到左边距离
            start = Node(i[0], i[1])
            end = Node(j[0], j[1])
            if astar(start, end, map,3) != None:
                return i
    #L_4 to R_4
    for i in L_lis_4:
        for j in R_lis_4:
            # x 是到上边距离
            # y 是到左边距离
            start = Node(i[0], i[1])
            end = Node(j[0], j[1])
            if astar(start, end, map,4) != None:
                return i
    print(L_lis_1,L_lis_2,L_lis_3,L_lis_4)
    print(R_lis_1,R_lis_2,R_lis_3,R_lis_4)
    return None
NUM=random.randint(0,N)
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
            a = xiaochu(map)
            if a != None:
                # print(a)
                # print("开始消除")
                map = start_check(map,a)
                for _ in range(15):
                    map = update_game(map)
            NUM = random.randint(0,N)
            map = add_init(map,NUM)
            INIT_X = random.choice(li)
            INIT_Y = 30
            INIT_X_1 = random.choice(li)
            INIT_Y_1 = 30


    screen.fill((0, 0, 0))
    draw_block(map)
    pygame.display.flip()
    clock.tick(SPEED)
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
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_LEFT:
                    for _ in range(STEP):
                        if INIT_X<=0:
                            # print("到达左边")
                            break
                        current_x = INIT_X
                        map = move(map,current_x,current_y,BLOCK_SIZE,BLOCK_SIZE,-1)
                        INIT_X -=1
                    # print("处理左移事件")
                elif event.key == pygame.K_RIGHT:
                    for _ in range(STEP):
                        if INIT_X+BLOCK_SIZE>=LENGTH:
                            # print("到达右边")
                            break
                        current_x = INIT_X
                        map = move(map, current_x, current_y, BLOCK_SIZE, BLOCK_SIZE, 1)
                        INIT_X +=1

                    # print("处理右移事件")
    # end_time = time.time()
    # print("time",end_time-start_time)

pygame.quit()
sys.exit()