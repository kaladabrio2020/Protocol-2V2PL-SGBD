class Protocolo2v2pl:
    SysLockInfo = []
    def __init__(self,Logico): self.Logico = Logico

    def SetSysLockInfo(self,schedule):
        for tupla in schedule:

            if ( tupla[1] == 'C'):
                self.Commit(tupla)  
            else:
                Status = self.AdicionarBloqueio(tupla[1],tupla[2])
                self.SysLockInfo.append(
                    (tupla[0],tupla[2],tupla[1]+'l',Status)
                )
        print(self.SysLockInfo)
        
            
    def Commit(self,tuplaDoCommit):
    
        for tupla in self.SysLockInfo:
            pass
            
 

        
    def AdicionarBloqueio(self,operacao,objeto):
        database = self.Logico.Database
        if objeto == database.nome:
            if ( 'W' == operacao or 'U' == operacao ):
                if ( database.lock[0] ): database.lock  = ( False , operacao )  
            
                else: return 3

            if ( 'R' == operacao ):
                if  ( database.lock[1] == 'U' ): return 3
                else:                            return 1
        
        #===============================================================     
        for area in database.lista:
            if  ( not( self.Logico.Database.lock[0] ) ): 
                area.lock = ( False , operacao )

            if ( objeto == area.nome ):
                if ( 'W' == operacao or 'U' == operacao ):
                    if ( area.lock[0] ): 
                        area.lock = ( False , operacao )
                        self.IntencionalBloqueios('a',area,operacao)
                        return 1
                    else:                
                        return 3
                
                if ( 'R' == operacao ):
                    if ( area.lock[1] == 'U' ): return 3
                    else :                      return 1  

            #==============================================================
            for tabela in area.lista:
                if ( not ( area.lock[0] )):
                    tabela.lock = ( False , operacao )

                if ( objeto == tabela.nome ):
                    print(objeto == tabela.nome)
                    if ( 'W' == operacao or 'U' == operacao ):
                        if ( tabela.lock[0] ):
                            tabela.lock = ( False,operacao )
                            self.IntencionalBloqueios('t',tabela,operacao)                            
                            return 1

                        else: 
                            return 3


                    if ( 'R' == operacao ):
                        if ( tabela.lock[1] == 'U' ): return 3
                        else :                        return 1  
     

                #=============================================================
                for  pagina in tabela.lista:
                    if ( not ( tabela.lock[0] )):
                        pagina.lock = ( False , operacao )
                     
                    if ( objeto == pagina.nome ):
                        if ( 'W' == operacao or 'U' == operacao ):
                            if ( pagina.lock[0] ):
                                pagina.lock = ( False , operacao )
                                self.IntencionalBloqueios('p',pagina,operacao)
                                return 1
                            else: 
                                return 3

                        if ( 'R' == operacao ):
                            if ( pagina.lock[1] == 'U' ): return 3
                            else :                        return 1

                    #+========================================================
                    for  tupla in pagina.lista:
                        if ( not ( tupla.lock[0] )): 
                            tupla.lock = ( False , operacao )

                        if ( objeto == tupla.nome ):
                            if ( 'W' == operacao or 'U' == operacao ):
                                if ( tupla.lock[0] ):
                                    tupla.lock = ( False,operacao )
                                    self.IntencionalBloqueios('tu',tupla,operacao)
                                    return 1
                                else:             
                                    return 3
                                
                            if ( 'R' == operacao ):
                                if ( tupla.lock[1] == 'U' ): return 3
                                else :                       return 1
        return 1
        
                    
    def IntencionalBloqueios(self,chartype,type,operacao):    
    
        if   'a' == chartype:
            type.predecessor.lock = (False,operacao)
        
        elif 't' == chartype: 
            type.predecessor.lock             = (False,operacao)
            type.predecessor.predecessor.lock = (False,operacao)  
        
        elif 'p' == chartype:
            type.predecessor.lock                         = (False,operacao)
            type.predecessor.predecessor.lock             = (False,operacao) 
            type.predecessor.predecessor.predecessor.lock = (False,operacao) 
        
        elif 'tu' == chartype:
            type.predecessor.lock                                     = (False,operacao)
            type.predecessor.predecessor.lock                         = (False,operacao) 
            type.predecessor.predecessor.predecessor.lock             = (False,operacao) 
            type.predecessor.predecessor.predecessor.predecessor.lock = (False,operacao)