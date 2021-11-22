import os

from connect4 import Game, Player, AIPlayer
from algorithms import Minimax


# Human Player vs Computer

# PvC_Game是Game的子类，只是初始化的时候不一样
class PvC_Game(Game):
    def __init__(self):
        super(PvC_Game, self).__init__()

        # 默认算法是Minimax，可以改成其他的算法
        algorithm = Minimax()

        # 清空屏幕，有时候会出问题，但是不影响程序执行。
        os.system('clear')
        print(u"Welcome to {0}!".format(self.game_name))
        print("Should Player 1 be a Human or a Computer?")
        while self.players[0] == None:
            # Human Player先走还是Computer先走
            choice = str(input("Type 'H' or 'C': "))
            if choice == "Human" or choice.lower() == "h":
                self.players[0] = Player("Human_Player", self.colors[0])
                # 设置AI的难度，也就是搜索的深度
                diff = int(input("Enter difficulty for this AI (1 - 4) "))
                self.players[1] = AIPlayer("AI_Player", algorithm, self.colors[1], diff + 1)
            elif choice == "Computer" or choice.lower() == "c":
                diff = int(input("Enter difficulty for this AI (1 - 4) "))
                self.players[0] = AIPlayer("AI_Player", algorithm, self.colors[0], diff + 1)
                self.players[1] = Player("Human_Player", self.colors[1])

            else:
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
    g = PvC_Game()

    # 打印（空）棋盘状态
    g.printState()
    player1 = g.players[0]
    player2 = g.players[1]

    while not g.finished:
        # 一步一步地下棋
        g.nextMove()

    # 至此棋局已经结束了，找出连成了4个一串的棋子
    g.findFours()
    # 打印（最终）棋盘状态
    g.printState()
