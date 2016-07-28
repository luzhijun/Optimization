import numpy as np
import fcts
import copy
import time
import matplotlib.pyplot as plt

class ESIndividual:
    '''
    individual of evolutionary strategy
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
        self.fct=fct

    def generate(self):
        '''
        generate a random chromsome for evolutionary strategy
        '''
        len = self.vardim
        rnd = np.random.random(size=len)
        self.chrom = np.zeros(len)
        for i in range(0, len):
            self.chrom[i] = self.bound[0, i] + \
                (self.bound[1, i] - self.bound[0, i]) * rnd[i]

    def calculateFitness(self):
        '''
        calculate the fitness of the chromsome
        '''
        self.fitness = -self.fct(self.chrom)



class EvolutionaryStrategy:

    '''
    the class for evolutionary strategy
    '''

    def __init__(self, fct,sizepop, vardim, bound, MAXGEN, params):
        '''
        sizepop: population sizepop
        vardim: dimension of variables
        bound: boundaries of variables
        MAXGEN: termination condition
        params: algorithm required parameters, it is a list which is consisting of[delta_max, delta_min]
        '''
        self.sizepop = sizepop
        self.vardim = vardim
        self.bound = bound
        self.MAXGEN = MAXGEN
        self.params = params
        self.population = []
        self.fitness = np.zeros(self.sizepop)
        self.trace = np.zeros((self.MAXGEN, 2))
        self.fct=fct

    def initialize(self):
        '''
        initialize the population of es
        '''
        for i in range(0, self.sizepop):
            ind = ESIndividual(self.fct,self.vardim, self.bound)
            ind.generate()
            self.population.append(ind)

    def evaluation(self):
        '''
        evaluation the fitness of the population
        '''
        for i in range(0, self.sizepop):
            self.population[i].calculateFitness()
            self.fitness[i] = self.population[i].fitness

    def solve(self):
        '''
        the evolution process of the evolutionary strategy
        '''
        #SM=[]
        self.t = 0
        self.initialize()
        self.evaluation()
        bestIndex = np.argmax(self.fitness)
        self.best = copy.deepcopy(self.population[bestIndex])
        while self.t < self.MAXGEN:
            self.t += 1
            tmpPop = self.mutation()
            self.selection(tmpPop)
            best = np.max(self.fitness)
            bestIndex = np.argmax(self.fitness)
            if best > self.best.fitness:
                self.best = copy.deepcopy(self.population[bestIndex])
            print(best)
            #if (self.t-1)%50==0:
            #	SM.append(best)
            #if abs(best)<1e-16:
            #	return best
            #self.avefitness = np.mean(self.fitness)
           # self.trace[self.t - 1, 0] = \
            #    (1 - self.best.fitness) / self.best.fitness
           # self.trace[self.t - 1, 1] = (1 - self.avefitness) / self.avefitness
            #print("Generation %d: optimal function value is: %f; average function value is %f" % (
             #   self.t, self.trace[self.t - 1, 0], self.trace[self.t - 1, 1]))
        print("Optimal function value is: %f; " % self.best.fitness)
        print ("Optimal solution is:")
        print (self.best.chrom)
        #self.printResult()
        return -self.best.fitness
        name = input("Please input your name:\n")
        print(name)

    def mutation(self):
        '''
        mutate the population by a random normal distribution
        '''
        tmpPop = []
        for i in range(0, self.sizepop):
            ind = copy.deepcopy(self.population[i])
            delta = self.params[0] + self.t * \
                (self.params[1] - self.params[0]) / (self.MAXGEN)
            #ind.chrom += np.random.normal(0.0, delta, self.vardim)
            ind.chrom += np.random.standard_cauchy(self.vardim)*delta**2
            for k in range(0, self.vardim):
                if ind.chrom[k] < self.bound[0, k]:
                    ind.chrom[k] = self.bound[0, k]
                if ind.chrom[k] > self.bound[1, k]:
                    ind.chrom[k] = self.bound[1, k]
            ind.calculateFitness()
            tmpPop.append(ind)
        return tmpPop

    def selection(self, tmpPop):
        '''
        update the population
        '''
        for i in range(0, self.sizepop):
            if self.fitness[i] < tmpPop[i].fitness:
                self.population[i] = tmpPop[i]
                self.fitness[i] = tmpPop[i].fitness

    def printResult(self):
        '''
        plot the result of evolutionary strategy
        '''
        x = np.arange(0, self.MAXGEN)
        y1 = self.trace[:, 0]
        y2 = self.trace[:, 1]
        plt.plot(x, y1, 'r', label='optimal value')
        plt.plot(x, y2, 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("Evolutionary strategy for function optimization")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    s=time.clock()
    down=-10
    up=-down
    bound = np.tile([[down], [up]], 30)
    fa = EvolutionaryStrategy(fcts.levy,100, 30, bound, 1000, [0.8,0])
    print(fa.solve())
    print(time.clock()-s)