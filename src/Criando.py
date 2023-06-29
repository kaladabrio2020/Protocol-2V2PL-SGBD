
import re
from . import Logico

def extrair_numeros_regex(operacao):  
    return [int(numero) for numero in re.findall(r'\d+', operacao)]

def extrair_valor_entre_parenteses(operacao):
    correspondencias = re.findall(r'\((.*?)\)', operacao)
    
    if correspondencias: 
        return correspondencias
    else:
        raise ValueError(f'Não existe objeto nessa operacao {operacao}')
    

class Criando:
    ordem_schedules = []
    transacoes      = []

    def __init__(self,S): self.schedules = S

    def Criando_transacao(self):
        index = 0
        for operacao in self.schedules.split(' '):
            
            numero = extrair_numeros_regex(operacao)[0]
            
            if 'c' in operacao:  objeto = True
            else:                objeto = extrair_valor_entre_parenteses(operacao)[0]
  
            if numero not in self.transacoes:
                self.transacoes.append(numero)

            self.ordem_schedules.append((numero,operacao[0],objeto))            
            index+=1
     

   
            
        
