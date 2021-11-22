from algorithms import *


# 这是一个测试类，用来测试某个算法在某一步的输出结果，帮助你快速地debug


# 打印棋盘状态
def printState(board):
    for i in range(5, -1, -1):
        print("\t", end="")
        for j in range(7):
            print("| " + str(board[i][j]), end=" ")
        print("|")
    print("\t  _   _   _   _   _   _   _ ")
    print("\t  0   1   2   3   4   5   6 ")


# 棋盘状态
board = [['x', 'x', 'x', 'o', 'o', 'x', 'o'], [' ', 'x', 'x', 'o', 'x', 'o', 'o'],
         [' ', 'x', 'x', 'x', ' ', 'o', 'o'],
         [' ', 'o', 'o', ' ', ' ', ' ', 'x'], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
printState(board)

m = Minimax()
print("Finding best move for o...")
print(m.bestMove(4, board, 'o'))
