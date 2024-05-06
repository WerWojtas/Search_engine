from app import app
from flask import render_template, request
from engine.engine import SearchEngine


engine = SearchEngine()

# add new app route /
@app.route('/')
def home():
    return render_template('home.html')

# add new app route /solve
@app.route('/solve', methods=['GET'])
def solve():
    query = request.args.get('query')
    method = request.args.get('method')
    if method == 'without':
        results = engine.solve(query)
    elif method == 'svd_10':
        results = engine.solve_SVD(query,10)
    elif method == 'svd_100':
        results = engine.solve_SVD(query,100)
    else:
        results = engine.solve_SVD(query,500)
    return render_template('results.html', results=results)