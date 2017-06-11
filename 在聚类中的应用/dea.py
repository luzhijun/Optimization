# encoding: utf-8

import numpy as np
import fcts
import random
import copy
import matplotlib.pyplot as plt
import time


def f1(b):
    p = np.array(b) / 100000
    s = b[0] * p[0]
    for x in [1, 2, 3, 4]:
        s += np.sum(b[:(x + 1)]) * (1 - np.sum(p[:x])) * p[x]
    s += (np.sum(b[:5]) + 100000) * (1 - np.sum(p[:5]))
    return s


class DEIndividual:

    '''
    individual of differential evolution algorithm
    '''

    def __init__(self, fct, vardim, bound):
        '''
        vardim: dimension of variables
        bound: boundaries of variables
        '''
        self.vardim = vardim
        self.bound = bound
        self.fitness = 0.
        self.fct = fct

    def generate(self):
        '''
        generate a random chromsome for differential evolution algorithm
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


class DifferentialEvolutionAlgorithm:

    '''
    The class for differential evolution algorithm
    '''

    def __init__(self, fct, sizepop, vardim, bound, MAXGEN, params):
        '''
        sizepop: population sizepop
        vardim: dimension of variables
        bound: boundaries of variables
        MAXGEN: termination condition
        param: algorithm required parameters, it is a list which is consisting of [crossover rate CR, scaling factor F]
        '''
        self.sizepop = sizepop
        self.MAXGEN = MAXGEN
        self.vardim = vardim
        self.bound = bound
        self.population = []
        self.fitness = np.zeros((self.sizepop, 1))
        self.trace = np.zeros((self.MAXGEN, 2))
        self.params = params
        self.fct = fct

    def initialize(self):
        '''
        initialize the population
        '''
        for i in range(0, self.sizepop):
            ind = DEIndividual(self.fct, self.vardim, self.bound)
            ind.generate()
            self.population.append(ind)

    def evaluate(self, x):
        '''
        evaluation of the population fitnesses
        '''
        x.calculateFitness()

    def solve(self):
        '''
        evolution process of differential evolution algorithm
        '''
        SM = []
        self.t = 0
        self.initialize()
        for i in range(0, self.sizepop):
            self.evaluate(self.population[i])
            self.fitness[i] = self.population[i].fitness
        best = np.max(self.fitness)
        bestIndex = np.argmax(self.fitness)
        self.best = copy.deepcopy(self.population[bestIndex])
        self.avefitness = np.mean(self.fitness)
        self.trace[self.t, 0] = (1 - self.best.fitness) / self.best.fitness
        self.trace[self.t, 1] = (1 - self.avefitness) / self.avefitness
        # print("Generation %d: optimal function value is: %f; average function value is %f" % (
        #   self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
        while (self.t <= self.MAXGEN):
            for i in range(0, self.sizepop):
                vi = self.mutationOperation(i)
                ui = self.crossoverOperation(i, vi)
                xi_next = self.selectionOperation(i, ui)
                self.population[i] = xi_next
            for i in range(0, self.sizepop):
                self.evaluate(self.population[i])
                self.fitness[i] = self.population[i].fitness
            best = np.max(self.fitness)
            bestIndex = np.argmax(self.fitness)
            if best > self.best.fitness:
                self.best = self.population[bestIndex]
            if self.t % 20 == 0:
                print(self.t, ':', -best)
                SM.append(-best)
            self.t += 1
            '''
            # if abs(best)<1e-15:
            #    break
            self.avefitness = np.mean(self.fitness)
            self.trace[self.t, 0] = (1 - self.best.fitness) / self.best.fitness
            self.trace[self.t, 1] = (1 - self.avefitness) / self.avefitness

            #print("Generation %d: optimal function value is: %f; average function value is %f" % (
            #    self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
            '''
        print("Optimal function value is: %f; " %
              self.best.fitness)
        print("Optimal solution is:")
        print(self.best.chrom)
        return SM
        # self.printResult()

    def selectionOperation(self, i, ui):
        '''
        selection operation for differential evolution algorithm
        '''
        xi_next = copy.deepcopy(self.population[i])
        xi_next.chrom = ui
        self.evaluate(xi_next)
        if xi_next.fitness > self.population[i].fitness:
            return xi_next
        else:
            return self.population[i]

    def crossoverOperation(self, i, vi):
        '''
        crossover operation for differential evolution algorithm
        '''
        k = np.random.random_integers(0, self.vardim - 1)
        ui = np.zeros(self.vardim)
        for j in range(0, self.vardim):
            pick = random.random()
            if pick < self.params[0] or j == k:
                ui[j] = vi[j]
            else:
                ui[j] = self.population[i].chrom[j]
        return ui

    def mutationOperation(self, i):
        '''
        mutation operation for differential evolution algorithm
        '''
        a = np.random.random_integers(0, self.sizepop - 1)
        while a == i:
            a = np.random.random_integers(0, self.sizepop - 1)
        b = np.random.random_integers(0, self.sizepop - 1)
        while b == i or b == a:
            b = np.random.random_integers(0, self.sizepop - 1)
        c = np.random.random_integers(0, self.sizepop - 1)
        while c == i or c == b or c == a:
            c = np.random.random_integers(0, self.sizepop - 1)
        vi = self.population[c].chrom + self.params[1] * \
            (self.population[a].chrom - self.population[b].chrom)
        for j in range(0, self.vardim):
            if vi[j] < self.bound[0, j]:
                vi[j] = self.bound[0, j]
            if vi[j] > self.bound[1, j]:
                vi[j] = self.bound[1, j]
        return vi

    def printResult(self):
        '''
        plot the result of the differential evolution algorithm
        '''
        x = np.arange(0, self.MAXGEN)
        y1 = self.trace[:, 0]
        y2 = self.trace[:, 1]
        plt.plot(x, y1, 'r', label='optimal value')
        plt.plot(x, y2, 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("Differential Evolution Algorithm for function optimization")
        plt.legend()
        plt.show()

if __name__ == "__main__":
   # bound = np.tile([[-10], [10]], 30)abs
    s = time.clock()
    bound = np.tile([[-600], [600]], 30)
   # dea = DifferentialEvolutionAlgorithm(
    #    fcts.Rlevy, 120, 30, bound, 1000, [5, 0.6])
    dea = DifferentialEvolutionAlgorithm(
        fcts.sphere, 100, 30, bound, 600, [0.9, 0.6])
    dea.solve()
    print(time.clock() - s)
