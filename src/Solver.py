from .Grafos       import Grafo
from .Tratamento   import TratamentoString
from .Protocol     import CriandoObjeto


def solver(S):

    objetos = CriandoObjeto.CriandoObjeto()
    criando = TratamentoString.Criando(S)
    criando.Criando_transacao()
    
    grafo   = Grafo.Grafo(criando.ordem_schedules,criando.transacoes)
    grafo.Plotar_grafo()
    

        
