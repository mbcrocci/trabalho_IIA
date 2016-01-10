from random import randint, uniform


class Solucao:
    def __init__(self, n_vertices):
        self.sol = []
        self.fitness = 0
        self.valido = True

        self.gerar_sol(n_vertices)

    def gerar_sol(self, n_vertices):
        for v in range(n_vertices):
            self.sol.append(randint(0, 1))

    def __str__(self):
        return str(self.sol)


class Pop:
    def __init__(self, settings, n_genes):
        self.n_genes = n_genes
        self.settings = settings

        self.pop_size = settings[0]
        self.prob_mut = settings[1]
        self.prob_rec = settings[2]
        self.max_gen = settings[3]

        self.pop = self.gera_pop_init()

    def gera_pop_init(self):
        pop = []
        for i in range(self.pop_size):
            s = Solucao(self.n_genes)
            pop.append(s)

        return pop

    def evaluate(self, graph):
        # (TODO): Ver se este fitness pode ser calculado de outra maneira
        for s in self.pop:
            s.fitness = sum(s.sol)
            # por cada elemento da solucao
            for i, b1 in enumerate(s.sol):
                # se for 1 (index+1 pertence a solucao)
                if b1 == 1:
                    # percorre outra vez a solucao e ve se aquele vertice conhece algum outro
                    for j, b2 in enumerate(s.sol):
                        if i != j and b2 == 1:
                            if i in graph[j+1] or j in graph[i+1]:
                                s.valido = False
                                break

    def get_best(self):
        best = Solucao(self.n_genes)
        best.fitness = self.n_genes
        for s in self.pop:
            if s.fitness < best.fitness:
                best = s

        return best

    def tournament(self):
        parents = Pop(self.settings, self.n_genes)
        for i in range(0, self.pop_size-1):
            x1 = randint(0, self.pop_size-1)
            x2 = randint(0, self.pop_size-1)

            while x1 == x2:
                x2 = randint(0, self.pop_size-1)

            # so lhe interessa aquelas que sao validas
            if self.pop[x1].valido and self.pop[x2].valido:
                if self.pop[x1].fitness > self.pop[x2].fitness:
                    parents.pop[i] = self.pop[x1]

                else:
                    parents.pop[i] = self.pop[x2]

        return parents

    def genetic_operators(self, parents):
        descendents = self.crossover(parents)
        descendents = self.mutation(descendents)
        return descendents

    def crossover(self, parents):
        offspring = Pop(self.settings, self.n_genes)
        offspring.gera_pop_init()

        for i in range(0, self.pop_size-1):
            if uniform(0.0, 1.0) < self.prob_rec:
                point = randint(0, self.n_genes)
                for j in range(0, point):
                    offspring.pop[i].sol[j] = parents.pop[i].sol[j]
                    offspring.pop[i+1].sol[j] = parents.pop[i+1].sol[j]

                for j in range(point, self.n_genes):
                    offspring.pop[i].sol[j] = parents.pop[i].sol[j]
                    offspring.pop[i+1].sol[j] = parents.pop[i+1].sol[j]

            else:
                offspring.pop[i] = parents.pop[i]
                offspring.pop[i+1] = parents.pop[i+1]

            offspring.pop[i].fitness = 0.0
            i += 1

        return offspring

    def mutation(self, offspring):
        for i in range(0, self.pop_size):
            for j in range(0, self.n_genes):
                if uniform(0.0, 1.0) < self.prob_mut:
                    if offspring.pop[i].sol[j] == 1:
                        offspring.pop[i].sol[j] = 0

                    else:
                        offspring.pop[i].sol[j] = 1

        return offspring
