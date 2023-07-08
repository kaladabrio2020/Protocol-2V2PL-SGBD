class Database:
    def __init__(self, nome):
        self.nome = nome
        self.area = None

class Area:
    def __init__(self, nome):
        self.nome   = nome
        self.tabela = None
        self.predecessor = None

class Tabela:
    def __init__(self, nome):
        self.nome   = nome
        self.pagina = None
        self.predecessor = None

class Pagina:
    def __init__(self, nome):
        self.nome  = nome
        self.tupla = None
        self.predecessor = None

class Tupla:
    def __init__(self, nome):
        self.nome = nome
        self.predecessor = None