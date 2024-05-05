import os
import json
from itertools import islice

# Finds all terms in the files in the given directory and saves them in json format in search_files folder

class TermUnionFinder(): 
    def __init__(self, bag_number, dir_path='app_data/documents', dict_path = 'app_data/dicts'):
        self.dir_path = dir_path
        self.dict_path = dict_path
        self.bag_number = bag_number

    def find_terms(self):
        term_to_files = dict()
        files = os.listdir(self.dir_path)
        for file in files:
            for line in open(f'{self.dir_path}/{file}', 'r', encoding='utf-8'):
                for term in line.split():
                    if term not in term_to_files:
                        term_to_files[term] = 1
                    else:
                        term_to_files[term] += 1
        term_to_files = dict(sorted(term_to_files.items(), key=lambda item: item[1], reverse=True))
        first_words = dict(islice(term_to_files.items(), self.bag_number))
        indexes = dict()
        reversed_indexes = dict()
        for idx, key in enumerate(first_words.keys()):
            indexes[idx] = key
            reversed_indexes[key] = idx
        with open(f'{self.dict_path}/terms.json', 'w') as file:
            json.dump(first_words, file)
        with open(f'{self.dict_path}/indexes.json', 'w') as file:
            json.dump(indexes, file)
        with open(f'{self.dict_path}/reversed_indexes.json', 'w') as file:
            json.dump(reversed_indexes, file)



                   