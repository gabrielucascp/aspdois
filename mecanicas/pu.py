class Pu:
    def __init__(self, setor, DADOS_PU):
        self.sbase = DADOS_PU[0]
        self.vbase = DADOS_PU[setor]
        self.ibase = self.sbase/self.vbase
        self.zbase = self.vbase/self.ibase