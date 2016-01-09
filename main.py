from sys import argv
import minimum_vertex_cover as mvc
from Grid import Grid


def run():
    # open File
    try:
        file_name = argv[1]

    except IndexError:
        file_name = input("Enter a file name: ")

    graph, n_vertices, n_arestas = read_file(file_name)

    graph_show = {**graph[0], **graph[1]} # syntax python 3.5 (junta os 2 dicts num so)
    show_graph(graph_show)

    # Criar uma lista com todos os vertices
    keys = list(graph[0].keys()) + list(graph[1].keys())
    all_vertices = []
    for v in keys:
        if v not in all_vertices:
            all_vertices.append(v)

    print("\nTODOS OS VERTICES")
    print(all_vertices)

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

    # remover da lista que contem todos os vertices
    # os valors que estao no mvc
    sol_list = all_vertices.copy()
    for v in m:
        for u in m[v]:
            try:
                sol_list.remove(u)

            except ValueError:
                pass

    print("\nSOLUCAO: tam =", len(sol_list))
    print(sol_list)

    sol_bin = []
    sol_bin = sol_inicial(all_vertices, sol_list)

    g = Grid(n_vertices, n_arestas)

    print(g)


def sol_inicial(all_vertices, sol_list):
    sol = []

    for v in all_vertices:
        if v in sol_list:
            sol.append(1)

        else:
            sol.append(0)

    return sol


def show_graph(graph):
    string = ""
    for k in graph:
        string += str(k) + ": ["
        for v in graph[k]:
            string += str(v) + ' '

        string += "]\n"

    print(string)


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