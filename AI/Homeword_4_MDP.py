# 一些全局变量
p = 0.9
living_reward = -0.01
gama = 0.95


# 每个格子的类
class Grid:
    def __init__(self, grid_world=None, x=0, y=0):
        # 位置坐标
        self.x = x
        self.y = y

        # 记录下所在的grid_world，方便寻找东南西北的格子
        self.grid_world = grid_world

        # 格子的所有对应的q states
        self.q_states = set()

        # 合法的行动
        self.actions = {"W", "E", "S", "N"}
        for action in self.actions:
            self.q_states.add(Q_state(self, action))

        # 是否是终点格
        self.is_exit = False
        self.exit_reward = 0

        # 格子的效用值
        self.value = 0

        # 最佳行动
        self.best_action = ""

    # 找出向北移动后的格子
    def find_north(self):
        for g in self.grid_world.grids:
            if g.x == self.x:
                if g.y == self.y + 1:
                    return g
        return self

    def find_south(self):
        for g in self.grid_world.grids:
            if g.x == self.x:
                if g.y == self.y - 1:
                    return g
        return self

    def find_east(self):
        for g in self.grid_world.grids:
            if g.y == self.y:
                if g.x == self.x + 1:
                    return g
        return self

    def find_west(self):
        for g in self.grid_world.grids:
            if g.y == self.y:
                if g.x == self.x - 1:
                    return g
        return self

    # 根据最大的q state的效用值更新格子的效用值
    def update_value(self):
        if self.is_exit is True:
            self.value = self.exit_reward
        else:
            temp = -65545
            for q in self.q_states:
                if q.value > temp:
                    temp = q.value
            self.value = temp

    # 根据最大的q state的效用值更新格子的最佳行动值
    def update_best_action(self):
        if self.is_exit is True:
            self.best_action = "ex"
        else:
            min_temp = -65535
            for q in self.q_states:
                if q.value > min_temp:
                    min_temp = q.value
                    self.best_action = q.action

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + ":" + self.best_action + "=" + str(round(self.value, 1)) + "]"


class Q_state:

    def __init__(self, grid, action):
        self.grid = grid
        self.action = action
        self.value = 0

    # 状态转移的结果
    def trans(self):
        transitions = set()
        if self.action == "W":
            transitions.add((self.grid.find_west(), p))
            transitions.add((self.grid.find_north(), (1 - p) / 2))
            transitions.add((self.grid.find_south(), (1 - p) / 2))
        if self.action == "S":
            transitions.add((self.grid.find_south(), p))
            transitions.add((self.grid.find_west(), (1 - p) / 2))
            transitions.add((self.grid.find_east(), (1 - p) / 2))
        if self.action == "N":
            transitions.add((self.grid.find_north(), p))
            transitions.add((self.grid.find_east(), (1 - p) / 2))
            transitions.add((self.grid.find_west(), (1 - p) / 2))
        if self.action == "E":
            transitions.add((self.grid.find_east(), p))
            transitions.add((self.grid.find_north(), (1 - p) / 2))
            transitions.add((self.grid.find_south(), (1 - p) / 2))
        return transitions

    # 根据状态转移的结果，已经对应的格子的效用值，计算q state的效用值
    def update_value(self):
        transitions = self.trans()
        temp = 0
        for grid, p in transitions:
            temp += p * (living_reward + gama * grid.value)
        self.value = temp


# 格子世界的类
class GridWorld:

    def __init__(self, size=(8, 8), ):
        self.size = size
        # 记录下世界中所有的格子
        self.grids = set()
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                grid = Grid(self, i, j)
                self.grids.add(grid)
        exit_good = self.grids.pop()
        exit_good.is_exit = True
        exit_good.exit_reward = 10
        exit_bad = self.grids.pop()
        exit_bad.is_exit = True
        exit_bad.exit_reward = -10
        self.grids.add(exit_bad)
        self.grids.add(exit_good)

    def find_by_position(self, x, y):
        for g in self.grids:
            if g.y == y:
                if g.x == x:
                    return g
        return None

    # 获取所有格子的效用值之和，用于计算每次迭代的变化
    def get_total_values(self):
        total = 0
        for g in self.grids:
            total += g.value
        return total

    def __str__(self):
        grid_world_str = ""
        # 注意迭代的顺序，为了符合上北下南左西右东
        for j in reversed(range(0, self.size[0])):
            for i in range(0, self.size[1]):
                g = self.find_by_position(i, j)
                grid_world_str += "\t" + str(g)
            grid_world_str += "\n"
        return grid_world_str


grid_world = GridWorld()

delta = 65535
epsilon = 0.01

# 迭代，直到变化小于epsilon，则可以认为已经收敛了。
while delta > epsilon:
    current_total_values = grid_world.get_total_values()
    for g in grid_world.grids:
        for q in g.q_states:
            # 更新每个q state的效用值
            q.update_value()
        # 更新每个格子的效用值
        g.update_value()
    delta = abs(grid_world.get_total_values() - current_total_values)

for g in grid_world.grids:
    # 更新每个格子的最佳行动值
    g.update_best_action()
print(grid_world)
