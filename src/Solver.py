from . import Grafo
from . import Logico
from . import Criando

def tratamento_schedules(S):
    new_S = ''
    S     = S.replace(')',') ').split(' ')
    
    for operacao in S:
        if 'c' in operacao: new_S += operacao[:2]+' '+operacao[2:]+' '
        else:               new_S +=operacao+' '
        
    return new_S.lower()[:len(new_S)-2]


def solver(S):
    S = tratamento_schedules(S)
    
    criando = Criando.Criando(S)
    criando.Criando_transacao()
    
    grafo   = Grafo.Grafo(criando.ordem_schedules,criando.transacoes)
    grafo.Plotar_grafo()
    

        
