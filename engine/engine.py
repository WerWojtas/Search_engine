import os
import json
import numpy as np
from scipy.sparse import load_npz
from processing.file_parser import FileParser
from file_creators.bag_creator import BagCreator




class SearchEngine():
    def __init__(self, matrix_path = 'app_data/matrixes', dict_path = 'app_data/dicts'):
        self.matrix = load_npz(f'{matrix_path}/term_by_document.npz')
        self.u_10 = np.load(f'{matrix_path}/u_10.npy')
        self.s_10 = np.load(f'{matrix_path}/s_10.npy')
        self.v_10 = np.load(f'{matrix_path}/v_10.npy')
        self.u_100 = np.load(f'{matrix_path}/u_100.npy')
        self.s_100 = np.load(f'{matrix_path}/s_100.npy')
        self.v_100 = np.load(f'{matrix_path}/v_100.npy')
        self.u_500 = np.load(f'{matrix_path}/u_500.npy')
        self.s_500 = np.load(f'{matrix_path}/s_500.npy')
        self.v_500 = np.load(f'{matrix_path}/v_500.npy')
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
        articles_idx = np.argsort(result)[::-1][:number_of_results]
        percent = [result[idx] for idx in articles_idx]
        results = list(zip(articles_idx,percent))
        max_value = max(percent)
        percent = [(value / max_value) * 100 for value in percent] 
        results = list(zip(articles_idx, percent))
        return self.return_urls(results)

    def solve_SVD(self,query, k, number_of_results=10):
        if k == 10:
            u = self.u_10
            s = self.s_10
            v = self.v_10
        elif k == 100:
            u = self.u_100
            s = self.s_100
            v = self.v_100
        else:
            u = self.u_500
            s = self.s_500
            v = self.v_500
        query_vector = self.process_query(query)
        result = ((query_vector@u)@np.diag(s))@v
        result = sorted(enumerate(result), key=lambda x: x[1], reverse=True)
        max_percent = max([x[1] for x in result])
        result = [(x[0], (x[1]/max_percent)*100) for x in result]
        return self.return_urls(result[:number_of_results])

    def return_urls(self, article_idx):
        results = []
        for idx,percent in article_idx:
            filename = self.file_dict[str(idx)]
            filename = filename[:-5]
            url = 'https://en.wikipedia.org/wiki/' + filename
            results.append((url,percent,filename))
        return results
