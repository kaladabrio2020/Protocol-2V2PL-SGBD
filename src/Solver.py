from .Grafos       import Grafo
from .Tratamento   import TratamentoString
from .Protocol     import CriandoLogico
from .Protocol     import Protocolo2v2pl


import networkx as nx
import matplotlib.pyplot as plt



def grafoEspera(Espera,transacoes):
        A = Espera
        G   = nx.DiGraph()
        G.add_nodes_from(transacoes)

        G.add_edges_from(A)
        pos = nx.circular_layout(G) 
        nx.draw(G, pos,  with_labels = True, arrows = True, connectionstyle='arc3, rad = 0.1')
        plt.savefig('grafoEspera.png')

        if len(list(nx.simple_cycles(G))) != 0 :  
            return 'Dead lock'
        else:                                     
            return' Tem ciclo'
        
def solver(S):
    print('Escalonador :' ,S)
    criando  = TratamentoString.Tratamento(S)
    
    criando.Criando_transacao()


    protocol = Protocolo2v2pl.Protocolo2v2pl(
        CriandoLogico.CriandoLogico(),
        len(criando.transacoes),
        criando.ordem_schedules
        )
    protocol.SetSysLockInfo()

    grafoEspera(protocol.GetEspera(),criando.transacoes)
    if ( 'DEAD LOCK' in protocol.GetString()):
        return protocol.GetString()
    else:
        return 'New Escalonador :'+protocol.GetString()+str(protocol.GetNewSchedule())

    
    


    
    

    

        
