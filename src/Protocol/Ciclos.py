import networkx as nx
import matplotlib.pyplot as plt
def VerificaGrafoTemCiclo(Espera,tamanho):
    
    try:
        A   = Espera
        G   = nx.DiGraph()
        G.add_nodes_from([i for i in range(1,tamanho+1)])

        G.add_edges_from(A)
        pos = nx.circular_layout(G) 
        plt.savefig('grafoEspera.png')

        if len(list(nx.simple_cycles(G))) != 0 :  
            return True
        else:                                     
            return False
    
    except Exception:
        return False