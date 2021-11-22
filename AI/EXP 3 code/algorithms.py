import random
from abc import ABCMeta, abstractmethod
import time


# 算法类的抽象父类
class Algorithm(metaclass=ABCMeta):
    @abstractmethod
    def bestMove(self, depth, state, curr_player):
        pass


# 随机乱下算法
class Random(Algorithm):

    def bestMove(self, depth, state, curr_player):
        # 睡上大约一秒钟，假装在思考
        time.sleep(random.randrange(8, 17, 1) / 10.0)
        while True:
            random_move = random.randint(0, 6)
            for col in range(7):
                for row in range(6):
                    # 该位置是空的，可以合法地走棋
                    if state[row][col] == ' ':
                        return random_move


# Minimax算法
class Minimax(Algorithm):
    colors = ["x", "o"]

    def bestMove(self, depth, state, curr_player):

        # 确定对手的颜色
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        # 遍历所有位置，记录合法的下法，并且计算每种合法下法的得分
        legal_moves = {}
        for col in range(7):
            # 如果下在这里是是合法的
            if self.isLegalMove(col, state):
                # 试探性地下棋
                temp = self.makeMove(state, col, curr_player)
                # 搜索这步棋(为根的子树)的得分
                # 注意负号！！ 因为search返回的是对手的最高可能得分，所以分越高，对于本方来说越不好。
                legal_moves[col] = -self.search(depth - 1, temp, opp_player)

        best_alpha = -99999999
        best_move = None
        # 找到最高的得分所对应的下棋位置
        # shuffle的目的：避免在有多个平分的情况下，总是选择最右边的那一个位置
        moves = list(legal_moves.items())
        random.shuffle(moves)
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move

    # 搜索深度为depth的子树，返回得分（alpha value）
    def search(self, depth, state, curr_player):

        # 遍历所有位置，记录合法的下法
        legal_moves = []
        for i in range(7):
            # 如果下在这里是是合法的
            if self.isLegalMove(i, state):
                # 试探性地下棋
                temp = self.makeMove(state, i, curr_player)
                # 放到legal_moves集合里面去。
                legal_moves.append(temp)

        # 如果此节点（状态）是终端节点或深度==0。。。
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # 返回节点的启发函数值
            return self.value(state, curr_player)

        # 确定对手的颜色
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        alpha = -99999999
        # Max算法
        # 思考：为什么代码中只有max，而没有mini？
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth - 1, child, opp_player))
        return alpha

    # 用于检查column在当前state是否合法
    def isLegalMove(self, column, state):

        for i in range(6):
            if state[i][column] == ' ':
                # 一旦发现第一个空，就可以确定这是合法的
                return True

        # 如果都不空，就不合法
        return False

    # 判断游戏是否结束，如果有连成4个的棋子，则游戏结束
    def gameIsOver(self, state):
        if self.checkForStreak(state, self.colors[0], 4) >= 1:
            return True
        elif self.checkForStreak(state, self.colors[1], 4) >= 1:
            return True
        else:
            return False

    # 在column处下棋
    # 注意：返回的是一个新的棋盘
    def makeMove(self, state, column, color):
        temp = [x[:] for x in state]
        for i in range(6):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    # 一个简单的启发式算法
    def value(self, state, color):
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]

        # 统计本方的4连、3连、2连的数量
        my_fours = self.checkForStreak(state, color, 4)
        my_threes = self.checkForStreak(state, color, 3)
        my_twos = self.checkForStreak(state, color, 2)
        # 统计对方的4连的数量
        opp_fours = self.checkForStreak(state, o_color, 4)
        # 如果对方有4连，肯定要不得！！！
        if opp_fours > 0:
            return -100000
        else:
            # 一个简单的h_value计算式
            h_value = my_fours * 100000 + my_threes * 100 + my_twos
            return h_value

    def printState(self, board):
        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

    # 计算n子连线，n=streak
    def checkForStreak(self, state, color, streak):
        count = 0
        for i in range(6):
            for j in range(7):
                if state[i][j].lower() == color.lower():
                    count += self.verticalStreak(i, j, state, streak)
                    count += self.horizontalStreak(i, j, state, streak)
                    count += self.diagonalCheck(i, j, state, streak)
        return count

    # 计算纵向n子连线，n=streak
    def verticalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for i in range(row, 6):
            if state[i][col].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    # 计算横向n子连线，n=streak
    def horizontalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for j in range(col, 7):
            if state[row][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    # 计算斜向n子连线，n=streak
    def diagonalCheck(self, row, col, state, streak):
        total = 0
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1
        if consecutiveCount >= streak:
            total += 1
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1
        if consecutiveCount >= streak:
            total += 1
        return total
