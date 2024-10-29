
import matplotlib.pyplot as plt
import time
start_time = time.time()
map = [[0 for i in range(100)] for j in range(100)]
s = False
start_x = 10
start_y = 10


# block 形状：正方形
block = [[1, 1, 1, 1],
         [1, 1, 1, 1],
         [1, 1, 1, 1],
         [1, 1, 1, 1],
         ]
def r_and_c_sum(map,start_row,x):
    lis = []
    for i in range(100):
        sum = 0
        for j in range(start_row,start_row+x):
            sum += map[i][j]
        lis.append(sum)
    return lis
def init(map):
    for i in range(100):
        for j in range(100):
            map[i][j] =0
    # for i in range(4):
    #     for j in range(4):
    #         map[96 + i][10 + j] = 1

    for i in range(4):
        for j in range(4):
            map[start_x + i][start_y + j] = 1
    return map
map = init(map)
def g_update(map,lis):
    global a
    a = 0
    #实现类似重力的更新方式,i从下往上扫描
    for i in range(98,0,-1):
        if lis[i] == 0:
            continue
        print(i)
        for j in range(99):
                #如果下方为0，下降
                if map[i+1][j] == 0:
                    tmp = map[i][j]
                    map[i][j] = 0
                    map[i+1][j] = tmp
                #向左滑
                if map[i][j-1] == 0 and map[i+1][j-1]==0:
                    tmp = map[i][j]
                    map[i][j] = 0
                    map[i+1][j-1] = tmp
                #向右滑
                if map[i][j+1] == 0 and map[i+1][j+1]==0:
                    tmp = map[i][j]
                    map[i][j] = 0
                    map[i+1][j+1] = tmp
    return map
def show(map):
    # matplotlib.pyplot as plt
    plt.imshow(map, cmap='gray')
    plt.show()

def rotate(map_, x, y, r_x, r_y, fangxiang):
    # 复制原始地图，避免直接修改原地图
    new_map = [row.copy() for row in map_]
    show(new_map)
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

# lis = r_and_c_sum(map,10,4)
# map = g_update(map,lis)
# map = g_update(map,lis)
# map = g_update(map,lis)
# print(a)
# print(r_and_c_sum(map, 10, 4)[::-1])
# show(map)
# map = rotate(map, 10, 10, 4, 4, -1)
# show(map)
# def move(map_, y, x, r_x, r_y, fangxiang):
#     new_map = [row.copy() for row in map_]
#     if fangxiang == -1:
#         for i in range(r_x):
#             if y < len(map_):
#                 tmp = map_[x + i][y-1]
#                 for j in range(y, y + r_y):
#                     if j > 0:
#                         new_map[x + i][j - 1] = map_[x + i][j]
#                     else:
#                         # 处理左边界情况，这里设为0
#                         new_map[x + i][j] = 0
#                 new_map[x + i][y + r_y - 1] = tmp
#     elif fangxiang == 1:
#         for i in range(r_x):
#             if y + r_y - 1 < len(map_):
#                 tmp = map_[x + i][y + r_y]
#                 for j in range(y + r_y - 1, y - 1, -1):
#                     if j < len(map_[0]) - 1:
#                         new_map[x + i][j + 1] = map_[x + i][j]
#                     else:
#                         # 处理右边界情况，这里设为0
#                         new_map[x + i][j] = 0
#                 new_map[x + i][y] = tmp
#     return new_map

# map_example = [[1, 2, 3,12],
#                [4, 5, 6,11],
#                [7, 8, 9,10]]
# x = 1
# y = 1
# r_x =2
# r_y = 2
# result = move(map_example, x, y, r_x, r_y, -1)
# for row in result:
#     print(row)
# c_x = 10
# c_y = 10
# for i in range(10):
#     print(r_and_c_sum(map, 10, 4)[::-1])
#     map = move(map, c_x, c_y, 4, 4, 1)
#     show(map)
#     c_x +=1
#     print(c_x)
from collections import deque


# def check(map, x, y, type):
#     dx = [-1, 1, 0, 0]
#     dy = [0, 1, -1, 0]
#     q = deque([(x, y)])
#     while q:
#         cur_x, cur_y = q.popleft()
#         if cur_x < 0 or cur_y < 0 or cur_x > len(map) - 1 or cur_y > len(map)-1:
#             continue
#         if map[cur_x][cur_y]!= type:
#             continue
#         map[cur_x][cur_y] = 0
#         for i in range(4):
#             new_x = cur_x+dx[i]
#             new_y = cur_y + dy[i]
#             if 0 <= new_x < len(map) and 0 <= new_y < len(map):
#                 q.append((new_x, new_y))
#     return map
# def show(map):
#     plt.imshow(map, cmap='gray')
#     plt.show()
#
# map = [[0 for _ in range(200)] for _ in range(200)]
# #第一行变为1
# for j in range(10):
#     for i in range(200):
#         map[j][i] = 1
# show(map)
# map = check(map, 0, 0, 1)
# show(map)
print(type(500//2))
print(type(500/2))
# map = [[0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 1, 1, 1, 0],
#         [1, 1, 1, 1, 0],
#         [1, 1, 1, 1, 0]]
# map = check(map, 11, 0, 1)
# print(map)