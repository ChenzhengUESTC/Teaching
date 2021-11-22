import os


# 保存Connect 4棋盘和游戏值的状态的游戏对象
class Game(object):
    board = None
    round = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    game_name = u"Connect 4"
    colors = ["x", "o"]

    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = None

    # 开始新的一局棋，重置一些成员变量
    def newGame(self):
        self.round = 1
        self.finished = False
        self.winner = None
        self.turn = self.players[0]
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')

    # （下完一盘棋后）双方交换棋子颜色，同时也交换先手
    def switchPlayerTurn(self):
        tempColor = self.players[1].color
        self.players[1].color = self.players[0].color
        self.players[0].color = tempColor

        # 确保 x 总是先走
        if self.players[0].color == "x":
            self.turn = self.players[0]
        else:
            self.turn = self.players[1]

    # （下完一步棋后）双方交换
    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        # 记录下了多少轮（颗棋子）
        self.round += 1

    # 下一步
    def nextMove(self):
        player = self.turn

        # 棋盘上只有42个合法的棋子位置，所以到了42棋局就结束了
        if self.round > 42:
            self.finished = True
            return

        # 获取当前棋手的move，也就是他要在哪里下棋
        move = player.move(self.board)

        # 遍历row,以获取该棋子会落到哪一行
        for row in range(6):
            if self.board[row][move] == ' ':
                # 落子
                self.board[row][move] = player.color
                # 换手
                self.switchTurn()
                # 检测是否有4连
                self.checkForFours()
                # 打印当前棋局状态
                self.printState()
                return

        # 该位置是非法的（人类棋手可能会犯错误，所以要做检查）
        print("Invalid move (column is full)")
        return

    # 检查是否有4连
    def checkForFours(self):
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    if self.verticalCheck(i, j):
                        self.finished = True
                        return
                    if self.horizontalCheck(i, j):
                        self.finished = True
                        return
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        print(slope)
                        self.finished = True
                        return

    # 检查是否有以row, col为起点的纵向4连
    def verticalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0
        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
        return fourInARow

    # 检查是否有以row, col为起点的横向4连
    def horizontalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0
        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
        return fourInARow

    # 检查是否有以row, col为起点的斜向4连
    def diagonalCheck(self, row, col):
        fourInARow = False
        count = 0
        slope = None

        # 先检查正斜
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1

        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # 再检查反斜
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope

    # （棋局结束了之后）找到4连，并高亮（大写）显示
    def findFours(self):
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    # 检查纵向
                    if self.verticalCheck(i, j):
                        self.highlightFour(i, j, 'vertical')

                    # 检查横向
                    if self.horizontalCheck(i, j):
                        self.highlightFour(i, j, 'horizontal')

                    # 检查斜向
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        self.highlightFour(i, j, 'diagonal', slope)

    # 高亮（大写）显示
    def highlightFour(self, row, col, direction, slope=None):
        if direction == 'vertical':
            for i in range(4):
                self.board[row + i][col] = self.board[row + i][col].upper()

        elif direction == 'horizontal':
            for i in range(4):
                self.board[row][col + i] = self.board[row][col + i].upper()

        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.board[row + i][col + i] = self.board[row + i][col + i].upper()

            elif slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.board[row - i][col + i] = self.board[row - i][col + i].upper()

        else:
            print("Error - Cannot enunciate four-of-a-kind")

    # 打印当前棋局状态
    def printState(self):
        os.system('clear')
        print(u"{0}!".format(self.game_name))
        print("Round: " + str(self.round))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  0   1   2   3   4   5   6 ")

        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner")
            else:
                print("Game was a draw")


# 棋手类，默认为人类棋手
class Player(object):
    type = None  # "Human" or "AI"
    name = None
    color = None

    def __init__(self, name, color):
        self.type = "Human"
        self.name = name
        self.color = color

    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        column = None
        while column == None:
            try:
                choice = int(input("Enter a move (by column number): "))
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Invalid choice, try again")
        return column


# AI棋手类，是Player的子类
class AIPlayer(Player):
    difficulty = None

    def __init__(self, name, algorithm, color, difficulty=5):
        self.type = "AI"
        self.name = name
        self.algorithm = algorithm
        self.color = color
        self.difficulty = difficulty

    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        best_move = self.algorithm.bestMove(self.difficulty, state, self.color)
        return best_move
