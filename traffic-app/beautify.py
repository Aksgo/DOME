import networkx as gp
def processEdges(edges_raw):
    edges=[]
    for d in edges_raw:
        ele = []
        ele.append(d['u'])
        ele.append(d['v'])
        d = {'congestion' : d['congestion'], 'distance': d['distance']}
        ele.append(d)
        ele = tuple(ele)
        edges.append(ele)
    return edges

def processCarData(sd_raw):
    src_dest = []
    for d in sd_raw:
         ele=[]
         ele.append(d['src'])
         ele.append(d['dest'])
         ele.append(d['type'])
         ele = tuple(ele)
         src_dest.append(ele)
    return src_dest