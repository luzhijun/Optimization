import numpy as np
import fcts
import random
import copy
import time
import matplotlib.pyplot as plt


class ABSIndividual:

    '''
    individual of artificial bee swarm algorithm
    '''

    def __init__(self, fct, vardim, bound):
        '''
        vardim: dimension of variables
        bound: boundaries of variables
        '''
        self.vardim = vardim
        self.bound = bound
        self.fitness = 0.
        self.trials = 0
        self.fct = fct

    def generate(self):
        '''
        generate a random chromsome for artificial bee swarm algorithm
        '''
        len = self.vardim
        rnd = np.random.random(size=len)
        self.chrom = np.zeros(len)
        for i in range(0, len):
            self.chrom[i] = self.bound[0, i] +  \
                (self.bound[1, i] - self.bound[0, i]) * rnd[i]

    def calculateFitness(self):
        '''
        calculate the fitness of the chromsome
        '''
        self.fitness = -self.fct(self.chrom)


class ArtificialBeeSwarm:

    '''
    the class for artificial bee swarm algorithm
    '''

    def __init__(self, fct, sizepop, vardim, bound, MAXGEN):
        '''
        sizepop: population sizepop
        vardim: dimension of variables
        bound: boundaries of variables
        MAXGEN: termination condition
        params: algorithm required parameters, it is a list which is consisting of[trailLimit, C]
        '''
        self.sizepop = sizepop
        self.vardim = vardim
        self.bound = bound
        self.foodSource = 100
        self.MAXGEN = MAXGEN
        self.params = [vardim * self.foodSource, 1]
        self.population = []
        self.fitness = np.zeros((self.sizepop, 1))
        self.trace = np.zeros((self.MAXGEN, 2))
        self.fct = fct

    def initialize(self):
        '''
        initialize the population of abs
        '''
        for i in range(0, self.sizepop):
            ind = ABSIndividual(self.fct, self.vardim, self.bound)
            ind.generate()
            self.population.append(ind)

    def evaluation(self):
        '''
        evaluation the fitness of the population
        '''
        for i in range(0, self.sizepop):
            self.population[i].calculateFitness()
            self.fitness[i] = self.population[i].fitness

    def employedBeePhase(self):
        '''
        employed bee phase
        '''
        for i in range(0, self.foodSource):
            k = np.random.random_integers(0, self.vardim - 1)
            j = np.random.random_integers(0, self.foodSource - 1)
            while j == i:
                j = np.random.random_integers(0, self.foodSource - 1)
            vi = copy.deepcopy(self.population[i])
            vi.chrom = vi.chrom + np.random.uniform(-1, 1, self.vardim) * (
                vi.chrom - self.population[j].chrom) + np.random.uniform(0.0, self.params[1], self.vardim) * (self.best.chrom - vi.chrom)
            for k in range(0, self.vardim):
                if vi.chrom[k] < self.bound[0, k]:
                    vi.chrom[k] = self.bound[0, k]
                if vi.chrom[k] > self.bound[1, k]:
                    vi.chrom[k] = self.bound[1, k]
            vi.calculateFitness()

            if vi.fitness > self.fitness[i]:
                self.population[i] = vi
                self.fitness[i] = vi.fitness
                if vi.fitness > self.best.fitness:
                    self.best = vi
            else:
                self.population[i].trials += 1

    def onlookerBeePhase(self):
        '''
        onlooker bee phase
        '''
        accuFitness = np.zeros((self.foodSource, 1))
        maxFitness = np.max(self.fitness)

        for i in range(0, self.foodSource):
            accuFitness[i] = 0.9 * self.fitness[i] / maxFitness + 0.1

        for i in range(0, self.foodSource):
            for fi in range(0, self.foodSource):
                r = random.random()
                if r < accuFitness[i]:
                    #k = np.random.random_integers(0, self.vardim - 1)
                    j = np.random.random_integers(0, self.foodSource - 1)
                    while j == fi:
                        j = np.random.random_integers(0, self.foodSource - 1)
                    vi = copy.deepcopy(self.population[i])
                    vi.chrom = vi.chrom + np.random.uniform(-1, 1, self.vardim) * (
                        vi.chrom - self.population[j].chrom) + np.random.uniform(0.0, self.params[1], self.vardim) * (self.best.chrom - vi.chrom)
                    for k in range(0, self.vardim):
                        if vi.chrom[k] < self.bound[0, k]:
                            vi.chrom[k] = self.bound[0, k]
                        if vi.chrom[k] > self.bound[1, k]:
                            vi.chrom[k] = self.bound[1, k]

                    vi.calculateFitness()
                    if vi.fitness > self.fitness[fi]:
                        self.population[fi] = vi
                        self.fitness[fi] = vi.fitness
                        if vi.fitness > self.best.fitness:
                            self.best = vi
                    else:
                        self.population[fi].trials += 1
                    break

    def scoutBeePhase(self):
        '''
        scout bee phase
        '''
        for i in range(0, self.foodSource):
            if self.population[i].trials > self.params[0]:
                self.population[i].generate()
                self.population[i].trials = 0
                self.population[i].calculateFitness()
                self.fitness[i] = self.population[i].fitness

    def solve(self):
        '''
        the evolution process of the abs algorithm
        '''
        #SM = []
        self.t = 0
        self.initialize()
        self.evaluation()
        best = np.max(self.fitness)
        bestIndex = np.argmax(self.fitness)
        self.best = copy.deepcopy(self.population[bestIndex - 1])
        self.avefitness = np.mean(self.fitness)
        self.trace[self.t, 0] = (1 - self.best.fitness) / self.best.fitness
        self.trace[self.t, 1] = (1 - self.avefitness) / self.avefitness
        print("Generation %d: optimal function value is: %f; average function value is %f" % (
            self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
        while self.t < self.MAXGEN - 1:
            self.t += 1
            self.employedBeePhase()
            self.onlookerBeePhase()
            self.scoutBeePhase()
            best = np.max(self.fitness)
            bestIndex = np.argmax(self.fitness)
            print(best)
            #if (self.t - 1) % 50 == 0:
            #    SM.append(best)
            '''
            if best > self.best.fitness:
                self.best = copy.deepcopy(self.population[bestIndex])
            self.avefitness = np.mean(self.fitness)
            self.trace[self.t, 0] = (1 - self.best.fitness) / (self.best.fitness+1e-60)
            self.trace[self.t, 1] = (1 - self.avefitness) / self.avefitness
            '''
            # print("Generation %d: optimal function value is: %f; average function value is %f" % (
            #   self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
        print("Optimal function value is: %f; " % self.best.fitness)
        print("Optimal solution is:")
        print(self.best.chrom)
        return -self.best.fitness
        # self.printResult()

    def printResult(self):
        '''
        plot the result of abs algorithm
        '''
        x = np.arange(0, self.MAXGEN)
        y1 = self.trace[:, 0]
        y2 = self.trace[:, 1]
        plt.plot(x, y1, 'r', label='optimal value')
        plt.plot(x, y2, 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("Artificial Bee Swarm algorithm for function optimization")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    s=time.clock()
    bound = np.tile([[-10], [10]], 30)
    abs = ArtificialBeeSwarm(fcts.griewank, 100, 30, bound, 1000)
    abs.solve()
    print(time.clock()-s)
