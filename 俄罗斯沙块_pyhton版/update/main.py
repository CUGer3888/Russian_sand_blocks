"""
游戏名称： 俄罗斯沙块
作者： 袁张俊
版本： 1.0
日期： 2024-10-24
"""
# import sys
# import pygame
# 100*100map
#引用绘图
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

def init(map):
    for i in range(100):
        for j in range(100):
            map[i][j] =0
    for i in range(4):
        for j in range(4):
            map[96 + i][10 + j] = 1

    for i in range(4):
        for j in range(4):
            map[start_x + i][start_y + j] = 1
    return map
#单独统计某一行和列
def r_and_c_sum(map,start_row,x):
    lis = []
    for i in range(100):
        sum = 0
        for j in range(start_row,start_row+x):
            sum += map[i][j]
        lis.append(sum)
    return lis

def change(map_,index):

    for j in range(4):
        temp = map_[index][start_y+j]
        for i in range(index,0,-1):
            map_[i][start_y+j] = map_[i-1][start_y+j]
        map_[0][start_y+j] = temp
    return map_
def update(map_):
    chance_index = 0
    lis = r_and_c_sum(map_, start_y, 4)[::-1]
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
        chance_index =100-chance_index
    print("chance_index",chance_index)
    map_ = change(map_,chance_index)
    return map_
def get_lis(map_):
    lis_ = []
    for i in range(100):
        for j in range(100):
            if map_[i][j] == 1:
                lis_.append([j,i])
    return lis_


map = init(map)

for i in range(100):
    map = update(map)
    print(r_and_c_sum(map, 10, 4)[::-1])
    print(get_lis(map))