import pandas   as pd
from ..Protocol import Ciclos as cl
class Protocolo2v2pl:
    def __init__(self,Logico,tamanho): 
        self.tamanho = tamanho
        self.Logico  = Logico
        self.string  = ''
        self.Espera  = []

        self.SysLockInfo = pd.DataFrame({
            'Transacao':[],
            'Objeto'   :[],
            'Operacao' :[],
            'Status'   :[],
            'Predecessores':[]
        })

    def GetString(self): return self.string
    
    def GetEspera(self): return self.Espera
    
    def SetSysLockInfo(self,schedule):
        
        for tupla in schedule:


            if ( tupla[1] == 'C'):
                if (self.Commit(tupla) ):
                    self.string += 'DEAD LOCK'
                    return self.string

                self.string+='Passos \n'+'Espera:'+str(self.Espera)+'\n'+self.SysLockInfo.drop(columns='Predecessores').to_string()+'\n\n'

            else:
                Status,predecessores = self.AdicionarBloqueio(tupla[1],tupla[2])
                
                self.SysLockInfo.loc[
                    len(self.SysLockInfo)
                ] = [tupla[0],
                     tupla[2],
                     tupla[1]+'L',
                     Status,
                     ','.join(predecessores)]
                
                self.string+='Passos \n'+self.SysLockInfo.drop(columns='Predecessores').to_string()+'\n\n'

            if ( cl.VerificaGrafoTemCiclo(self.Espera,self.tamanho)):
                self.string += 'DEAD LOCK'
                return self.string


        if ( cl.VerificaGrafoTemCiclo(self.Espera,self.tamanho)):
            self.string += 'DEAD LOCK'
            return self.string


    def Commit(self,tuplaDoCommit):
        transacao    = tuplaDoCommit[0]
        
        dataCommit   = self.SysLockInfo.loc[self.SysLockInfo['Transacao'] == transacao]
        dataFrame    = self.SysLockInfo[self.SysLockInfo['Transacao']!=transacao]
        

        for _ , LinhaC in dataCommit.iterrows():
            
            for _ , LinhaDF in dataFrame.iterrows():
               
                
                if ( LinhaC['Operacao'] == LinhaDF['Operacao'] and 
                     LinhaC['Operacao'] == 'WL' ):
                    
                    if ( LinhaC['Objeto']  in LinhaDF['Predecessores'] or
                         LinhaDF['Objeto'] in LinhaDF['Predecessores']):
                                            
                        self.Espera.append(
                                (LinhaDF['Transacao'],LinhaC['Transacao'])
                            )

                        self.SysLockInfo.loc[
                                len(self.SysLockInfo)
                            ] = [tuplaDoCommit[0],LinhaC['Objeto'],tuplaDoCommit[1]+'L',3,LinhaC['Objeto']]
                        
                        return 
                    elif ( LinhaDF['Objeto']  in LinhaC['Predecessores'] and 
                           LinhaC['Operacao'] == LinhaDF['Operacao']     and 
                           LinhaC['Operacao'] == 'WL'):
                        
                        self.Espera.append(
                            (LinhaDF['Transacao'],LinhaC['Transacao'])
                        )

                        self.SysLockInfo.loc[
                                len(self.SysLockInfo)
                            ] = [tuplaDoCommit[0],LinhaC['Objeto'],tuplaDoCommit[1]+'L',3,LinhaC['Objeto']]
                        
                        return    
                    
                    elif ( 
                           LinhaC['Operacao'] == LinhaDF['Operacao'] and 
                           LinhaC['Operacao'] == 'WL'                and 
                           LinhaC['Status']   == 3):
                        
                        self.Espera.append(
                            (LinhaDF['Transacao'],LinhaC['Transacao'])
                        )

                        self.SysLockInfo.loc[
                                len(self.SysLockInfo)
                            ] = [tuplaDoCommit[0],LinhaC['Objeto'],tuplaDoCommit[1]+'L',3,LinhaC['Objeto']]
                        
                        return  
                          
        if ( cl.VerificaGrafoTemCiclo(self.Espera,self.tamanho)):
            return True

                
        self.SysLockInfo.loc[
            len(self.SysLockInfo)
        ] = [tuplaDoCommit[0],LinhaC['Objeto'],tuplaDoCommit[1]+'L',1,None]
        
        return

 

        
    def AdicionarBloqueio(self,operacao,objeto):
        database = self.Logico.Database
        
        if objeto == database.nome:

            if ( 'W' == operacao or 'U' == operacao ):
                if ( not(database.ilock[0]) ):
                    return 3,[]
                if ( database.lock[0] ): 
                    database.lock  = ( False , operacao )  
                
                else: 
                    return 3,[]

            if ( 'R' == operacao ):
                if  ( database.lock[1] == 'U' ): return 3,[]
                else:                            return 1,[]

        #===============================================================    
        
        numero = self.AddBlock(database,operacao,objeto,'a')
        
        if (numero != None):return numero
        
        for area in database.lista:
            numero = self.AddBlock(area,operacao,objeto,'t')             
            if (numero != None):return numero

            for tabela in area.lista: 
                numero = self.AddBlock(tabela,operacao,objeto,'p')
                if (numero != None):return numero
           
                for pagina in tabela.lista:
                    numero = self.AddBlock(pagina,operacao,objeto,'tu')
                    if (numero != None):return numero
        return 1,[]




    def AddBlock(self,Pai,operacao,objeto,chartype):
        for filho in Pai.lista:
            if ( objeto == filho.nome and 
                  not(filho.ilock[0]) and 
                  operacao != 'R'):
                return 3,self.ListaPredecessor(filho,chartype)
                

            if  ( not( Pai.lock[0] ) and object==filho.nome ): 
                filho.lock = ( False , operacao )
             
            if ( objeto == filho.nome ):
                if ( 'W' == operacao or 'U' == operacao ):
                    if ( filho.lock[0] ): 
                        filho.lock = ( False , operacao )
                        self.IntencionalBloqueios(chartype,filho,operacao)
                        return 1,self.ListaPredecessor(filho,chartype)
                    
                    else:                
                        return 3,self.ListaPredecessor(filho,chartype)
                
                if ( 'R' == operacao ):
                    if ( filho.lock[1] == 'U' ): return 3,self.ListaPredecessor(filho,chartype)
                    if ( filho.lock[1] == 'C' ): return 3,self.ListaPredecessor(filho,chartype)
                    else :                       return 1,self.ListaPredecessor(filho,chartype)
         
        return None


    def IntencionalBloqueios(self,chartype,type,operacao):    
    
        if   'a' == chartype:
            type.predecessor.ilock = (False,operacao)
        
        elif 't' == chartype: 
            type.predecessor.ilock = (False,operacao)
            type.predecessor.predecessor.ilock  = (False,operacao) 

        
        elif 'p' == chartype:
            type.predecessor.ilock              = (False,operacao)
            type.predecessor.predecessor.ilock  = (False,operacao) 
            type.predecessor.predecessor.predecessor.predecessor.ilock  = (False,operacao) 

        
        elif 'tu' == chartype:
            type.predecessor.ilock                          = (False,operacao)
            type.predecessor.predecessor.ilock              = (False,operacao) 
            type.predecessor.predecessor.predecessor.ilock  = (False,operacao) 
            type.predecessor.predecessor.predecessor.predecessor.ilock  = (False,operacao) 

            



    def ListaPredecessor(self,type,chartype):
        if   'a' == chartype:
            return [type.predecessor.nome] 
        
        elif 't' == chartype: 
            return [type.predecessor.nome]
        
        elif 'p' == chartype:
            return [type.predecessor.nome, type.predecessor.predecessor.nome] 
        
        elif 'tu' == chartype:
            return [type.predecessor.nome,type.predecessor.predecessor.nome,type.predecessor.predecessor.predecessor.nome]



