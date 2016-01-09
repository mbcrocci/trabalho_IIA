class Grid:
    def __init__(self, n_vertices, graph):
        def generate_grid_0():
            vg = []
            for v in range(n_vertices):
                ag = []
                for a in range(n_vertices):
                    ag.append(0)

                vg.append(ag)

            return vg

        self.grid = generate_grid_0()
        self.n_vertices = n_vertices
        self.graph = graph

        for k in self.graph.keys():
            for a in self.graph[k]:
                l = 0
                while l+1 != len(self.graph[k]) and l < n_vertices:
                    l += 1

                self.grid[k][a] = 1

    def __repr__(self):
        string = ""
        for x in range(0, self.n_vertices-1):
            for y in range(0, self.n_vertices-1):
                string += str(self.grid[x][y]) + ' '

            string += '\n'

        return string
