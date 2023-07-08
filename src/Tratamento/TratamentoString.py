import re
from ..Protocol import Logico


def extrair_numeros_regex(operacao): 
    return [int(numero) for numero in re.findall(r'\d+', operacao)]

def extrair_valor_entre_parenteses(operacao):
    correspondencias = re.findall(r'\((.*?)\)', operacao)[0]

    if correspondencias: 
        return correspondencias.split(',')
    else:                
        raise ValueError(f'Não existe objeto nessa operacao {operacao}')


class Criando:
    def __init__(self,S): 
        self.schedules       = self.tratamento_schedules(S)
        self.ordem_schedules = []
        self.transacoes      = []

    def Criando_transacao(self):
        index = 0
        for operacao in self.schedules.split(' '):
            NumeroDaTransacao = extrair_numeros_regex(operacao)[0]
        
            if 'C' in operacao:  
                operacao   = 'C'
            else:                
                tipoObjeto = extrair_valor_entre_parenteses(operacao)[0]
  
            if NumeroDaTransacao not in self.transacoes:
                self.transacoes.append(NumeroDaTransacao)

            self.ordem_schedules.append(
                ( NumeroDaTransacao , operacao[0] , tipoObjeto )
            )            
            index+=1
            
    def tratamento_schedules(self,S):
        new_S = ''
        S     = S.replace(')',') ').split(' ')  
        for operacao in S:
            if 'c' in operacao: new_S += operacao[:2]+' '+operacao[2:]+' '
            else:               new_S +=operacao+' '
            
        return new_S.upper()[:len(new_S)-2]

            
        
