# 节点类，记录节点的值和子节点集合
class Node:

    def __init__(self, value=0, children={}):
        self.value = value
        self.children = children


# 最大节点类，继承自节点类
class MaxNode(Node):
    def get_value(self):
        temp = -65535
        for child in self.children:
            if child.value > temp:
                temp = child.value
        self.value = temp
        return temp


# 最小节点类，继承自节点类
class MinNode(Node):
    def get_value(self):
        temp = 65535
        for child in self.children:
            if child.value < temp:
                temp = child.value
        self.value = temp
        return temp


# 机会节点类，继承自节点类
class ChanceNode(Node):
    def get_value(self):
        temp = 0
        for child in self.children:
            temp += child.value / len(self.children)
        self.value = temp
        return temp


print("======first tree=======")
node_A = MinNode(children={Node(6), Node(9), Node(5)})
node_B = MinNode(children={Node(3), Node(4), Node(8)})
node_C = MinNode(children={Node(1), Node(7), Node(2)})
node_D = MaxNode(children={node_A, node_B, node_C})
print("A:", node_A.get_value())
print("B:", node_B.get_value())
print("C:", node_C.get_value())
print("D:", node_D.get_value())

print()
print("======second tree=======")
node_A = ChanceNode(children={Node(15), Node(9), Node(33)})
node_B = ChanceNode(children={Node(24), Node(3), Node(30)})
node_C = ChanceNode(children={Node(18), Node(6), Node(27)})
node_D = ChanceNode(children={Node(21), Node(12), Node(0)})
node_E = MinNode(children={node_A, node_B})
node_F = MinNode(children={node_C, node_D})
node_G = MaxNode(children={node_E, node_F})
print("A:", node_A.get_value())
print("B:", node_B.get_value())
print("C:", node_C.get_value())
print("D:", node_D.get_value())
print("E:", node_E.get_value())
print("F:", node_F.get_value())
print("G:", node_G.get_value())
