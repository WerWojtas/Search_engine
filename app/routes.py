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
    if method == 'normal':
        results = engine.solve(query)
    else:
        results = engine.solve_SVD(query)
    return render_template('results.html', results=results)