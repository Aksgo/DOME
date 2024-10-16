
# DOME Traffic Optimizer
<ul>
<li>The project aims is to provide way to reduce traffic congestion and delays, and prioritize emergency vehicle by rerouting them and optimizing traffic light timings</li>
<li>The tool will provide both a standalone application and a web-based interface to effectively optimize traffic</li>
<li>'DOME' is just some name easy to call =)</li>
<hr>
<b>NOTE :</b> For testing sample data , please check city-network.ipynb and if you want to insert your own network please perform the local installation steps
<hr>

# Index
1. [Requirement and Deployment](#requirement-and-deployment)
2. [Features](#features)
3. [Preview](#preview)
4. [DOME implementation](#dome-implementation)

# Requirement and Deployment
<h3>Required Tech</h3>
<table>
    <thead>
        <tr>
            <th>Library Name</th>
            <th>Version</th>
        </tr>
    </thead>
    <tbody>
      <tr>
        <td>Python</td>
        <td>3.8</td>
      </tr>
      <tr>
        <td>Jupyter Notebook</td>
        <td>6.5.4</td>
      </tr>
    </tbody>
</table>
<h3>Local Installation</h3>

```
Type the commands inside on your anaconda prompt
```

1. In the terminal clone the project.

```
git clone https://github.com/Aksgo/City-traffic-optimization.git
```

2. Navigate to traffic-app folder

```
cd ./traffic-app
```

3. In your anaconda prompt create a virtual environment

```
conda create --name traffic-app-env python=3.8
```

4. Activate the virtual environment
```
conda activate traffic-app-env
```

5. Install the dependencies
```
pip install -r requirements.txt
```

6. Start The server
```
python app.py
```

# Features

<ul>
  <li>Interface to input the city network (may seem a little robust :) but improving)</li>
  <li>Give priority to emrgency vehicles</li>
  <li>Finds three best routes using k_simple_path algorithm</li>
  <li>Runs Optimization using QUBO formation to find the best of three paths for each Vehicle</li>
  <li>Currently, using dimod exactSolver to simulate solving of QUBO on a Quantum Annealer</li>
</ul>

# Preview
<p>Below are some images of application for a sample in city-data.txt</p>
<div><img src="https://github.com/user-attachments/assets/ff7224e4-44d7-4758-8442-3fe12f58cee3"></div>
<div><img src="https://github.com/user-attachments/assets/42666526-1be2-4d93-ab98-3541dd9c7529"></div>
<div><img src="https://github.com/user-attachments/assets/6c9ca9e8-389e-413d-a7cd-a5ffac043226"></div>
<div><img src="https://github.com/user-attachments/assets/792d8115-91fa-4c20-876f-bcf6ce6046e7"></div>

# DOME Implementation
<ul>
  <h3>Below I have explained the working of Model implemented till now</h3>
  <li>Utliized Networkx to form and visualize directed graphs and perform some starter algorithms</li>
  <li>Each road (edge) has two parameters : congestion (no of vehicles) and distance (the length of road)</li>
  <li>Then the model inputs all the the required details of emergency vehicles and normal vehicles (their source and destination)</li>
  <li>Using networkx k_simple_path algorithm (essenstially multiple times dijkstra) we find the all the simple paths (non-cyclic) from source to destination (for each vehicle)</li>
  <li>Used Jaccard Similarity Index to find least overlapping paths</li>
  <li>Formed i*j binary variables where i = number of Cars and j = number of alternative routes</li>
  <li>Implemented weight for each binary variables based on :
    <ul>
      <li>If non emergency car then increase the weight</li>
      <li>For each of the three routes, I prioritized them based on an overall parameter: (1.5*total_congestion + 1*total_distance)</li>
      <li>congestion heavier parameter then distance (more weight)</li>
    </ul>
  </li>
  <li>Finally Formed the QUBO matrix based on the equation</li>
  <li>Solved it (for now) using dimod's eactSolver (classical simulator)</li>
</ul>
