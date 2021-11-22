import os

from connect4 import Game, AIPlayer

# 把所有算法都import进来，很重要！！
from algorithms import *


# Computer vs Computer， 用来测试两个算法哪个比较厉害
# 把需要测试的两个算法都放到algorithms文件里面
# 或者修改前面的import语句，确保需要被测试的算法都成功的import进来了

# CvC_Game是Game的子类，只是初始化的时候不一样
class CvC_Game(Game):
    def __init__(self):
        # 调用超类的构造函数
        super(CvC_Game, self).__init__()

        # 清空屏幕，有时候会出问题，但是不影响程序执行。
        os.system('clear')
        print(u"Welcome to {0}!".format(self.game_name))
        print("What algorithm should Player 1 use?")
        while self.players[0] == None:
            try:
                # 读取算法一的类名，并构造算法一对象
                algorithm1_class_name = str(input("Type algorithm class name: "))
                algorithm1_class = globals()[algorithm1_class_name]
                algorithm1 = algorithm1_class()
                diff = int(input("Enter difficulty for this AI (1 - 4) "))
                self.players[0] = AIPlayer(algorithm1_class_name, algorithm1, self.colors[0], diff + 1)
            except:
                print("Invalid choice, please try again")
        while self.players[1] == None:
            try:
                # 读取算法二的类名，并构造算法二对象
                algorithm2_class_name = str(input("Type algorithm class name: "))
                algorithm2_class = globals()[algorithm2_class_name]
                algorithm2 = algorithm2_class()
                diff = int(input("Enter difficulty for this AI (1 - 4) "))
                self.players[1] = AIPlayer(algorithm2_class_name, algorithm2, self.colors[1], diff + 1)
            except:
                print("Invalid choice, please try again")

        print("{0} will be {1}".format(self.players[0].name, self.colors[0]))
        print("{0} will be {1}".format(self.players[1].name, self.colors[1]))

        # 设定谁先走棋
        self.turn = self.players[0]

        # 初始化棋盘
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')


if __name__ == "__main__":
    g = CvC_Game()

    games = None
    win_counts = [0, 0, 0]  # [p1 wins, p2 wins, ties]

    while games == None:
        try:
            games = int(input("How many games should they play: "))
        except:
            print("Invalid input! please try again")
    player1 = g.players[0]
    player2 = g.players[1]
    game = 0
    while game < games:
        game += 1

        # 打印（空）棋盘状态
        g.printState()

        while not g.finished:
            # 一步一步地下棋
            g.nextMove()

        # 至此棋局已经结束了，找出连成了4个一串的棋子
        g.findFours()

        # 打印（最终）棋盘状态
        g.printState()

        # 记录结果
        if g.winner == None:
            win_counts[2] += 1
        else:
            if g.winner == player1:
                win_counts[0] += 1
            elif g.winner == player2:
                win_counts[1] += 1

        # 重新初始化棋局
        g.newGame()

        # 双方交互棋子颜色（先手）
        g.switchPlayerTurn()

    print("Final results: {0} {1} wins, {2} {3} wins, {4} ties".format(player1.name,
                                                                       win_counts[0], player2.name, win_counts[1],
                                                                       win_counts[2]))
