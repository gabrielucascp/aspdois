class Trafo:
    def __init__(self, nome_trafo, reatancia_indutiva, geometria):
        self.nome_trafo = nome_trafo
        self.zfase = reatancia_indutiva*60
        self.admitancia = 1/self.zfase
        self.geometria = geometria
        self.parametros = complex(self.zfase)

