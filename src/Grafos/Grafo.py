import networkx as nx
import numpy    as np
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self , ordem_schedules,transaction):
        self.digraph = []
        self.ordem_schedules = ordem_schedules
        self.transaction     = transaction
    
    def Grafo_serialização(self):
        index = 1
        for tupla_i in self.ordem_schedules:
            for tupla_j in self.ordem_schedules[index:]:
                if   (tupla_i[0] == tupla_j[0]):                pass
                elif ('C' == tupla_i[1] or  'C' == tupla_j[1]): pass
                elif ('R' == tupla_i[1] and 'R' == tupla_j[1]): pass

                elif   ('W' == tupla_i[1] and 'W' == tupla_j[1]):
                    if (tupla_i[2] == tupla_j[2]): self.digraph.append((tupla_i[0],tupla_j[0]))

                elif   (tupla_i[1] != tupla_j[1]):
                    if (tupla_i[2] == tupla_j[2]): self.digraph.append((tupla_i[0],tupla_j[0]))
            index+=1
    
    def Plotar_grafo(self):
        self.Grafo_serialização()

        G = nx.DiGraph()
        G.add_nodes_from(self.transaction)
        G.add_edges_from(self.digraph)

        pos = nx.circular_layout(G) 
        nx.draw(G, pos,  with_labels = True, arrows = True, connectionstyle='arc3, rad = 0.1')
    
        if len(list(nx.simple_cycles(G))) != 0 :  
            string = 'Não tem ciclo'
        else:                                     
            string = ' Tem ciclo'
        plt.title(string)
        plt.show()
        

        