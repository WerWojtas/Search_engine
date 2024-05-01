from scipy.sparse import csc_matrix
import numpy as np
import os
from term_finder import TermUnionFinder
from scipy import sparse
import json


class BagCreator():
    def __init__(self,dir_path,terms_path):
        with open(terms_path, 'r') as file:
            self.terms = json.load(file)
        self.dir_path = dir_path

    def create_bag(self, filepath=None, words=None):
        bag = [0] * len(self.terms)
        if words is not None:
            for term in words:
                if term in self.terms:
                    bag[self.terms.get(term)] += 1
            return bag
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                for term in line.split():
                    if term in self.terms:
                        bag[self.terms.get(term)] += 1
        return bag

    def create_matrix(self):
        matrix_elements = []
        files = sorted(os.listdir(self.dir_path))
        number = 0
        for file in files:
            number +=1
            if number > 5000:
                break
            bag = self.create_bag(filepath=f'{self.dir_path}/{file}')
            for i in range(len(bag)):
                if bag[i] > 0:
                    matrix_elements.append([i, files.index(file), bag[i]])
        rows,cols,vals = zip(*matrix_elements)
        matrix = sparse.csc_matrix((vals, (rows, cols)), shape = (len(self.terms), 5000))
        IDF = self.IDF(matrix)
        matrix = matrix.T.dot(sparse.diags(IDF))
        matrix = matrix.T
        return matrix, IDF
    
    def IDF(self,bag_of_words):
        N = bag_of_words.shape[1]
        n_w = np.array((bag_of_words > 0).sum(axis=1)).flatten()
        IDF = np.log(N / (n_w + 1))
        return IDF.flatten()
