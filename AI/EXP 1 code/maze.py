import copy
import codecs
from datetime import datetime

maze_file_loc = 'Maze.txt'
soln_file_loc = 'Maze_solution.txt'

# 迷宫文件中，x表示墙，空格表示路
blocked_tile = 'X'
free_tile = ' '


# 生成下一个可能的路径
def Next_State_Generator(maze, current_location, visited_locations):
    max_vertical = len(maze) - 1
    max_horizontal = len(maze[0]) - 1

    allowed_location_1 = None
    allowed_location_2 = None
    allowed_location_3 = None
    allowed_location_4 = None
    next_states = list()

    # UP
    # Check if UP location is inside the maze
    if (current_location[0] - 1 >= 0):
        # Check if it is possible to move UP
        if (maze[current_location[0] - 1][current_location[1]] == free_tile):
            # check if the path was already visited
            if ([current_location[0] - 1, current_location[1]] not in visited_locations):
                allowed_location_1 = [current_location[0] - 1, current_location[1]]
                next_states.append(allowed_location_1)

    # DOWN
    # Check if DOWN location is inside the maze
    if (current_location[0] + 1 <= max_vertical):
        # Check if it is possible to move DOWN
        if (maze[current_location[0] + 1][current_location[1]] == free_tile):
            # check if the path was already visited
            if ([current_location[0] + 1, current_location[1]] not in visited_locations):
                allowed_location_2 = [current_location[0] + 1, current_location[1]]
                next_states.append(allowed_location_2)
    # LEFT
    # Check if LEFT location is inside the maze
    if (current_location[1] - 1 >= 0):
        # Check if it is possible to move LEFT
        if (maze[current_location[0]][current_location[1] - 1] == free_tile):
            # check if the path was already visited
            if ([current_location[0], current_location[1] - 1] not in visited_locations):
                allowed_location_3 = [current_location[0], current_location[1] - 1]
                next_states.append(allowed_location_3)
    # RIGHT
    # Check if RIGHT location is inside the maze
    if (current_location[1] + 1 <= max_horizontal):
        # Check if it is possible to move RIGHT
        if (maze[current_location[0]][current_location[1] + 1] == free_tile):
            # check if the path was already visited
            if ([current_location[0], current_location[1] + 1] not in visited_locations):
                allowed_location_4 = [current_location[0], current_location[1] + 1]
                next_states.append(allowed_location_4)

    return next_states


# 将解决方案打印到.txt文件
def Create_Solution_Map(maze, path_trace):
    fileP = codecs.open(soln_file_loc, mode="w", encoding="utf16")
    maze_string = str()

    # 要打印到.txt文件中的Unicode字符（箭头）
    down_arrow = '\u25BC'
    up_arrow = '\u25B2'
    left_arrow = '\u25C4'
    right_arrow = '\u25BA'

    # 在地图上放置箭头
    i = 0
    for loc in path_trace:
        if (i != len(path_trace) - 1):
            if (loc[0] > path_trace[i + 1][0]):
                maze[loc[0]][loc[1]] = up_arrow

            if (loc[0] < path_trace[i + 1][0]):
                maze[loc[0]][loc[1]] = down_arrow

            if (loc[1] > path_trace[i + 1][1]):
                maze[loc[0]][loc[1]] = left_arrow

            if (loc[1] < path_trace[i + 1][1]):
                maze[loc[0]][loc[1]] = right_arrow

        i = i + 1

    for lineX in maze:
        for charX in lineX:
            maze_string = maze_string + charX

    fileP.write('Solution :\n' + maze_string + '\n\nFull Path - \n' + str(path_trace))


# 读取迷宫文件，并解析出开始点和目标点位置
def load_maze(maze_file_loc):
    maze_file = open(maze_file_loc, 'r')

    maze = list()
    for lineX in maze_file:
        lineX = list(lineX)
        maze.append(lineX)

    for lineX in maze:
        for char in lineX:
            print(char, end='')

    # 找到开始点和目标点位置
    start_i = 0
    start_j = 0
    goal_i = 0
    goal_j = 0

    found_s = False
    found_g = False

    i = 0
    j = 0
    for maze_lineX in maze:
        for maze_char in maze_lineX:
            # Search for 'S'
            if maze_char == 'S':
                start_i = i
                start_j = j
                found_s = True
                break
            j = j + 1
        i = i + 1
        j = 0

        if found_s:
            break

    i = 0
    j = 0
    for maze_lineX in maze:
        for maze_char in maze_lineX:
            # Search for 'G'
            if maze_char == 'G':
                goal_i = i
                goal_j = j
                found_g = True
                break
            j = j + 1
        i = i + 1
        j = 0

        if found_g:
            break

    if found_s and found_g:
        print()
        print("Found start point:", start_i, start_j)
        print("Found goal point:", goal_i, goal_j)

    start_location = [start_i, start_j]
    goal_location = [goal_i, goal_j]
    maze[goal_i][goal_j] = free_tile
    maze[start_i][start_j] = free_tile
    return maze, start_location, goal_location


# 深度优先搜索
def DFS_search(maze, start_location, goal_location):
    # 当前位置
    current_location = start_location
    # 访问过的位置
    visited_locations = list()
    # 记录路径，最终会通过这个dict中的记录来生成路径
    traceBack_dict = {'START': current_location}
    # 迭代的次数
    Number_Of_iterations = 0

    # 通过当前位置和已访问过的位置，找出下一步行动的全部可能位置
    next_Locations = Next_State_Generator(maze, current_location, visited_locations)
    # 要用deepcopy，确保新生成一个available_location对象
    available_location = copy.deepcopy(next_Locations)
    visited_locations.append(current_location)

    # 在traceBack_dict中记录，是从current_location到达的locationX
    for locationX in next_Locations:
        traceBack_dict.update({str(locationX): current_location})

    while available_location and current_location != goal_location:
        # current_location移动到可移动的第一个位置
        current_location = available_location[0]
        # 删去已被移动的位置
        available_location = available_location[1:]
        next_Locations = Next_State_Generator(maze, current_location, visited_locations)
        for locationX in next_Locations:
            traceBack_dict.update({str(locationX): current_location})
            # 插入在表头，所以是深度优先。
            available_location.insert(0, locationX)
            # 如果插入在表尾，那就是广度优先。
            # available_location.append(locationX)
        visited_locations.append(current_location)
        Number_Of_iterations = Number_Of_iterations + 1

    if current_location == goal_location:
        path_trace = list()
        # 通过traceBack_dict反向寻找构建path_trace
        while current_location != start_location:
            path_trace.append(current_location)
            current_location = traceBack_dict[str(current_location)]
        path_trace = path_trace + [start_location]
        path_trace.reverse()
        return path_trace, Number_Of_iterations
    else:
        return None, Number_Of_iterations


if __name__ == '__main__':

    maze, start_location, goal_location = load_maze(maze_file_loc)

    start_time = datetime.now()
    path_trace, Number_Of_iterations = DFS_search(maze, start_location, goal_location)
    time_consumed = datetime.now() - start_time

    if path_trace is not None:
        print('Path = ' + str(path_trace))
        Create_Solution_Map(maze, path_trace)
        print('\nNumber of iterations = ' + str(Number_Of_iterations))
        print('Path length = ' + str(len(path_trace)))
        print('Time consumed = ', time_consumed)
    else:
        print('No path Found - ' + str(Number_Of_iterations))
        input('Press enter')
