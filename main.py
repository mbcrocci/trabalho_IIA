from sys import argv
from collections import defaultdict
import minimum_vertex_cover as mvc


class Graph:
    """
    Graph representa um grafo.

    Este contem um dicionario de todos os nos e suas ligacoes:
    Exemplo:
        A : [B, C, D]
        B : [D, A]
        C : [D]


    minimum vertex cover: https://en.wikipedia.org/wiki/K%C5%91nig%27s_theorem_(graph_theory)


    """
    def __init__(self, connections, directed=False):
        self.graph = defaultdict(set)
        self.directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        for parent, child in connections:
            self.add(parent, child)

    def add(self, parent, child):
        self.graph[parent].add(child)
        if not self.directed:
            self.graph[child].add(parent)

    def is_connected(self, node1, node2):
        return node1 in self.graph and node2 in self.graph[node1]

    def neighbours(self, id):
        return self.graph[id]

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self.graph))


def run():
    # open File
    try:
        file_name = argv[1]

    except IndexError:
        file_name = input("Enter a file name: ")


    graph, n_vertices, n_arestas = read_file(file_name)

    # MINIMUM VERTEX COVER
    print("\nMVC")

    # calcula o minimum vertex cover
    m = mvc.min_vertex_cover(graph[0], graph[1])
    print(m)

    """
        Sendo A   - conjunto de todos os vertices
              I   - conjunto de todos os vertices independentes
              EC  - total vertex cover
              MVC - Minimum vertex cover

              A = I + EC
              I = A - MVC
    """
    all_vertices = [i for i in range(1, n_vertices)] # (TODO): construir isto melhor
    for v in m:
        for u in m[v]:
            try:
                all_vertices.remove(u)

            except ValueError:
                pass

    print(all_vertices)



def read_file(file_name):
    """
    :param file_name: nome do ficheiro a abrir
    :return: left_v, right_v, n_vertices, n_arestas

    Le o ficheiro extraindo o numero de vertices e numero de arestas
    na linha que lhe corresponde (aquela que comeca por 'p')

    Nas linhas que comecam por 'e', tira as ligacoes e cria 2 dicionarios, left_v e right_v.
    left_v: dict em que as keys sao os vertices que se encontram a esquerda nas ligacoes
            e o 'value' e uma lista de vertices que se encontram a direita nas ligacoes

    right_v: mesmo que o left mas da direita para a esquerda
    """

    left_v = {} # dicionario que contem para cada vertice a esquerda da ligacao todos os que lhe correspondem a direita
    right_v = {} # mesmo que left_v, mas da direita para a esquerda
    with open(file_name, 'r') as graph:
        for edge in graph:  # por cada linha
            if edge.startswith('p'):
                l = edge.split(' ')
                n_arestas = int(l[2])
                n_vertices = int(l[3])

            if edge.startswith('e'):
                e = edge.split(' ')
                try:
                    left_v[int(e[1])].append(int(e[2]))

                except KeyError:
                    left_v[int(e[1])] = [int(e[2])]

                try:
                    right_v[int(e[2])].append(int(e[1]))

                except KeyError:
                    right_v[int(e[2])] = [int(e[1])]

    return [left_v, right_v], n_vertices, n_arestas

if __name__ == '__main__':
    run()