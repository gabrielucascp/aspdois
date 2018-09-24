DADOS_PU = [
    # o primeiro item corresponde ao sbase
    100000,
    # do segundo item em diante são as vbase de cada setor (começando da slack)
    1000,
    500,
]

class Pu:
    def __init__(self, setor, DADOS_PU):
        self.sbase = DADOS_PU[0]
        self.vbase = DADOS_PU[setor]
        self.ibase = self.sbase/self.vbase
        self.zbase = self.vbase/self.ibase