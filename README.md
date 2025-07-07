# DOME: QUBO Model for Traffic Optimization Using Quantum Computing

> **Notice**  
> The source code in this repository is proprietary and is provided solely for review purposes.  
> The author does **not grant** copyright or reuse rights to anyone, except under explicitly defined conditions.  
> Please refer to the [LICENSE.md](./LICENSE.md) file for detailed terms and restrictions.

---

## Overview

**DOME** is a Quantum Computing Solution that uses QUBO modeling and the Quantum Approximate Optimization Algorithm (QAOA) to optimize mordern traffic systems. The goals of this project are:

- Reduce traffic congestion  
- Minimize delays  
- Prioritize emergency vehicles  
- Optimize traffic light timing

For sample data testing, see `city-network.ipynb`. To run with your own data, follow the installation instructions below to set up the `traffic-app`.

---

## Index

1. [Setting up the Project](#setting-up-the-project)  
2. [Features](#features)  
3. [Preview](#preview)  
4. [DOME Implementation](#dome-implementation)

---

## Setting up the Project

### Required Technologies

| Library           | Version |
|------------------|---------|
| Python           | 3.8     |
| Jupyter Notebook | 6.5.4   |

### Local Installation

Run the following commands inside the Anaconda Prompt:

```bash
# 1. Clone the repository
git clone https://github.com/Aksgo/City-traffic-optimization.git

# 2. Navigate to the traffic-app directory
cd ./traffic-app

# 3. Create a virtual environment
conda create --name traffic-app-env python=3.8

# 4. Activate the virtual environment
conda activate traffic-app-env

# 5. Install dependencies
pip install -r requirements.txt

# 6. Start the application server
python app.py
```

## Features

<ul>
    <li>Interface to input the city network (may seem a little robust :) but improving)</li>
    <li>Give priority to emergency vehicles</li>
    <li>Finds three best routes using k_simple_path algorithm</li>
    <li>Utilize congestion parameter to optimize the green the green light timing (aims to increase the time at most congested places)</li>
    <li>Runs Optimization using QUBO formation to find the best of three paths for each Vehicle</li>
    <li>Currently, using dimod exactSolver to simulate solving of QUBO on a Quantum Annealer</li>
</ul>

## Preview

<p>Below are some images of application for a sample in city-data.txt</p>
<div><img src="https://github.com/user-attachments/assets/8c3f34c8-75db-4f13-ac14-d9c400b48e23"></div>
<div><img src="https://github.com/user-attachments/assets/0f3e2f17-b3ae-455e-9150-43c71af837ed"></div>
<div><img src="https://github.com/user-attachments/assets/4c98cccc-8cf8-4b58-a8e2-b460fb83aefb"></div>
<div><img src="https://github.com/user-attachments/assets/b54ac62a-bf48-4a76-8319-470717442e3c"></div>


### Copyright © Aksgo, 2025
