import random


class TSPGeneticAlgorithm:
    def __init__(self, *args, N=10, n=300, m=50, seed=1,
                 mutation=0.4, adjacency_matrix=None):
        self.n = n
        self.m = m
        self.r = random.Random()
        self.r.seed(seed)
        self.mutation = mutation
            
        if not adjacency_matrix:
            self.N = N
            self.adjacency_matrix = self._init_adjacency_matrix()

        else:
            self.N = len(adjacency_matrix)
            self.adjacency_matrix = adjacency_matrix
            
        self.cities = [i for i in range(self.N)]
        self.p = self._init_population()

    def _init_adjacency_matrix(self):
        adjacency_matrix = [[None for j in range(self.N)] for i in range(self.N)]
        for i in range(self.N):
            for j in range(i, self.N):
                if i == j:
                    adjacency_matrix[i][j] = 0
                else:
                    adjacency_matrix[i][j] = adjacency_matrix[j][i] \
                                             = self.r.randint(1, 50)
        return adjacency_matrix

    def _init_population(self):
        p = []
        for _ in range(self.n):
            x = self.cities[:]
            random.shuffle(x)
            p.append(x)
        return p

    def _f(self, x):
        f = 0
        for i in range(-1, self.N-1):
            f += self.adjacency_matrix[x[i]][x[i+1]]
        return f

    def _selection(self):
        new_p = sorted(self.p, key=lambda x: self._f(x))
        return new_p[:int(self.n * 0.5)]

    def _recombination(self):
        new_p = []
        new_p.extend(self.p)
        while len(new_p) < self.n:
            x = self.p[random.randint(0, len(self.p) - 1)]
            y = self.p[random.randint(0, len(self.p) - 1)]
            new_p.append(self._crossover(x, y))
        return new_p

    def _crossover(self, x, y):
        d = random.randint(1, self.N - 1)
        new_sequence = x[:d]
        for i in range(self.N):
            if y[i] not in new_sequence:
                new_sequence.append(y[i])
        assert len(new_sequence) == self.N
        return new_sequence

    def _mutation(self):
        n = random.randint(1, 1 if self.N//10 < 1 else self.N//10)
        for _ in range(int(self.n * self.mutation)):
            i = random.randint(1, self.n - 1)
            self.p[i] = self._mutate(self.p[i])

    def _mutate(self, sequence):
        n = random.randint(1, 1 if len(sequence)//10 < 1 \
                           else len(sequence)//10)
        new_sequence = sequence[:]
        for _ in range(n):
            a = random.randint(0, len(sequence) - 1)
            b = random.randint(0, len(sequence) - 1)
            new_sequence[a], new_sequence[b] = new_sequence[b], new_sequence[a]
        return new_sequence

    def run(self):
        self.p = self._selection()
        for i in range(self.m):
            self.p = self._recombination()
            self._mutation()
            self.p = self._selection()
            print('{}: {}'.format(i+1, self._f(self.p[0])))


if __name__ == '__main__':
    ga = TSPGeneticAlgorithm(N=50, n=600, m=200)
    ga.run()
