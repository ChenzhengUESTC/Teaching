# 搜索算法，values:A-Star, UCS, Greedy
algorithm = "A-Star"


# 节点类
class Node:
    def __init__(self, name="", children={}, h_value=0):
        """"初始化方法"""
        self.name = name
        self.children = children
        self.h_value = h_value

    name = ""
    children = {}
    father = None
    f_value = 0
    h_value = 0
    g_value = 0


# 构造图
Goal = Node("Goal", {}, 0)
D = Node("D", {Goal: 4}, 2)
C = Node("C", {Goal: 7}, 1)
B = Node("B", {D: 5}, 3)
A = Node("A", {B: 1, C: 3, D: 1}, 3)
Start = Node("Start", {A: 2, B: 1}, 0)

# 搜索前沿
fringe = [Start]

# 闭集
closed_set = set()

while len(fringe) > 0:
    # 根据不同的搜索算法，对搜索前沿进行排序
    if algorithm == "A-Star":
        fringe.sort(key=lambda x: x.f_value)
    elif algorithm == "UCS":
        fringe.sort(key=lambda x: x.g_value)
    elif algorithm == "Greedy":
        fringe.sort(key=lambda x: x.h_value)

    # 取出当前最"小"的节点，加入闭集
    node = fringe.pop(0)
    closed_set.add(node)
    print("poped: " + node.name + "(" + (node.father.name if node.father != None else 'none') + ")",
          "\tfringe: " + " ".join(v.name + "(" + v.father.name + ")" for v in fringe),
          "\tclosed_set: " + " ".join(v.name for v in closed_set))

    # 如果目标节点被取出搜索前沿，则搜索结束
    if node == Goal:
        print("Find goal, search ends.")
        route = [node.name]
        while node.father != None:
            node = node.father
            route.append(node.name)
        route.reverse()
        print("The route is: " + " ".join(route))
        break

    # 将节点的子节点都加入搜索前沿，并且计算其g和f值
    for child in node.children:
        if child in closed_set:
            # 已经被搜索过了，不要在搜索了
            continue
        if child in fringe:
            # 在搜索前沿里面，但是还没有被搜索，考察之前的路径和当然的路径哪个更近一些
            if child.g_value < node.g_value + node.children[child]:
                continue
        else:
            fringe.append(child)
        child.father = node
        child.g_value = node.g_value + node.children[child]
        child.f_value = child.g_value + child.h_value
        print("node " + child.name + " added into the fringe.")

