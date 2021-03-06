from sys import argv
import minimum_vertex_cover as mvc
from Genetic import Pop, Solucao


def run():
    # open File
    try:
        file_name = argv[1]

    except IndexError:
        file_name = input("Enter a file name: ")

    graph, n_vertices, n_arestas = read_file(file_name)
    full_graph = {**graph[0], **graph[1]} # syntax python 3.5 (junta os 2 dicts num so)
    show_graph(full_graph)

    op = menu()

    if op == '1':
        sol_opt = pesquisa_local(graph)
        print("\nSOLUCAO: ", sol_opt)

        sol_bin = sol_in_bin(n_vertices, sol_opt)
        print("SOL BIN: ", sol_bin)

    elif op == '2':
        alg_genetico(n_vertices, full_graph)

    elif op == '3':
        hybrid(n_vertices, graph)

    else:
        print("Invalid option")


def alg_genetico(n_geracoes, graph):
    runs = int(input("N. runs: "))

    settings = get_settings()

    mbf = 0.0
    best_ever = None

    for r in range(runs):
        pop = Pop(settings, n_geracoes)
        pop.evaluate(graph)
        gen_actual = 1

        best_run = pop.get_best()

        while gen_actual < n_geracoes:
            parents = pop.tournament()
            pop = pop.genetic_operators(parents)
            pop.evaluate(graph)

            best_run = pop.get_best()
            gen_actual += 1

        invalids = 0
        for s in pop.pop:
            if not s.valido:
                invalids += 1

        print("\nRepeticao", r)
        print(best_run)
        print("\nPercentagem Invalidos:", invalids/20*100) # pop_size / 100

        mbf += best_run.fitness
        print("MBF = ", mbf)

        if r == 0 or best_run.fitness > best_ever.fitness:
            best_ever = best_run

    print("MBF: ", mbf)
    print("MELHOR SOLUCAO ENCONTRADA:")
    print(best_ever.sol)


def hybrid(n_geracoes, graph):
    """
    :param n_geracoes: igual a numero de vertices no grapho
    :param graph: tuple dos dois mapas retirados de read file
    :return:

    O Algoritmo hibrido e exactamente igual ao genetico, no entanto, introduz a solucao optima
    conseguida pela pesquisa local na populacao inicial.
    """

    sol_bin = sol_in_bin(n_geracoes, pesquisa_local(graph))
    full_graph = {**graph[0], **graph[1]} # syntax python 3.5 (junta os 2 dicts num so)

    runs = int(input("N. runs: "))
    settings = get_settings()

    mbf = 0.0
    best_ever = None

    for r in range(runs):
        pop = Pop(settings, n_geracoes)
        pop.pop[0].sol = sol_bin
        pop.evaluate(full_graph)
        gen_actual = 1

        best_run = pop.get_best()

        while gen_actual < n_geracoes:
            parents = pop.tournament()
            pop = pop.genetic_operators(parents)
            pop.evaluate(full_graph)

            best_run = pop.get_best()
            gen_actual += 1

        invalids = 0
        for s in pop.pop:
            if not s.valido:
                invalids += 1

        print("\nRepeticao", r)
        print(best_run)
        print("\nPercentagem Invalidos:", invalids/20*100) # pop_size / 100

        mbf += best_run.fitness
        print("MBF = ", mbf)

        if r == 0 or best_run.fitness > best_ever.fitness:
            best_ever = best_run

    print("MBF: ", mbf)
    print("MELHOR SOLUCAO ENCONTRADA:")
    print(best_ever.sol)


def pesquisa_local(graph):
    # MINIMUM VERTEX COVER
    print("\nMVC")

    # calcula o minimum vertex cover
    m = mvc.min_vertex_cover(graph[0], graph[1])
    show_graph(m)
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
    sol_list = all_vert(graph)
    for v in m:
        for u in m[v]:
            try:
                sol_list.remove(u)

            except ValueError:
                pass

    return sol_list


def all_vert(graph):
    # Criar uma lista com todos os vertices
    keys = list(graph[0].keys()) + list(graph[1].keys())
    all_vertices = []
    for v in keys:
        if v not in all_vertices:
            all_vertices.append(v)

    return all_vertices


def sol_in_bin(n_vertices, sol_list):
    sol = []

    for v in range(n_vertices):
        sol.append(0)

    for v in sol_list:
        sol[v-1] = 1

    return sol


def menu():
    print("1 - Pesquisa Local")
    print("2 - Algoritmo Genetico")
    print("3 - Algoritmo hibrido")

    op = input("Option: ")
    return op


def get_settings():
    op = input("Enter 1 for default settings 2 for costumized: ")
    if op == '1':
        pop_size = 20
        prob_mut = 0.01
        prob_rec = 0.7
        max_gen = 100

    else:
        pop_size = int(input("Pop size: "))
        prob_mut = float(input("Probabilidade de mutacao: "))
        prob_rec = float(input("Probabilidade de reprocriacao: "))
        max_gen = int(input("Max. Geracoes: "))

    return [pop_size, prob_mut, prob_rec, max_gen]


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
                n_vertices = int(l[2])
                n_arestas = int(l[3])

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