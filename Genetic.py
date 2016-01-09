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
    def __init__(self, pop_size, prob_mut, prob_rec, n_genes, max_gen):
        self.pop_size = pop_size
        self.prob_mut = prob_mut
        self.prob_rec = prob_rec
        self.n_genes = n_genes
        self.max_gen = max_gen
        self.pop = self.gera_pop_init()

    def gera_pop_init(self):
        pop = []
        for i in range(self.pop_size):
            s = Solucao(self.n_genes)
            pop.append(s)

        return pop

    def evaluate(self):
        for s in self.pop:
            s.fitness = self.evaluate_sol(s)

    def evaluate_sol(self, s):
        ft = 0
        # (TODO): Ver se este fitness pode ser calculado de outra maneira§
        for i in range(0, self.n_genes-1):
            if s.sol[i] == 1:
                for j in range(0, self.n_genes-1):
                    if i != j and s.sol[j] == 1:
                        ft -= 1

        if ft == 0:
            for i in range(0, self.n_genes-1):
                if s.sol[i] == 1:
                    ft += 1

        return ft

    def get_best(self):
        best = Solucao(self.n_genes)
        for s in self.pop:
            if s.fitness < best.fitness:
                best = s

        return best

    def tournament(self, parents):
        for i in range(0, self.pop_size-1):
            x1 = randint(0, self.pop_size-1)
            x2 = randint(0, self.pop_size-1)

            while x1 == x2:
                x2 = randint(0, self.pop_size-1)

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
        offspring = Pop(pop_size=20, prob_mut=0.01, prob_rec=0.7, n_genes=self.n_genes, max_gen=100)
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
