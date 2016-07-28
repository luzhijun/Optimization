import numpy as np
import fcts
import copy
import random
import matplotlib.pyplot as plt


class BAIndividual:

    '''
    individual of bat algorithm
    '''

    def __init__(self,  vardim, bound):
        '''
        vardim: dimension of variables
        bound: boundaries of variables
        '''
        self.vardim = vardim
        self.bound = bound
        self.fitness = 0.
        self.trials = 0

    def generate(self):
        '''
        generate a random chromsome for bat algorithm
        '''
        len = self.vardim
        rnd = np.random.random(size=len)
        self.chrom = np.zeros(len)
        self.velocity = np.random.random(size=len)
        for i in range(0, len):
            self.chrom[i] = self.bound[0, i] + \
                (self.bound[1, i] - self.bound[0, i]) * rnd[i]

    def calculateFitness(self):
        '''
        calculate the fitness of the chromsome
        '''
        self.fitness = -fcts.griewank(self.chrom)


class BatAlgorithm:

    '''
    the class for bat algorithm
    '''

    def __init__(self, sizepop, vardim, bound, MAXGEN, params):
        '''
        sizepop: population sizepop
        vardim: dimension of variables
        bound: boundaries of variables
        MAXGEN: termination condition
        params: algorithm required parameters, it is a list which is consisting of[fmax, fmin, Amax, Amin, alpha, gamma]
        '''
        self.sizepop = sizepop
        self.vardim = vardim
        self.bound = bound
        self.MAXGEN = MAXGEN
        self.params = params
        self.population = []
        self.fitness = np.zeros(self.sizepop)
        self.freq = np.zeros(self.sizepop)
        self.loudness = np.zeros(self.sizepop)
        self.emissionrate = np.zeros(self.sizepop)
        self.initEmissionrate = np.zeros(self.sizepop)
        self.trace = np.zeros((self.MAXGEN, 2))

    def initialize(self):
        '''
        initialize the population of ba
        '''
        for i in range(0, self.sizepop):
            ind = BAIndividual(self.vardim, self.bound)
            ind.generate()
            self.population.append(ind)
            self.freq[i] = self.params[1] + \
                (self.params[0] - self.params[1]) * np.random.random(1)
            self.loudness[i] = self.params[3] + \
                (self.params[2] - self.params[3]) * np.random.random(1)
            self.initEmissionrate[i] = np.random.random(1)
            self.emissionrate[i] = self.initEmissionrate[i]

    def evaluation(self):
        '''
        evaluation the fitness of the population
        '''
        for i in range(0, self.sizepop):
            self.population[i].calculateFitness()
            self.fitness[i] = self.population[i].fitness

    def solve(self):
        '''
        the evolution process of the bat algorithm
        '''
        SM = []
        self.t = 0
        self.initialize()
        self.evaluation()
        bestIndex = np.argmax(self.fitness)
        self.best = copy.deepcopy(self.population[bestIndex])
        while self.t < self.MAXGEN:
            self.t += 1
            self.update()
            # idx = self.select()
            self.evaluation()
            best = np.max(self.fitness)
            bestIndex = np.argmax(self.fitness)
            if best > self.best.fitness:
                self.best = copy.deepcopy(self.population[bestIndex])
            print(best)
            if self.t % 10 == 0:
                SM.append(best)
            if abs(best)<1e-15:
            	break
            self.avefitness = np.mean(self.fitness)
            self.trace[self.t - 1, 0] = \
                (1 - self.best.fitness) / self.best.fitness
            self.trace[self.t - 1, 1] = (1 - self.avefitness) / self.avefitness
            # print("Generation %d: optimal function value is: %f; average function value is %f" % (
            #   self.t, self.trace[self.t - 1, 0], self.trace[self.t - 1, 1]))
        print("Optimal function value is: %f; " % SM[-1])
        print("Optimal solution is:")
        print(self.best.chrom)
        return SM
        # self.printResult()

    def update(self):
        '''
        update the population
        '''
        for i in range(0, self.sizepop):
            self.freq[i] = self.params[1] + \
                (self.params[0] - self.params[1]) * np.random.random(1)
            self.population[
                i].velocity += (self.best.chrom - self.population[i].chrom) * self.freq[i]

            self.population[i].chrom += self.population[i].velocity
            for k in range(0, self.vardim):
                if self.population[i].chrom[k] < self.bound[0, k]:
                    self.population[i].chrom[k] = self.bound[0, k]
                if self.population[i].chrom[k] > self.bound[1, k]:
                    self.population[i].chrom[k] = self.bound[1, k]
            rnd = np.random.random(1)
            A = np.mean(self.emissionrate)
            tmpInd = copy.deepcopy(self.best)
            if rnd > self.emissionrate[i]:
                tmpInd.chrom += np.random.uniform(low=-1,
                                                  high=1.0, size=self.vardim) * A
                for k in range(0, self.vardim):
                    if tmpInd.chrom[k] < self.bound[0, k]:
                        tmpInd.chrom[k] = self.bound[0, k]
                    if tmpInd.chrom[k] > self.bound[1, k]:
                        tmpInd.chrom[k] = self.bound[1, k]
            tmpInd.calculateFitness()
            if tmpInd.fitness > self.best.fitness and random.random() < self.loudness[i]:
                self.population[i] = tmpInd
                self.loudness[i] *= self.params[4]
                self.emissionrate[i] = self.initEmissionrate[
                    i] * (1 - np.exp(self.params[5] * self.t))
            if tmpInd.fitness > self.best.fitness:
                self.best = copy.deepcopy(tmpInd)

    def selectOne(self):
        '''
        select one individual from the population
        '''
        totalFitness = np.sum(self.fitness)
        accuFitness = np.zeros(self.sizepop)

        sum1 = 0.
        for i in range(0, self.sizepop):
            accuFitness[i] = sum1 + self.fitness[i] / totalFitness
            sum1 = accuFitness[i]

        r = random.random()
        idx = 0
        for j in range(0, self.sizepop - 1):
            if j == 0 and r < accuFitness[j]:
                idx = 0
                break
            elif r >= accuFitness[j] and r < accuFitness[j + 1]:
                idx = j + 1
                break
        return idx

    def printResult(self):
        '''
        plot the result of bat algorithm
        '''
        x = np.arange(0, self.MAXGEN)
        y1 = self.trace[:, 0]
        y2 = self.trace[:, 1]
        plt.plot(x, y1, 'r', label='optimal value')
        plt.plot(x, y2, 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("Bat algorithm for function optimization")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    bound = np.tile([[-600], [600]], 30)
    fa = BatAlgorithm(20, 10, bound, 1000, [2, 0, 4, 0, 0.9, 0.9])
    fa.solve()
