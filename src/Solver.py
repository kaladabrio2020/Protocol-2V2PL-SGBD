from .Grafos       import Grafo
from .Tratamento   import TratamentoString
from .Protocol     import CriandoLogico
from .Protocol     import Protocolo2v2pl

def solver(S):
    criando  = TratamentoString.Tratamento(S)
    

    criando.Criando_transacao()
    grafo   = Grafo.Grafo(criando.ordem_schedules,criando.transacoes)
    grafo.Plotar_grafo()

    protocol = Protocolo2v2pl.Protocolo2v2pl(
        CriandoLogico.CriandoLogico(),len(grafo.transacoes)
        )
    protocol.SetSysLockInfo(criando.ordem_schedules)

    grafo.grafoEspera(protocol.GetEspera())
    print(protocol.GetString())
    return protocol.GetString()

    
    


    
    

    

        
