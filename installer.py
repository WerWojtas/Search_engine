import json
from processing.web_scrapper import Scrapper
from processing.file_parser import FileParser
from processing.term_finder import TermUnionFinder
from file_creators.matrix_creator import MatrixCreator

class Installer():
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as file:
            self.config = json.load(file)
        self.scrapper = Scrapper(self.config['MAX_PAGES'], self.config['LIST_OF_URLS'])
        self.parser = FileParser()
        self.finder = TermUnionFinder(self.config['BAG_OF_WORDS'])
        self.matrix_creator = MatrixCreator(self.config['BAG_OF_WORDS'])

    def scrap(self):
        self.scrapper.scrap_all()
    
    def parse(self):
        self.parser.parse()

    def find_terms(self):
        self.finder.find_terms()

    def create_matrixes(self):
        self.matrix_creator.create_matrix()
        self.matrix_creator.create_SVD()