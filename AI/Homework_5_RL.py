import random

# 一些全局变量
p = 0.9
living_reward = -0.01
gama = 0.95

# epsilon-greedy学习策略的参数
epsilon = 0.99
epsilon_decay = 0.9999

# 时间差分学习的学习率
alpha = 0.5
alpha_decay = 0.99

# grid world的大小
grid_size = (8, 8)

# 固定下出口的位置，方便与MDP比较
exit_good_position = (2, 2)
exit_bad_position = (5, 5)


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
        self.best_action = random.choice(list(self.actions))

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
        updated = False
        best_action_last = self.best_action
        if self.is_exit is True:
            self.best_action = "ex"
        else:
            min_temp = -65535
            for q in self.q_states:
                if q.value > min_temp:
                    min_temp = q.value
                    self.best_action = q.action
        if self.best_action != best_action_last:
            updated = True
        return updated

    def get_action(self):
        if self.is_exit is True:
            return "ex"
        if random.random() < epsilon:
            return random.choice(list(self.actions))
        else:
            return self.best_action

    def get_q_state(self, action):
        for q in self.q_states:
            if q.action == action:
                return q
        print("something wrong with get_q_state()")

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + ":" + self.best_action + "=" + str(round(self.value, 1)) + "]"


class Q_state:

    def __init__(self, grid, action):
        self.grid = grid
        self.action = action
        self.value = 0

    # 根据状态转移的结果，对应的格子的效用值，计算q state的效用值
    def update_value(self, transition, reward):
        # 时间差分学习
        self.value = (1 - alpha) * self.value + alpha * (reward + gama * transition.value)


# 格子世界的类
class GridWorld:

    def __init__(self, size=grid_size):
        self.size = size
        # 记录下世界中所有的格子
        self.grids = set()
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                grid = Grid(self, i, j)
                self.grids.add(grid)
        exit_good = self.find_by_position(exit_good_position[0], exit_good_position[1])
        exit_bad = self.find_by_position(exit_bad_position[0], exit_bad_position[1])
        exit_good.is_exit = True
        exit_good.exit_reward = 10
        exit_bad.is_exit = True
        exit_bad.exit_reward = -10

    def find_by_position(self, x, y):
        for g in self.grids:
            if g.y == y:
                if g.x == x:
                    return g
        return None

    def __str__(self):
        grid_world_str = ""
        # 注意迭代的顺序，为了符合上北下南左西右东
        for j in reversed(range(0, self.size[0])):
            for i in range(0, self.size[1]):
                g = self.find_by_position(i, j)
                grid_world_str += "\t" + str(g)
            grid_world_str += "\n"
        return grid_world_str

    # grid_world决定当一个grid采取一个action后会转移到哪个grid，以及过程中的reward
    def take_action(self, g, action):
        rand = random.random()
        # 正常移动
        if rand < p:
            if action == "W":
                return g.find_west(), living_reward
            if action == "S":
                return g.find_south(), living_reward
            if action == "N":
                return g.find_north(), living_reward
            if action == "E":
                return g.find_east(), living_reward
        # 往左滑
        elif rand < p + (1 - p) / 2:
            if action == "W":
                return g.find_south(), living_reward
            if action == "S":
                return g.find_east(), living_reward
            if action == "N":
                return g.find_west(), living_reward
            if action == "E":
                return g.find_south(), living_reward
        # 往右滑
        else:
            if action == "W":
                return g.find_north(), living_reward
            if action == "S":
                return g.find_west(), living_reward
            if action == "N":
                return g.find_east(), living_reward
            if action == "E":
                return g.find_north(), living_reward


grid_world = GridWorld()

# 没有更新最佳行动的行动次数
no_updates_moves = 0
# 行动次数
moves = 0

# 随机初始位置
start_position = (random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1))
g = grid_world.find_by_position(start_position[0], start_position[1])

while no_updates_moves < 500:
    # 决策'试图'移动的方向
    action = g.get_action()
    if action != "ex":
        # 获取向此方向移动的结果
        transition, reward = grid_world.take_action(g, action)
        q = g.get_q_state(action)
        # 更新q state的效用值
        q.update_value(transition, reward)

    g.update_value()
    updated = g.update_best_action()
    if action != "ex":
        # 移动
        g = transition
    else:
        # 走到出口了，重新随机初始化位置
        start_position = (random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1))
        g = grid_world.find_by_position(start_position[0], start_position[1])
    if updated is False:
        no_updates_moves += 1
    else:
        no_updates_moves = 0

    moves += 1
    if moves % (grid_size[0] * grid_size[1]) == 0:
        epsilon = epsilon * epsilon_decay
        alpha = alpha * alpha_decay

print("Convergence after " + str(moves) + " moves. Learned best actions are:")
print(grid_world)
