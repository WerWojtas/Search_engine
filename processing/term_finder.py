import os
import json

# Finds all terms in the files in the given directory and saves them in json format in search_files folder

class TermUnionFinder(): 
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.term_to_files = dict()

    def find_terms(self):
        files = os.listdir(self.dir_path)
        num = 0
        for file in files:
            for line in open(f'{self.dir_path}/{file}', 'r', encoding='utf-8'):
                for term in line.split():
                    if term not in self.term_to_files:
                        self.term_to_files[term] = num
                        num+=1
        with open('search_files/terms.json', 'w') as file:
            json.dump(self.term_to_files, file)



                   