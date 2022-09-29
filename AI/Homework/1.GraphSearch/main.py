# 请加入注释...
class Node:
    # 请加入注释...
    all_nodes = list()

    # 请加入注释...
    def __init__(self, name, h):
        self.h = h
        self.name = name
        Node.all_nodes.append(self)

    # 请加入注释...
    def __str__(self):
        return "Node-" + self.name + "(" + str(self.f) + "," + str(self.g) + "," + str(self.h) + ")"


# 请加入注释...
class Edge:
    # 请加入注释...
    all_edges = list()

    # 请加入注释...
    def __init__(self, head, tail, cost):
        self.head = head
        self.tail = tail
        self.cost = cost
        Edge.all_edges.append(self)


# 请加入注释...
class Graph:
    # 请加入注释...
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    # 请加入注释...
    def find_next_nodes(self, node):
        next_nodes = list()
        if node not in self.nodes:
            return next_nodes
        for edge in self.edges:
            if edge.head == node:
                next_nodes.append(edge.tail)
        return next_nodes

    # 请加入注释...
    def find_edge(self, head, tail):
        for edge in self.edges:
            if edge.head == head and edge.tail == tail:
                return edge
        return None


# 请加入注释...
if __name__ == '__main__':

    # A-star, UCS, Greedy, BFS, DFS
    search_algorithm = "Greedy"

    # 请加入注释...
    node_S = Node("S", 0)
    node_a = Node("a", 3)
    node_b = Node("b", 3)
    node_c = Node("c", 1)
    node_d = Node("d", 2)
    node_G = Node("G", 0)

    # 请加入注释...
    edge_Sa = Edge(node_S, node_a, 2)
    edge_Sb = Edge(node_S, node_b, 1)
    edge_ab = Edge(node_a, node_b, 1)
    edge_ac = Edge(node_a, node_c, 3)
    edge_ad = Edge(node_a, node_d, 1)
    edge_bd = Edge(node_b, node_d, 5)
    edge_cG = Edge(node_c, node_G, 7)
    edge_dG = Edge(node_d, node_G, 4)
    edge_bG = Edge(node_b, node_G, 10)

    # 请加入注释...
    graph = Graph(Node.all_nodes, Edge.all_edges)

    # 请加入注释...
    fringe = list()
    # 请加入注释...
    closed_set = set()

    # 请加入注释...
    node_S.g = 0
    node_S.f = node_S.g + node_S.h
    # 请加入注释...
    fringe.append(node_S)

    # 请加入注释...
    while len(fringe) > 0:

        # 请加入注释...
        if search_algorithm == "A-star":
            fringe.sort(key=lambda x: x.f, reverse=True)
        # 请加入注释...
        elif search_algorithm == "UCS":
            fringe.sort(key=lambda x: x.g, reverse=True)
        # 请加入注释...
        elif search_algorithm == "Greedy":
            fringe.sort(key=lambda x: x.h, reverse=True)

        # 请加入注释...
        node_current = fringe.pop()
        print(node_current)
        print(*fringe)
        print(*closed_set)
        print()

        # 请加入注释...
        if node_current == node_G:
            print("Found route.")
            break

        # 请加入注释...
        closed_set.add(node_current)

        # 请加入注释...
        next_nodes = graph.find_next_nodes(node_current)
        if len(next_nodes) > 0:
            # 请加入注释...
            for node in next_nodes:
                # 请加入注释...
                if node in closed_set:
                    continue
                # 请加入注释...
                elif node in fringe:
                    temp_g = node_current.g + graph.find_edge(node_current, node).cost
                    temp_f = temp_g + node.h
                    if search_algorithm == "Greedy":
                        continue
                    if search_algorithm == "A-star" and temp_f >= node.f:
                        continue
                    if search_algorithm == "UCS" and temp_g >= node.g:
                        continue
                # 请加入注释...
                node.fore_node = node_current
                node.g = node_current.g + graph.find_edge(node_current, node).cost
                node.f = node.g + node.h
                # 请加入注释...
                fringe.append(node)

    # 请加入注释...
    route = list()
    route_cost = 0
    route.append(node_G)
    node_current = node_G
    fore_node = node_current.fore_node
    # 请加入注释...
    while fore_node != node_S:
        route.insert(0, fore_node)
        route_cost += graph.find_edge(fore_node, node_current).cost
        node_current = fore_node
        fore_node = node_current.fore_node
    # 请加入注释...
    route.insert(0, node_S)
    route_cost += graph.find_edge(node_S, node_current).cost

    # 请加入注释...
    print(*route)
    print(route_cost)
