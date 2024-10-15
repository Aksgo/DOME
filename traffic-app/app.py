from flask import Flask, render_template, request, jsonify
import os
import networkx
from trafficOptimize import solver, alternativeRoutes
app = Flask(__name__, template_folder="templates", static_folder='static', static_url_path='/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run')
def run():
    num_nodes = 6
    edges = [
    (0, 1, {'congestion': 2, 'distance': 2}),
    (1, 2, {'congestion': 10, 'distance': 2}),
    (2, 3, {'congestion': 1, 'distance': 2}),
    (3, 4, {'congestion': 4, 'distance': 10}),
    (0, 5, {'congestion': 1, 'distance': 3}),
    (5, 6, {'congestion': 5, 'distance': 3}),
    (6, 4, {'congestion': 1, 'distance': 2}),
    (1, 3, {'congestion': 15, 'distance': 2}),
    (0, 3, {'congestion': 5, 'distance': 3})
    ]
    no_of_cars = 2
    src_dest = [(0,4,0),(0,4,0)]
    net = networkx.DiGraph()
    net.add_edges_from(edges)
    routes = alternativeRoutes(net, no_of_cars, src_dest)
    min_energy,result = solver(net, no_of_cars, src_dest)
    return render_template('result.html', result = routes, min_energy = min_energy)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)