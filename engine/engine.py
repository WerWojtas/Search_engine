from bag_of_words import BagCreator
import numpy as np
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csc_matrix,linalg, save_npz,load_npz
from scipy.sparse.linalg import svds
from file_parser import FileParser
import os



class SearchEngine():
    def __init__(self, dir_path='wiki_data', jsonpath = 'search_files/terms.json'):
        self.json_term = jsonpath
        self.bag = BagCreator(dir_path,jsonpath)
        self.parser = FileParser(dir_path)
        self.files = os.listdir(dir_path)

    def start_engine_bag(self):
        bag_of_words, IDF = self.bag.create_matrix()
        save_npz('resources/bag_of_words.npz',bag_of_words)
        np.save('resources/IDF.npy',IDF)

    def start_engine_lowrank(self):
        bag_of_words = load_npz('resources/bag_of_words.npz')
        A, V = self.lowrank(bag_of_words)
        save_npz('resources/A.npz', A)
        save_npz('resources/V.npz', V)

    def solve(self, query,number):
        bag_of_words = load_npz('resources/bag_of_words.npz')
        IDF = np.load('resources/IDF.npy')
        words = self.parser.parse_file(query)
        q = self.bag.create_bag(words=words.split())
        q = q / np.linalg.norm(q)
        q = csc_matrix(q)
        print(bag_of_words.shape)
        result = q @ bag_of_words
        print(result)
        articles_idx = np.argpartition(result, result.size - number)[-number:]
        return zip(articles_idx[np.argsort(result[articles_idx])][::-1], result[articles_idx[np.argsort(result[articles_idx])][::-1]])

        

    def solve_lowrank(self, query, number):
        A = load_npz('resources/A.npz')
        V = load_npz('resources/V.npz')
        bag_of_words = load_npz('resources/bag_of_words.npz')
        IDF = np.load('resources/IDF.npy')
        words = self.parser.parse_file(query)
        q = self.bag.create_bag(words=words.split())@ IDF
        q = q / np.linalg.norm(q)
        sim = A.dot(V.dot(q.T))
        sorted_indices = np.argsort(sim.data)
        sorted_indices = sorted_indices[::-1]
        top_10_indices = sorted_indices[:10]
        ulr_links = ['https://en.wikipedia.org/wiki/'+ os.path.splitext(self.files[i])[0] for i in top_10_indices]
        return ulr_links
    
    def lowrank(self,A, k=250):
        u, s, v = svds(A, k)
        s = np.diag(s)
        A = csc_matrix(u)
        V = csc_matrix(s.dot(v))
        return A,V