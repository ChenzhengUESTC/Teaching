import sys
import copy
from datetime import datetime

sudoku_file_loc = 'input0.txt'
soln_file_loc = 'solution.txt'

num_of_iteration = 0

# 每个位置的领接位置集合
neighbours = {}


def initial_neighours():
    for row in range(9):
        for col in range(9):
            neighbour = get_connecting_cells_positions((row, col))
            neighbours[(row, col)] = neighbour
    return neighbours


# 以列表的形式返回连接到给定位置的所有单元格（同一行/同一列/同一宫）。
def get_connecting_cells_positions(position):
    row, col = position
    output = list()
    for col_value in range(9):  # Items in same row
        if col_value != col:
            output.append((row, col_value))
    for row_value in range(9):  # Items in same col
        if row_value != row:
            output.append((row_value, col))
    top_row_in_box = int(row / 3) * 3  # Items in the same box
    top_col_in_box = int(col / 3) * 3
    for same_box_row_value in range(top_row_in_box, top_row_in_box + 3):
        for same_box_col_value in range(top_col_in_box, top_col_in_box + 3):
            if same_box_row_value != row and same_box_col_value != col:
                output.append((same_box_row_value, same_box_col_value))
    return output


# 将puzzle中的所有值初始化为一组值.
# 如果存在预先存在的值，我们将其设置为单个值的集合.
# 如果值为0，我们将其设置为一个包含了1-9数值的集合，也就是该位置的所有可能取值.
def initialise(puzzle):
    initial_neighours()
    new_puzzle = [[{1, 2, 3, 4, 5, 6, 7, 8, 9} for i in range(9)] for j in range(9)]
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] != 0:
                assign(new_puzzle, (row, col), puzzle[row][col])
    puzzle = new_puzzle
    return puzzle


# 将puzzle中的每个位置的集合转为单一的值，以便输出.
def convert_to_output(puzzle):
    ans = copy.deepcopy(puzzle)
    for row in range(9):
        for col in range(9):
            for value in puzzle[row][col]:
                ans[row][col] = value
    return ans


# 回溯搜索
def backtrack(puzzle):
    # 检查每行、每列和每宫(3x3框)是否合法
    if not analyse_domains(puzzle):
        return False, puzzle

    # 遍历puzzle，找出一个包含了多个候选数字的位置
    h_row = -1
    h_col = -1
    for row in range(9):
        for col in range(9):
            if len(puzzle[row][col]) > 1:
                h_row = row
                h_col = col
    # 先选择哪一个候选位置？这里可以应用最小剩余值 (Minimum remaining values -- MRV)原则

    # puzzle中每个位置都只有1个候选数字，则该puzzle已经成功求解了
    if h_row == -1 and h_col == -1:
        return True, puzzle

    # 候选赋值集合
    h_values = puzzle[h_row][h_col].copy()

    # 尝试按照候选赋值集合中的值对该位置进行赋值:
    # 先选择哪一个value？这里可以应用最小制约的值 (Least Constraining Value -- LCV)原则
    for value in h_values:
        current_puzzle = copy.deepcopy(puzzle)
        current_puzzle[h_row][h_col] = set()
        current_puzzle[h_row][h_col].add(value)
        # 将current_puzzle中的位置(h_row, h_col)赋值为value
        # 赋值会失败吗？
        if not assign(current_puzzle, (h_row, h_col), value):
            continue

        # 迭代进行回溯搜索
        result = backtrack(current_puzzle)
        succ, current_puzzle = result
        if succ:
            return succ, current_puzzle

    # 所有尝试都没有return，说明尝试失败了，得回溯
    return False, current_puzzle


def analyse_domains(puzzle):
    # 检查每一行中，是否存在着重复赋值
    for row in range(9):
        assigned_values = set()
        for col in range(9):
            if len(puzzle[row][col]) == 1:
                assigned_value = next(iter(puzzle[row][col]))
                if assigned_value in assigned_values:
                    return False
                assigned_values.add(assigned_value)

    # 检查每一列中，是否存在着重复赋值
    for col in range(9):
        assigned_values = set()
        for row in range(9):
            if len(puzzle[row][col]) == 1:
                assigned_value = next(iter(puzzle[row][col]))
                if assigned_value in assigned_values:
                    return False
                assigned_values.add(assigned_value)

    # 检查每一宫（3x3 small box）中，是否存在着重复赋值
    small_boxes = []
    large_boxes = []
    boxes_list = []
    # Creates boxes_list, which is a list of 3z3 small_boxes
    for i in range(3):
        for j in range(3):
            small_boxes.append((i, j))
            large_boxes.append((i * 3, j * 3))
    for large_box in large_boxes:
        boxes = []
        for small_box in small_boxes:
            boxes.append((small_box[0] + large_box[0], small_box[1] + large_box[1]))
        boxes_list.append(boxes)

    for small_box in boxes_list:
        assigned_values = set()
        for single_box in small_box:
            row = single_box[0]
            col = single_box[1]
            if len(puzzle[row][col]) == 1:
                assigned_value = next(iter(puzzle[row][col]))
                if assigned_value in assigned_values:
                    return False
                assigned_values.add(assigned_value)

    return True


# 将puzzle中的位置position赋值为value
def assign(puzzle, position, value):
    global num_of_iteration
    num_of_iteration = num_of_iteration + 1
    row, col = position
    puzzle[row][col] = set()
    puzzle[row][col].add(value)

    # 赋值完了可以做前向检查(forward checking)，减少puzzle中可取值集合的大小，
    # 也有可能导致赋值失败（某个位置的可选value集合为空），从而更快地进行回溯
    # 检查完了还可以做约束传播(Constraint Propagation)，进一步减少puzzle中可取值集合的大小，
    # 也有可能更快地导致赋值失败，从而更快地进行回溯

    return True


def load_puzzle(sudoku_file_loc):
    # 读取数独题目文件，读入到puzzle二维数组中
    try:
        f = open(sudoku_file_loc, 'r')
    except IOError:
        print("Input file not found!")
        sys.exit()

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    return puzzle


def write_solution(puzzle, soln_file_loc):
    with open(soln_file_loc, 'w') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(puzzle[i][j]) + " ")
            f.write("\n")


def print_puzzle(puzzle):
    for line in puzzle:
        for num in line:
            print(num, end=" ")
        print()


if __name__ == "__main__":
    # 从文件中读取puzzle
    puzzle = load_puzzle(sudoku_file_loc)

    # 打印初始puzzle
    print("-" * 5, "puzzle", "-" * 4)
    print_puzzle(puzzle)
    print("-" * 17)

    start = datetime.now()

    # 初始化puzzle
    puzzle = initialise(puzzle)

    # 回溯搜索
    succ, puzzle = backtrack(puzzle)

    if succ:
        end = datetime.now()
        print("Solve the puzzle within :", end - start, ", with", num_of_iteration, "iterations.")

        # 做一下结果的转换，并且打印结果
        ans = convert_to_output(puzzle)
        print("-" * 5, "answer", "-" * 4)
        print_puzzle(ans)
        print("-" * 17)

        # 结果保存到文件中
        write_solution(ans, soln_file_loc)
