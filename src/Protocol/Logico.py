class Database:
    def __init__(self, nome):
        self.nome  = nome
        self.lista = []
        self.lock  = (True,None)
        self.ilock  = (True,None)


class Area:
    def __init__(self, nome):
        self.nome  = nome
        self.lista = []
        self.lock  = (True,None)
        self.ilock  = (True,None)

        self.predecessor = None

class Tabela:
    def __init__(self, nome):
        self.nome  = nome
        self.lista = []
        self.lock  = (True,None)
        self.ilock  = (True,None)
        self.predecessor = None

class Pagina:
    def __init__(self, nome):
        self.nome  = nome
        self.lista = []
        self.lock  = (True,None)
        self.ilock  = (True,None)
        self.predecessor = None

class Tupla:
    def __init__(self, nome):
        self.nome  = nome
        self.lock  = (True,None)
        self.ilock  = (True,None)
        self.predecessor = None