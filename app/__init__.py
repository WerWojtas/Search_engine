import json
from flask import Flask
from scipy import sparse
from engine.engine import SearchEngine


app = Flask(__name__)
with open('config.json', encoding='utf-8') as f:
    config = json.load(f)

app.config.update(config)
app.config['MATRIX'] = sparse.load_npz('./app_data/matrixes/term_by_document.npz')

from app import routes