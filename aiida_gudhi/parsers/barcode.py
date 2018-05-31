# -*- coding: utf-8 -*-
import numpy as np


class BarcodeParser(object):
    def __init__(self, filename=None, max_life=None):
        self.filename = filename
        self.max_life = max_life

        if filename is None:
            self.data = None
        else:
            self.data = self.parse(filename, max_life)

    @classmethod
    def parse(cls, filename, max_life=None):
        """ Parse barcode from gudhi output. """
        data = np.genfromtxt(filename)
        #data = np.genfromtxt(filename, dtype= (int, int, float, float))

        if max_life is not None:
            data[np.isinf(data)] = max_life

        return data

    def dimensions(self):
        return np.unique(self.data[:, 1])

    def get_life_lines(self, dimension):
        indices = np.where(self.data[:, 1] == dimension)[0]
        return self.data[indices, 2:4]

    def plot(self, dimension):
        """ Plot barcode using matplotlib. """
        import matplotlib.pyplot as plt
        life_lines = self.get_life_lines(dimension)
        x, y = zip(*life_lines)
        plt.scatter(x, y)

        plt.xlabel("Birth")
        plt.ylabel("Death")

        if self.max_life is not None:
            plt.xlim([0, self.max_life])

        plt.title("Persistence Homology Dimension {}".format(dimension))

        #TODO: remove this
        plt.show()
