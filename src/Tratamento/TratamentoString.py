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


class Tratamento:
    def __init__(self,S): 
        
        self.schedules       = self.tratamento_schedules(S.replace(')',') '))
    
        self.ordem_schedules = []
        self.transacoes      = []


    def Criando_transacao(self):
        index = 0
        for operacao in self.schedules.split(' '):
            
            if (operacao != ''):
                NumeroDaTransacao = extrair_numeros_regex(operacao)[0]
            
                if 'C' in operacao:  tipoObjeto = None
                else:                tipoObjeto = extrair_valor_entre_parenteses(operacao)[0]
    
                if NumeroDaTransacao not in self.transacoes:
                    self.transacoes.append(NumeroDaTransacao)

                self.ordem_schedules.append(
                    ( NumeroDaTransacao , operacao[0] , tipoObjeto )
                )            
                index+=1
            
    def tratamento_schedules(self,S):
        new_S = ''
        S     = S.split(' ')

        for operacao in S:            
            if operacao.count('c')>=1 and operacao.count('c') <= 2: 
                new_S += operacao[:2]+' '+operacao[2:] + ' '

            elif operacao.count('c') > 2:
                new_S += ' '.join(re.findall(r'c\d', operacao))

            else:        
                new_S +=operacao+' '
        
        for operacao in new_S.split(' '):
            if ('c' in operacao and len(operacao)>2):
                return self.tratamento_schedules(new_S)
        
        return new_S.upper()

            
        
