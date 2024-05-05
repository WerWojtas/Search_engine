import os
import json
import numpy as np
from scipy.sparse import load_npz
from processing.file_parser import FileParser
from file_creators.bag_creator import BagCreator



class SearchEngine():
    def __init__(self, matrix_path = 'app_data/matrixes', dict_path = 'app_data/dicts'):
        self.matrix = load_npz(f'{matrix_path}/term_by_document.npz')
        self.u = np.load(f'{matrix_path}/u.npy')
        self.s = np.load(f'{matrix_path}/s.npy')
        self.v = np.load(f'{matrix_path}/v.npy')
        self.files = sorted(os.listdir('app_data/documents'))
        self.file_parser = FileParser()
        self.bag_creator = BagCreator()
        with open(f'{dict_path}/files.json', 'r') as file:
            self.file_dict = json.load(file)


    def process_query(self, query):
        query = self.file_parser.parse_file(query)
        q = self.bag_creator.create_bag(query)
        q = np.array(q)
        q = q / np.linalg.norm(q)
        return q

    def solve(self,query, number_of_results=10):
        query_vector = self.process_query(query)
        result = query_vector @ self.matrix
        articles_idx = np.argpartition(result, result.size - number_of_results)[-number_of_results:]
        return self.return_urls(articles_idx)

    def solve_SVD(self,query, number_of_results=10):
        query_vector = self.process_query(query)
        result = ((query_vector @ self.u) @ np.diag(self.s)) @ self.v
        articles_idx = np.argpartition(result, result.size - number_of_results)[-number_of_results:]
        return self.return_urls(articles_idx)

    def return_urls(self, article_idx):
        results = []
        for idx in article_idx:
            filename = self.file_dict[str(idx)]
            filename = filename.strip('.html')
            url = 'https://en.wikipedia.org/wiki/' + filename
            results.append(url)
        return results
