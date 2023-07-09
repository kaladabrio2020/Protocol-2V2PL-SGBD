from ..Protocol import Logico

class CriandoLogico:
    def __init__(self):
        #CRIANDO DATABASE
        self.Database = Logico.Database('DB')

        #CRINADO AREA
        self.Area_1   = Logico.Area('A1')
        self.Area_2   = Logico.Area('A2')

        #CRIANDO TABELA
        self.Tabela_1 = Logico.Tabela('T1')
        self.Tabela_2 = Logico.Tabela('T2')
        self.Tabela_3 = Logico.Tabela('T3')
        self.Tabela_4 = Logico.Tabela('T4')
        
        #CRIANDO PAGINAS
        self.Pagina_1 = Logico.Pagina('P1') 
        self.Pagina_2 = Logico.Pagina('P2')
        self.Pagina_3 = Logico.Pagina('P3')
        self.Pagina_4 = Logico.Pagina('P4')
        self.Pagina_5 = Logico.Pagina('P5')
        self.Pagina_6 = Logico.Pagina('P6')
        self.Pagina_7 = Logico.Pagina('P7')
        self.Pagina_8 = Logico.Pagina('P8')

        #CRIANDO TUPLAS
        self.Tupla_1 = Logico.Tupla('TP1')
        self.Tupla_2 = Logico.Tupla('TP2')
        self.Tupla_3 = Logico.Tupla('TP3')
        self.Tupla_4 = Logico.Tupla('TP4')
        self.Tupla_5 = Logico.Tupla('TP5')
        self.Tupla_6 = Logico.Tupla('TP6')
        self.Tupla_7 = Logico.Tupla('TP7')
        self.Tupla_8 = Logico.Tupla('TP8')
        self.Tupla_9 = Logico.Tupla('TP9')
        self.Tupla_10 = Logico.Tupla('TP10')
        self.Tupla_11 = Logico.Tupla('TP11')
        self.Tupla_12 = Logico.Tupla('TP12')
        self.Tupla_13 = Logico.Tupla('TP13')
        self.Tupla_14 = Logico.Tupla('TP14')
        self.Tupla_15 = Logico.Tupla('TP15')
        self.Tupla_16 = Logico.Tupla('TP16')


#-------------------------------------------------------------
        self.Area_1.predecessor = self.Database
        self.Area_2.predecessor = self.Database
        
        self.Tabela_1.predecessor = self.Area_1
        self.Tabela_2.predecessor = self.Area_1

        self.Tabela_3.predecessor = self.Area_2
        self.Tabela_4.predecessor = self.Area_2

#------------------------------------------------------------
        self.Pagina_1.predecessor = self.Tabela_1
        self.Pagina_2.predecessor = self.Tabela_1

        self.Pagina_3.predecessor = self.Tabela_2
        self.Pagina_4.predecessor = self.Tabela_2

        
        self.Pagina_5.predecessor = self.Tabela_3
        self.Pagina_6.predecessor = self.Tabela_3

        self.Pagina_7.predecessor = self.Tabela_4
        self.Pagina_8.predecessor = self.Tabela_4
#------------------------------------------------------------
        self.Tupla_1.predecessor  = self.Pagina_1
        self.Tupla_2.predecessor  = self.Pagina_1

        self.Tupla_3.predecessor  = self.Pagina_2
        self.Tupla_4.predecessor  = self.Pagina_2

        self.Tupla_5.predecessor  = self.Pagina_3
        self.Tupla_6.predecessor  = self.Pagina_3
        
        self.Tupla_7.predecessor  = self.Pagina_4
        self.Tupla_8.predecessor  = self.Pagina_4

        self.Tupla_9.predecessor  = self.Pagina_5
        self.Tupla_10.predecessor = self.Pagina_5

        self.Tupla_11.predecessor = self.Pagina_6
        self.Tupla_12.predecessor = self.Pagina_6

        self.Tupla_13.predecessor = self.Pagina_7
        self.Tupla_14.predecessor = self.Pagina_7

        self.Tupla_15.predecessor = self.Pagina_8
        self.Tupla_16.predecessor = self.Pagina_8

#---------------------------------------------------------------
        self.Database.lista = [self.Area_1,self.Area_2]
        
        self.Area_1.lista   = [self.Tabela_1,self.Tabela_2]
        self.Area_2.lista   = [self.Tabela_3,self.Tabela_4]

        self.Tabela_1.lista = [self.Pagina_1,self.Pagina_2]
        self.Tabela_2.lista = [self.Pagina_3,self.Pagina_4]
        self.Tabela_3.lista = [self.Pagina_5,self.Pagina_6]
        self.Tabela_4.lista = [self.Pagina_7,self.Pagina_8]

        self.Pagina_1.lista = [self.Tupla_1, self.Tupla_2  ]
        self.Pagina_2.lista = [self.Tupla_3, self.Tupla_4  ]
        self.Pagina_3.lista = [self.Tupla_5, self.Tupla_6  ]
        self.Pagina_4.lista = [self.Tupla_7, self.Tupla_8  ]
        self.Pagina_5.lista = [self.Tupla_9, self.Tupla_10 ]
        self.Pagina_6.lista = [self.Tupla_11, self.Tupla_12]
        self.Pagina_7.lista = [self.Tupla_13, self.Tupla_14]
        self.Pagina_8.lista = [self.Tupla_15, self.Tupla_16]


        

        