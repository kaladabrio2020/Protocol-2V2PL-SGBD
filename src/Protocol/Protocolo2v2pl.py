import pandas as pd


class Protocolo2v2pl:
    Espera      = []

    SysLockInfo = pd.DataFrame(
        {
            'Transacao':[],
            'Objeto'   :[],
            'Operacao' :[],
            'Status'   :[]
        }
    )


    def __init__(self,Logico): 
        self.Logico = Logico

    def SetSysLockInfo(self,schedule):
        for tupla in schedule:

            if ( tupla[1] == 'C'):
                self.Commit(tupla)  
            else:
                Status = self.AdicionarBloqueio(tupla[1],tupla[2])

                self.SysLockInfo.loc[
                    len(self.SysLockInfo)
                ] = [tupla[0],tupla[2],tupla[1]+'L',Status]
            
        print(self.Espera)
        
        print(self.SysLockInfo)

    def Commit(self,tuplaDoCommit):
        transacao    = tuplaDoCommit[0]

        dataCommit   = self.SysLockInfo.loc[self.SysLockInfo['Transacao'] == transacao]
        dataFrame    = self.SysLockInfo[self.SysLockInfo.index<transacao]
        
        for IndiceC , LinhaC in dataCommit.iterrows():
            for IndiceDF , LinhaDF in dataFrame.iterrows():
                if ( LinhaC['Operacao'] == LinhaDF['Operacao'] and 
                     LinhaC['Operacao'] == 'WL'   
                    ):
                    self.Espera.append(
                        (LinhaC['Transacao'] , LinhaDF['Transacao'])
                    )

                    self.SysLockInfo.loc[
                        len(self.SysLockInfo)
                    ] = [tuplaDoCommit[0],LinhaC['Objeto'],tuplaDoCommit[1]+'L',3]
    




            
 

        
    def AdicionarBloqueio(self,operacao,objeto):
        database = self.Logico.Database
        if objeto == database.nome:

            if ( 'W' == operacao or 'U' == operacao ):
                if ( database.lock[0] ): 
                    database.lock  = ( False , operacao )  
                else: 
                    return 3

            if ( 'R' == operacao ):
                if  ( database.lock[1] == 'U' ): return 3
                if  ( database.lock[1] == 'C' ): return 3
                else:                            return 1
        #===============================================================    
        #  
        numero = self.AddBlock(database,operacao,objeto)
        if (numero != None):return numero

        for area in database.lista:
            numero = self.AddBlock(area,operacao,objeto)  
            if (numero != None):return numero

            for tabela in area.lista: 
                numero = self.AddBlock(tabela,operacao,objeto)
                if (numero != None):return numero
           
                for pagina in tabela.lista:
                    numero = self.AddBlock(pagina,operacao,objeto)
                    if (numero != None):return numero
        return 1

    def AddBlock(self,Pai,operacao,objeto):

        for filho in Pai.lista:
            if  ( not( Pai.lock[0] ) ): 
                filho.lock = ( False , operacao )
             
            if ( objeto == filho.nome ):
                
                if ( 'W' == operacao or 'U' == operacao ):
                    if ( filho.lock[0] ): 
                        
                        filho.lock = ( False , operacao )
                        self.IntencionalBloqueios('a',filho,operacao)
                        return 1
                    else:                
                        return 3
                
                if ( 'R' == operacao ):
                    if ( filho.lock[1] == 'U' ): return 3
                    if ( filho.lock[1] == 'C' ): return 3
                    else :                       return 1  
        return None
    
    def IntencionalBloqueios(self,chartype,type,operacao):    
    
        if   'a' == chartype:
            type.predecessor.ilock = (False,operacao)
        
        elif 't' == chartype: 
            type.predecessor.ilock             = (False,operacao)
            type.predecessor.predecessor.ilock = (False,operacao)  
        
        elif 'p' == chartype:
            type.predecessor.lock                          = (False,operacao)
            type.predecessor.predecessor.ilock             = (False,operacao) 
            type.predecessor.predecessor.predecessor.ilock = (False,operacao) 
        
        elif 'tu' == chartype:
            type.predecessor.ilock                                     = (False,operacao)
            type.predecessor.predecessor.ilock                         = (False,operacao) 
            type.predecessor.predecessor.predecessor.ilock             = (False,operacao) 
            type.predecessor.predecessor.predecessor.predecessor.ilock = (False,operacao)