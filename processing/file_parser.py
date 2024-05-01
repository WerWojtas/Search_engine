import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import re

# Parses files in the wiki_data folder to make them ready for the bag of words model
class FileParser():
    def __init__(self, dir_path='wiki_data'):
        self.dir_path = dir_path

    def parse(self):
        files = os.listdir(self.dir_path)
        for file in files:
            filepath = f'{self.dir_path}/{file}'
            with open(filepath, 'r', encoding='utf-8') as f:
                text = self.parse_file(f)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)

    def parse_file(self,file):
        text = file.lower()
        text = re.sub(r'[^a-z]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = ''.join([c for c in text if c.isalpha() or c.isspace()])
        words = word_tokenize(text)
        words = [word for word in words if word not in stopwords.words('english')]
        stemmer = SnowballStemmer('english')
        words = [stemmer.stem(word) for word in words]
        words = [word for word in words if len(word) >= 3]
        text = ' '.join(words)
        return text
