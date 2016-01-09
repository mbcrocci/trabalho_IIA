from random import randint


class Grid():
    def __init__(self, n_vertices, n_arestas):
        def generate_grid():
            ag = []

            for a in range(n_arestas):
                vg = []
                for v in range(n_vertices):
                    vg.append(randint(0, 1))

                ag.append(vg)

            return ag

        self.grid = generate_grid()
        self.n_vertices = n_vertices
        self.n_arestas = n_arestas

    def __repr__(self):
        string = ""
        for y in range(0, self.n_arestas):
            for x in range(0, self.n_vertices):
                string += str(self.grid[y][x]) + ' '

            string += '\n'

        return string
