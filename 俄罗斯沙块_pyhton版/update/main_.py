import matplotlib.pyplot as plt
import time

start_y = 10
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num = 0
        self.s = False


def init_grid(grid):
    # 初始化网格中的每个元素为Block对象
    for i in range(100):
        for j in range(100):
            grid[i][j] = Block(i, j)
    return grid


def init_specific_area(grid):
    start_x = 10
    start_y = 10
    # 设置特定区域的值
    for i in range(4):
        for j in range(4):
            grid[start_x + i][start_y + j].num = 1
    return grid


# 单独统计某一行和列
def r_and_c_sum(grid, start_row, x):
    lis = []
    for i in range(100):
        sum = 0
        for j in range(start_row, start_row + x):
            sum += grid[i][j].num
        lis.append(sum)
    return lis


def change(grid, index):
    # 深层拷贝相关操作，这里是将指定索引行的数据向上移动
    for j in range(4):
        temp = grid[index][start_y + j]
        for i in range(index, 0, -1):
            grid[i][start_y + j].num = grid[i - 1][start_y + j].num
            grid[i][start_y + j].s = grid[i - 1][start_y + j].s
            grid[i][start_y + j].y = grid[i - 1][start_y + j].y
            grid[i][start_y + j].x = grid[i - 1][start_y + j].x

        grid[0][start_y + j].num = temp.num
        grid[0][start_y + j].s = temp.s
        grid[0][start_y + j].y = temp.y
        grid[0][start_y + j].x = temp.x
    return grid


def solid(grid):
    for i in range(100):
        for j in range(100):
            grid[i][j].s = True
    return grid


def update(grid):
    chance_index = 0
    lis = r_and_c_sum(grid, start_y, 4)[::-1]
    a = 1
    for i in lis:
        if a == 0:
            break
        if i!= 0:
            index = lis.index(i)
            lis[index] = 0
            index = 99 - index
            for j in range(start_y, start_y + 4):
                if grid[index][j].s == True:
                    # 如果当前行的和不为0，却已经固定。退出，寻找下一行
                    last_ = index
                    break
                else:
                    chance_index = index
                    a = 0
                    break
    chance_index += 1
    last_ = 1000
    if last_ == chance_index:
        global s
        grid = solid(grid)
        print("index:", chance_index)
        s = True
        return grid
    grid = change(grid, chance_index)
    return grid


def get_lis(grid):
    lis = []
    for i in range(100):
        for j in range(100):
            if grid[i][j].num == 1:
                lis.append([grid[i][j].y, grid[i][j].x])
    return lis


def one(grid):
    grid = update(grid)
    if s:
        print("触底")
        exit()
    lis = get_lis(grid)
    return grid,lis



start_time = time.time()
grid = [[0 for _ in range(100)] for _ in range(100)]
s = False
grid = init_grid(grid)
grid = init_specific_area(grid)
for i in range(10):
    grid_, n = one(grid)
    grid = grid_
    print(n)
    n.clear()
end_time = time.time()
print("程序运行时间：", end_time - start_time)