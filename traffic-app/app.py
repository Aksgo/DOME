from flask import Flask, render_template, request, jsonify, session, send_file
import os
import shutil
from beautify import processEdges, processCarData
import networkx as gp
import random
import matplotlib
matplotlib.use('Agg')  # Use Agg backend
import matplotlib.pyplot as plt
from trafficOptimize import solver, alternativeRoutes
app = Flask(__name__, template_folder="templates", static_folder='static', static_url_path='/static')
app.secret_key = os.urandom(24)
DIR = "static/plots"
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dome', methods=['POST'])
def run_dome():

    #clearing previous data
    if  os.path.exists(DIR):
        shutil.rmtree(DIR)
    os.makedirs(DIR)
    #data
    data = request.json
    no_of_cars = data.get('no_of_cars')
    #to disable
    no_of_cars = 3
    edges_raw = data.get('edges')
    sd_raw = data.get('src_dest')
    edges = processEdges(edges_raw)
    #to disable
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
    src_dest = processCarData(sd_raw)
    #to disable
    src_dest = [(0,4,0),(0,4,0),(0,4,0)]

    #network formation
    net = gp.DiGraph()
    net.add_edges_from(edges)
    routes = alternativeRoutes(net, no_of_cars, src_dest)
    
    #running DOME - utilizing classical simulator
    min_energy,result,bestRoute = solver(net, no_of_cars, src_dest)

    #graph plot
    plt.figure(figsize=(9,9))
    pos = gp.planar_layout(net)
    gp.draw_networkx_nodes(net, pos, node_color='green', node_size=400)
    gp.draw_networkx_edges(net, pos, arrowstyle='-|>', arrowsize=10)
    edge_labels = {(u, v): f'c: {d["congestion"]}, d: {d["distance"]}' for u, v, d in net.edges(data=True)}
    gp.draw_networkx_edge_labels(net, pos, edge_labels=edge_labels)
    gp.draw_networkx_labels(net, pos, font_size=10, font_color='white')
    plt.title("Directed Graph with Congestion Levels")
    plot_path = os.path.join(DIR, 'network.png')
    plt.savefig(plot_path)


    #storing in session storage to retrieve later
    session['min_energy'] = min_energy
    session['routes'] = routes
    session['result'] = result
    session['numCars'] = no_of_cars
    session['bestRoute'] = bestRoute
    return jsonify({'key':'value'})

@app.route('/results')
def show_results():
    min_energy = session.get('min_energy')
    routes = session.get('routes')
    result = session.get('result')
    numCars = session.get('numCars')
    bestRoute = session.get('bestRoute')
    return render_template(
        'result.html', 
        result=result, 
        min_energy=min_energy,
        routes=routes,
        numCars = numCars,
        bestRoute=bestRoute
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)