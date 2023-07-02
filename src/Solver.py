from . import Grafo
from . import TratamentoString
from . import CriandoObjeto


def solver(S):
    objetos = CriandoObjeto.CriandoObjeto()
    criando = TratamentoString.Criando(S)
    criando.Criando_transacao()
    
    grafo   = Grafo.Grafo(criando.ordem_schedules,criando.transacoes)
    grafo.Plotar_grafo()
    

        
