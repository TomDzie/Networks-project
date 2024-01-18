import pyvis as pv
import matplotlib.pyplot as plt
from pyvis.network import Network
import json
import networkx as nx
import numpy as np
import json

file_name = 'gwiazdy_json\\ryan_reynolds.json'
with open(f'{file_name}', 'r') as plik_json:
    dane = json.load(plik_json)
    iterations = 0
    for i in dane:
        name  = i
        family = []
        for j in dane[i]:
            if dane[i][j] != None:
                for k in dane[i][j][0]:
                    family.append(k)
            else: continue
        with open(f'ryan_blake-net.json', 'r') as net:
            stare = json.load(net)

       # Nowe dane do dodania
        nowy_dane = { 
            f"{name}": family
        }
        print(nowy_dane)

        # Dodanie nowych danych do istniejących danych
        stare.update(nowy_dane)

        with open(f'ryan_blake-net.json', 'w') as net:
            json.dump(stare, net, indent=4)



file = 'ryan_blake-net.json'
with open(file, 'r') as f:
    file = f.read()
    file = json.loads(file)

def return_tuples(dict_):
    net_tuple = []
    for i in dict_:
        for j in dict_[i]:
            net_tuple.append((i, j))  
    return net_tuple

def make_net(graph, name):
  net = Network()
  net.from_nx(graph)
  net.toggle_physics(True)
  net.prep_notebook(custom_template=False, custom_template_path=None)
  net.show(f'{name}.html')
  
G = nx.Graph()
G.add_nodes_from(file)
G.add_edges_from(return_tuples(file))

make_net(G, "ryan_blake-net")
