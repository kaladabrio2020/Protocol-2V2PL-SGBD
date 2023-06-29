class Database:
    def __init__(self, nome):
        self.nome = nome
        self.area = []


class Area:
    def __init__(self, nome):
        self.nome = nome
        self.tabela = []
        self.predecessor = None


class Tabela:
    def __init__(self, nome):
        self.nome = nome
        self.pagina = []
        self.predecessor = None


class Pagina:
    def __init__(self, nome):
        self.nome = nome
        self.Tupla = []
        self.predecessor = None


class Tupla:
    def __init__(self, nome):
        self.nome = nome
        self.predecessor = None