class Grid:
    def __init__(self, n_vertices, graph):
        self.grid = [[]]
        self.n_vertices = n_vertices
        self.graph = graph
        self.generate_grid()

    def generate_grid(self):
        def generate_grid_0():
            vg = []
            for vt in range(self.n_vertices):
                ag = []
                for ar in range(self.n_vertices):
                    ag.append(0)

                vg.append(ag)

            return vg

        self.grid = generate_grid_0()

        for v in range(self.n_vertices):
            for j in range(1,len(self.graph[v+1])):
                l = 0

                while l+1 != self.graph[v+1][j] and l < self.n_vertices:
                    l += 1

                self.grid[v][j] = 1


    def __repr__(self):
        string = ""
        for x in range(0, self.n_vertices-1):
            for y in range(0, self.n_vertices-1):
                string += str(self.grid[x][y]) + ' '

            string += '\n'

        return string
