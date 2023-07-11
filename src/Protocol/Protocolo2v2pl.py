import pandas   as pd
from ..Protocol import Ciclos as cl

class Protocolo2v2pl:
    def __init__(self,Logico,tamanho,schedule): 
        self.tamanho     = tamanho
        self.Logico      = Logico
        self.string      = ''
        self.Espera      = []
        self.schedule    = schedule
        self.NewSchedule = []
        self.OrdemCommit = []
        self.SysLockInfo = pd.DataFrame({
            'Transacao':[],
            'Objeto'   :[],
            'Operacao' :[],
            'Status'   :[],
            'Predecessores':[]
        })


    def GetString(self):      return self.string    
    def GetEspera(self):      return self.Espera
    def GetNewSchedule(self): return self.NewSchedule
    
    def SetSysLockInfo(self):
        
        for tupla in self.schedule:


            if ( tupla[1] == 'C'):
                self.OrdemCommit.append(tupla[0])

                if ( self.Commit(tupla) ):
                    self.string += 'ENTROU EM DEAD LOCK\n'+self.ultimoEscalonado(tupla)   
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
                self.string += 'ENTROU EM DEAD LOCK\n'+self.ultimoEscalonado(tupla)
                return self.string


        if ( cl.VerificaGrafoTemCiclo(self.Espera,self.tamanho)):
            self.string += 'ENTROU EM DEAD LOCK\n'+self.ultimoEscalonado(tupla)
            return self.string
        
        if ( len(self.Espera)!=0 ): self.Escalonamento()
        else:                       self.Removendo()
    
    def ultimoEscalonado(self,tupla):
        lista = []
        for tuplas in self.schedule:
            
            if (tupla[0] == tuplas[0]):
                lista.append(tuplas)
        return str(lista)

    def Escalonamento(self):
        lista = []

        for tuplaE in self.Espera:
            for i in tuplaE:
                
                for tuplaS in self.schedule:
                    if (tuplaS[0] == i and not(i in lista)):
                        self.NewSchedule.append(tuplaS)
                lista.append(i)
                    

    def Escalonado(self,index):
        for tupla in self.schedule:
            if (tupla[0] == index):
                self.NewSchedule.append(tupla)


    def BooleanoCommit(self,index , oper,NewSchedule):
        for tupla in NewSchedule: 
            if (index in tupla and oper in tupla):return True
        return False
    


    def EscalonadoOrdem(self):   
        for index in self.OrdemCommit:
            for tupla in self.schedule:
                if (tupla[0] == index and tupla[1]!= 'C'):
                    self.NewSchedule.append(tupla) 
        
        for index in reversed(self.OrdemCommit):            
            for tupla in self.schedule:
                if (tupla[1] == 'C' and tupla[0] == index):
                    if not(self.BooleanoCommit(tupla[0],tupla[1],self.NewSchedule)):    
                        self.NewSchedule.append(tupla)  
                
        
        

    def Removendo(self):   
        booleano = True
        for _ , linhas in self.SysLockInfo.iterrows():
            if (linhas['Status'] != 1):booleano = False
    
        if (booleano):
            self.EscalonadoOrdem()
            return

        
        Data = self.SysLockInfo.loc[ self.SysLockInfo['Operacao'] == 'CL' ]
        Data = Data.drop(Data.index[0])
        
        GetData = self.SysLockInfo.loc[self.SysLockInfo['Transacao']==Data['Transacao'].values[0]]
        for _ , linhas in GetData.iterrows():
            if (linhas['Status'] != 1):return

        
        self.Escalonado(Data['Transacao'].values[0])
        self.SysLockInfo.drop(GetData.index,inplace=True) 
        
        for linha in reversed(self.Espera):
            self.string += self.SysLockInfo.drop(columns='Predecessores').to_string()+'\n'
            self.Escalonado(linha[1])
            self.SysLockInfo.drop(self.SysLockInfo.loc[
                self.SysLockInfo['Transacao'] == linha[1]
            ].index,inplace=True)
        
            


    def Commit(self,tuplaDoCommit):
        transacao    = tuplaDoCommit[0]
        
        dataCommit   = self.SysLockInfo.loc[self.SysLockInfo['Transacao'] == transacao]
        
        dataFrame    = self.SysLockInfo[self.SysLockInfo['Transacao']!=transacao]

        
        for _ , LinhaC in dataCommit.iterrows():
            for _ , LinhaDF in dataFrame.iterrows():
                
                if ( LinhaC['Operacao'] != LinhaDF['Operacao'] and 
                    LinhaDF.name < LinhaC.name):
                                                            
                    self.Espera.append(
                            (LinhaDF['Transacao'],LinhaC['Transacao'])
                        )

                    self.SysLockInfo.loc[
                            len(self.SysLockInfo)
                        ] = [tuplaDoCommit[0],LinhaC['Objeto'],tuplaDoCommit[1]+'L',3,LinhaC['Objeto']]
                    return


        for _ , LinhaC in dataCommit.iterrows():
            
            for _ , LinhaDF in dataFrame.iterrows():
                    
                if ( LinhaC['Operacao'] == LinhaDF['Operacao'] and 
                     LinhaC['Operacao'] == 'WL' ):
                

                    if ( LinhaC.name < LinhaDF.name ):
                        self.SysLockInfo.loc[
                                len(self.SysLockInfo)
                            ] = [tuplaDoCommit[0],LinhaC['Objeto'],tuplaDoCommit[1]+'L',1,LinhaC['Objeto']]
                        return

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

        if (len(self.SysLockInfo)!=0):
            data = self.SysLockInfo.loc[self.SysLockInfo['Transacao']==tuplaDoCommit[0]]
            self.SysLockInfo.loc[ len(self.SysLockInfo) ] = [tuplaDoCommit[0],data['Objeto'].values[0],tuplaDoCommit[1]+'L',1,None]       
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
            type.predecessor.predecessor.predecessor.ilock  = (False,operacao) 

        
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



