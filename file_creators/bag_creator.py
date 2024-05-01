import os
import json
import numpy as np


class BagCreator():
    def __init__(self,document_path='app_data/documents',terms_path='app_data/dicts/terms.json', index_path='app_data/dicts/indexes.json'):
        with open(terms_path, 'r') as file:
            self.terms = json.load(file)
        with open(index_path, 'r') as file:
            self.indexes = json.load(file)
        self.files_number = len(os.listdir(document_path))
        self.IDF = self.create_IDF()

    def create_bag(self, text):
        bag = [0] * len(self.terms)
        text = text.split(" ")
        for word in text:
            if word in self.terms:
                bag[self.terms[word]] += 1
        return [bag[i]*self.IDF[i] for i in range(len(bag))]

    def create_IDF(self):
        IDF = [0] * len(self.terms)
        for i in range(len(IDF)):
            word = self.indexes[str(i)]
            IDF[i] = np.log(self.files_number/ self.terms[word])
        return IDF

    
