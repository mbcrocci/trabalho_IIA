from sys import argv


class Node:
    def __init__(self, name):
        self.name = name
        self.parent = Node
        self.childs = []

    def __repr__(self):
        string = "< Node: " + str(self.name)

        if self.childs:
            string += "  Childs:"
            for child in self.childs:
                string += " " + str(child)

        string += " >"

        return string



def exist_node(name, node_list):
    for n in node_list:
        if n.name == name:
            return True, n

    return False, Node(0)


def run():
    # open File

    try:
        file_name = argv[1]

    except IndexError:
        file_name = input("Enter a file name: ")

    connections_list = []
    connections_list, n_vertices, n_arestas = read_file(file_name, connections_list)

    print(connections_list)


    node_list = create_node_list(connections_list)

    print("\n\n")
    for node in node_list:
        print(node)


def create_node_list(connections_list):
    parents = []
    childs = []
    for c in connections_list:
        if c[0] not in parents:
            parents.append(c[0])

        if c[1] not in childs:
            childs.append(c[1])

    # convert every parent to an Object
    parent_nodes = [Node(p) for p in parents]

    for p in parent_nodes:
        for c in connections_list:
            if c[0] == p.name:
                p.childs.append(Node(c[1]))

    return parent_nodes


def read_file(file_name, connection_list):
    with open(file_name, 'r') as f:
        n_vertices, n_arestas = 0, 0

        for line in f.readlines():
            if line.startswith('p'):
                l = line.split(' ')
                n_arestas = int(l[2])
                n_vertices = int(l[3])

            if line.startswith('e'):
                l = line.split(' ')

                parent = int(l[1])
                child = int(l[2])

                connection_list.append((parent, child))

    return connection_list, n_vertices, n_arestas

if __name__ == '__main__':
    run()