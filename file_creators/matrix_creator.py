import os
import json
import numpy as np
from .bag_creator import BagCreator
from scipy import sparse
from scipy.sparse.linalg import svds


class MatrixCreator():
    def __init__(self, terms_number, dict_path='app_data/dicts', matrix_path = 'app_data/matrixes', document_path='app_data/documents'):
        self.matrix_path = matrix_path
        self.bag_creator = BagCreator()
        self.document_path = document_path
        self.terms_number = terms_number
        self.dict_path = dict_path


    def create_matrix(self):
        matrix_elements = []
        number = 0
        file_dict = dict()
        files = os.listdir(self.document_path)
        for file in files:
            with open(f'{self.document_path}/{file}', 'r', encoding='utf-8') as f:
                bag = self.bag_creator.create_bag(f.read())
            for i in range(len(bag)):
                if bag[i] > 0:
                    matrix_elements.append([i, files.index(file), bag[i]])
            file_dict[number] = file
            number += 1
        rows,cols,vals = zip(*matrix_elements)
        matrix = sparse.csc_matrix((vals, (rows, cols)), shape = (self.terms_number, len(files)))
        sparse.save_npz(f'{self.matrix_path}/term_by_document.npz', matrix)
        with open(f'{self.dict_path}/files.json', 'w') as file:
            json.dump(file_dict, file)
        
    def create_SVD(self, k):
        matrix = sparse.load_npz(f'{self.matrix_path}/term_by_document.npz')
        u, s, v = svds(matrix, k=k)
        np.save(f'{self.matrix_path}/u_{k}.npy', u)
        np.save(f'{self.matrix_path}/s_{k}.npy', s)
        np.save(f'{self.matrix_path}/v_{k}.npy', v)