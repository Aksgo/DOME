
# DOME Traffic Optimizer
<ul>
<li>This project is to provide a way to :
    <ul>
        <li>Reduce traffic congestion</li>
        <li>Reduce delays</li>
        <li>Prioritize emergency vehicle</li>
        <li>Optimizing traffic light timing (mathematical construction)</li>
    </ul>
<li>It is a web-based solution to  optimize the traffic effectively</li>
<li>Please view the document 'QUBO-Equation.pdf' to check the equations used</li>
<li>'DOME' is just a name, easy to call =)</li>
<hr>
<b>NOTE :</b> For testing sample data , please check city-network.ipynb and if you want to insert your own network please install the traffic-app following the instructions below
<hr>

# Index
1. [Setting up the Project](#setting-up-the-project)
2. [Features](#features)
3. [Preview](#preview)
4. [DOME implementation](#dome-implementation)

# Setting up the Project
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
<p>Please type the following commands inside Anaconda Prompt</p>

1. Clone the project repo into any desired folder

```
git clone https://github.com/Aksgo/City-traffic-optimization.git
```

2. Navigate to traffic-app folder

```
cd ./traffic-app
```

3. Create a virtual environment

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

6. Start the server
```
python app.py
```

# Features

<ul>
    <li>Interface to input the city network (may seem a little robust :) but improving)</li>
    <li>Give priority to emergency vehicles</li>
    <li>Finds three best routes using k_simple_path algorithm</li>
    <li>Utilize congestion parameter to optimize the green the green light timing (aims to increase the time at most congested places)</li>
    <li>Runs Optimization using QUBO formation to find the best of three paths for each Vehicle</li>
    <li>Currently, using dimod exactSolver to simulate solving of QUBO on a Quantum Annealer</li>
</ul>

# Preview

<p>Below are some images of application for a sample in city-data.txt</p>
<div><img src="https://github.com/user-attachments/assets/8c3f34c8-75db-4f13-ac14-d9c400b48e23"></div>
<div><img src="https://github.com/user-attachments/assets/0f3e2f17-b3ae-455e-9150-43c71af837ed"></div>
<div><img src="https://github.com/user-attachments/assets/4c98cccc-8cf8-4b58-a8e2-b460fb83aefb"></div>
<div><img src="https://github.com/user-attachments/assets/b54ac62a-bf48-4a76-8319-470717442e3c"></div>

# DOME Implementation
<ul>
    <b>NOTE : I have improvised and changed the formulation from those given earlier in write-up</b>
    <hr>
    <h3>Summary of Implementation</h3>
    <li>Utliized networkx library to form and visualize directed graphs</li>
    <li>Each road (edge) has two parameters : congestion (no of vehicles) and distance (the length of road)</li>
    <li>Each vehicle input consist of two parameters : source node, destination node</li>
    <li>First the model routes emergency vehicles and after that normal vehicles</li>
    <li>Using networkx k_simple_path algorithm (essentially multiple times dijkstra) we find all the simple paths (non-cyclic) from source to destination (for each vehicle)</li>
    <li>Used Jaccard Similarity Index to find least overlapping paths</li>
    <li>Formed i*j binary variables where i = number of Cars and j = number of alternative routes</li>
    <li>Implemented weight for each binary variables based on following :
    <ul>
      <li>If non emergency car then increase the weight</li>
      <li>Each of the three routes are prioritized based on an overall parameter : (1.5*total_congestion + 1*total_distance)</li>
      <li>Congestion heavier parameter then distance (more weight)</li>
    </ul>
    </li>
    <li>Finally formed the QUBO matrix based on the equation</li>
    <li>Solved it (for now) using dimod's exactSolver (classical simulator) which aims to minimize the total energy</li>
    <li>For optimizing traffic light timing :
        <ul>
            <li>Asssumed that traffic signal is present at each road ith point if road is going from j to i</li>
            <li>the weight of each signal is determined by the congestion at that road</li>
        </ul>
    </li>
    <li>Due to memory limitations, please look at the QUBO implementations details of traffic Signal (in city-network.ipynb) only</li>
</ul>

### Copyright ©️ Aksgo, 2025
