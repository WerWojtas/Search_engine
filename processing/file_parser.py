import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import re

# Parses files in the wiki_data folder to make them ready for the bag of words model
class FileParser():
    def __init__(self, dir_path='app_data/documents', parse_path='app_data/documents'):
        self.dir_path = dir_path
        self.parse_path = parse_path

    def parse(self):
        files = os.listdir(self.dir_path)
        for file in files:
            filepath = f'{self.dir_path}/{file}'
            new_filepath = f'{self.parse_path}/{file}'
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = self.parse_file(f.read())
                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(text)
            except UnicodeDecodeError:
                os.remove(filepath)
                

    def parse_file(self,text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^a-z]', '*', text)
        words = word_tokenize(text)
        words = [word for word in words if not '*' in word and word != "edit"]
        words = [word for word in words if word not in stopwords.words('english')]
        stemmer = SnowballStemmer('english')
        words = [stemmer.stem(word) for word in words]
        words = [word for word in words if len(word) >= 3]
        text = ' '.join(words)
        return text
