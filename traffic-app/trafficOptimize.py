import networkx as gp
import matplotlib.pyplot as plt
import dimod
'''
num_nodes = 6

edges = [
    (0,1,{'congestion':100, 'distance':40}),
    (0,2,{'congestion':10, 'distance':30}),
    (1,3,{'congestion':200, 'distance':260}),
    (1,4,{'congestion':110, 'distance':100}),
    (2,4,{'congestion':10, 'distance':500}),
    (2,5,{'congestion':12, 'distance':300}),
    (3,4,{'congestion':35, 'distance':6000}),
    (4,2,{'congestion':54, 'distance':300}),
    (0,5,{'congestion':200, 'distance':50}),
    (0,3,{'congestion':50, 'distance':3000})
]

no_of_cars = 3
src_dest = [(0,4,0),(0,4,0),(0,3,1)]
'''


### Alternative Routes

def nodeToEdge(node_routes,no_of_car, no_of_route):
    '''the function convert the route in nodes format to edge format (pairwise nodes as shown above)'''
    edge_route = []
    for i in range(no_of_car):
        car_route = []
        for j in range(no_of_route):
                car_route.append(list(gp.utils.pairwise(node_routes[i][j])))
        edge_route.append(car_route)
    return edge_route

def calcJCS(set_a, set_b):
    '''
    the function calculates the jaccard similarity index of two given paths
    '''
    inter = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return inter/union if union !=0 else 0
def jaccardSimilarityIndex(paths):
    '''
    the function returns the three paths which have least Jaccard Similarity index
    '''
    k = len(paths)
    if(k<=3):return paths
    route = [paths]
    route = nodeToEdge(route,1,k)
    route = route[0]
    result = {}
    for i in range(k):
        for j in range(i+1,k):
            set_a = set(route[i])
            set_b = set(route[j])
            similarity = calcJCS(set_a, set_b)
            result.update({(i,j):similarity})
    srf = sorted(result.items(), key=lambda x: x[1])
    sr=srf[0][0]
    sr2 = srf[1][0]
    final_paths = [paths[sr[0]],paths[sr[1]]]
    if sr2[0] not in sr:
        final_paths.append(paths[sr2[0]])
    else:
        final_paths.append(paths[sr2[1]])
    return final_paths

def edgeWeight(u,v,d):
    return d.get('congestion')/d.get('distance')

def alternativeRoutes(net, no_of_cars, sd):
    '''finds all the simple paths from source to destination for each car'''
    routes = []
    for i in range(no_of_cars):
        k_paths = list(gp.shortest_simple_paths(net, source = sd[i][0], target=sd[i][1], weight = edgeWeight))
        k_paths = jaccardSimilarityIndex(k_paths)
        routes.append(k_paths)
    return routes
    #return [[[0,1,4],[0,1,3,4],[0,2,4]],[[0,2,5],[0,1,3,4,5],[0,1,4,5]]]

#routes  = alternativeRoutes(no_of_cars,src_dest)

def printRoutes(routes,no_of_cars, src_dest):
    print("Source-Destination Pairs for Rerouting:")
    ind = 1
    for src, dest,emergency in src_dest:
        print(f"Car {ind} from {src} to {dest} : emergency {emergency}")
        ind+=1
    print(routes)
    print('\nAlternative Routes :\n')
    index = 0
    for i in range(1,no_of_cars+1):
        print(f'Possible Routes for Car {i}')
        if(len(routes[i-1])<3):
            print("Please give nodes with at least three paths")
            break
        for ch in range(0,len(routes[i-1])):
            l=[]
            for path in routes[i-1][ch]:
                l.append(str(path))
            c="->"
            print(index,":",c.join(l))
            index+=1
            print()

### Helping Functions

def getOverlappingEdges(route1, route2):
    '''the function returns a list of overlapping edges (pairwise-nodes)'''
    overlaps =[]
    for r1 in route1:
        if r1 in route2:
            overlaps.append(r1)
    return overlaps

def getNonOverlappingEdges(route):
    '''
    returns the unique elements in an array
    '''
    uni = []
    for edge in route:
        if edge not in uni:
            uni.append(edge)
    return uni

def matrixWeight(net, route_edge, no_of_cars, no_of_routes, src_dest):
    '''
        Forms the weight matrix (W(ij)) for each binary variable.
        We multiply the weights for the least, second, and best routes by 2, 4, and 8 respectively.
        For emergency vehicles, the weight is doubled overall.
    '''
    Q_weight = {}
    for i in range(no_of_cars):
        emergency = src_dest[i][2]
        path_multipliers = [1.5,2,3]
        l=[]
        for j in range(no_of_routes):
            path = route_edge[i][j]
            path_weight = 0
            total_congestion = 0
            total_distance = 0
            for x, y in path:
                congestion = net[x][y]['congestion']
                distance = net[x][y]['distance']
                total_congestion += congestion
                total_distance += distance
            path_weight = (1.5 * total_congestion) + (1*total_distance)
            l.append((path_weight,j))
        sorted(l)
        ind = 0
        for w,index in l:
            ele=1
            ele*=path_multipliers[ind]
            if emergency == 0:
                ele*=2
            ind+=1
            Q_weight.update({(i, index): ele})
    return Q_weight
    
def displayMatrix(Q, no_of_cars, no_of_routes):
    print("-"*100)
    for i in range(0,no_of_cars*no_of_routes):
        for j in range(0,no_of_cars*no_of_routes):
            print(round(Q.get((i,j)),3),"\t|", end="\t")
        print()
        print("-"*100)
    print()

def formQuboMatrix(net, routes, no_of_car, no_of_routes, src_dest):
    '''
    forms the QUBO matrix in the form of dictionary
    '''
    #dictionary Q will store the qubo matrix
    Q = {}
    K = 0 # initializing penalty factor
    W = matrixWeight(net, routes, no_of_car, no_of_routes, src_dest)
    tot_var = no_of_car*no_of_routes
    #initializing the matrix values to 0
    for i in range(tot_var):
        for j in range(tot_var):
            Q.update({(i,j):0})
    #adding cost function terms
    K = 0
    for i in range(no_of_car):
        car_i_overlap = 0
        for j in range(no_of_routes):
            tot_overlap = []
            for k in range(i+1, no_of_car):
                for m in range(no_of_routes):
                    list_of_overlap = getOverlappingEdges(routes[i][j], routes[k][m])
                    #print(list_of_overlap)
                    Q.update({(i*no_of_routes + j, k*no_of_routes + m):2*len(list_of_overlap)*W[(i,j)]*W[(k,m)]})
                    tot_overlap.extend(list_of_overlap)
            uni_overlap = getNonOverlappingEdges(tot_overlap)
            Q.update({(i*no_of_routes + j, i*no_of_routes + j):len(uni_overlap)*W[(i,j)]*W[(i,j)]})
            car_i_overlap+=len(uni_overlap)
        K = max(K, car_i_overlap)
    #adding penalty terms
    K=K*1000
    for i in range(no_of_car):
        for j in range(no_of_routes):
            for m in range(j+1, no_of_routes):
                Q.update({(i*no_of_routes + j, i*no_of_routes + m):K*2})
            Q[(i*no_of_routes + j, i*no_of_routes + j)] -= K;
    return Q 

#displayMatrix(Q, no_of_cars, no_of_routes)
def solver(net,no_of_cars,src_dest):

    ## Graph formation using NetworkX
    '''plt.figure(figsize=(9,9))
    pos = gp.planar_layout(net)
    gp.draw_networkx_nodes(net, pos, node_color='green', node_size=400)
    gp.draw_networkx_edges(net, pos, arrowstyle='-|>', arrowsize=10)
    edge_labels = {(u, v): f'c: {d["congestion"]}, d: {d["distance"]}' for u, v, d in net.edges(data=True)}
    gp.draw_networkx_edge_labels(net, pos, edge_labels=edge_labels)
    gp.draw_networkx_labels(net, pos, font_size=10, font_color='white')
    plt.title("Directed Graph with Congestion Levels")
    plt.show()'''

    #forming QUBO matrix

    routes  = alternativeRoutes(net, no_of_cars,src_dest)
    no_of_routes = len(routes[0])
    routes_edge = nodeToEdge(routes,no_of_cars,no_of_routes)
    Q = formQuboMatrix(net, routes_edge, no_of_cars, no_of_routes, src_dest)
    
    #running the classical solver 

    bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
    exact_solver  = dimod.ExactSolver()
    response = exact_solver.sample(bqm)
    result = list(response.samples())
    #print(response)
    resulting_energy = list(response.data_vectors['energy'])
    min_energy = min(resulting_energy)
    ct = resulting_energy.count(min_energy)
    best_result = []
    for i in range(ct):
        best_result.append(list(dict.values(dict(result[i]))))

     #returning the final result   
    return min_energy, best_result

    '''print("minimum energy :",min_energy)
    car1_nodes = []
    car2_nodes = []
    for sol in best_result:
        print("Possible Solution :", sol)
        ind = 0
        for i in range(no_of_cars):
            for j in range(no_of_routes):
                if(sol[ind]==1):
                        print(f'best route for car {i+1}: {routes[i][j]}')
                        if(i==0):car1_nodes = routes[i][j]
                        if(i==2):car2_nodes = routes[i][j]
                ind+=1
        '''
    

'''
print("Best Solution")
print("Blue represent Car 1 , Green represents Car 2")
car1_edges = list(gp.utils.pairwise(car1_nodes))
car2_edges = list(gp.utils.pairwise(car2_nodes))
edge_labels = {(u, v): f'c: {d["congestion"]}, d: {d["distance"]}' for u, v, d in net.edges(data=True)}
fig, axes = plt.subplots(1, 2, figsize=(15, 7)) 
pos = gp.planar_layout(net)
#car1
node_colors = ['blue' if node in car1_nodes else 'black' for node in net.nodes()]
edge_colors = ['blue' if (u, v) in car1_edges else 'black' for u, v in net.edges()]
gp.draw_networkx_nodes(net, pos, node_color=node_colors, node_size=400,ax=axes[0])
gp.draw_networkx_edges(net, pos, edge_color = edge_colors, arrowstyle='-|>', arrowsize=15,ax=axes[0])
gp.draw_networkx_edge_labels(net, pos, edge_labels=edge_labels,ax=axes[0])
gp.draw_networkx_labels(net, pos, font_size=10, font_color='white',ax=axes[0])
axes[0].set_title("Optimized Route for Car 1 in the Network")

#car2
node_colors_car2 = ['green' if node in car2_nodes else 'black' for node in net.nodes()]
edge_colors_car2 = ['green' if (u, v) in car2_edges else 'black' for u, v in net.edges()]

gp.draw_networkx_nodes(net, pos, node_color=node_colors_car2, node_size=400, ax=axes[1])
gp.draw_networkx_edges(net, pos, edge_color=edge_colors_car2, arrowstyle='-|>', arrowsize=15, ax=axes[1])
gp.draw_networkx_edge_labels(net, pos, edge_labels=edge_labels,ax=axes[1])
gp.draw_networkx_labels(net, pos, font_size=10, font_color='white',ax=axes[1])
axes[1].set_title("Optimized Route for Car 2 in the Network")

plt.tight_layout()
plt.show()
'''




