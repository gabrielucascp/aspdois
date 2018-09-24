from settings import DADOS_PU
from mecanicas.pu import Pu

class Ybarra(Pu):
    def __init__(self, *args, DADOS_PU=DADOS_PU):
        '''
            argumentos:
            os objetos Conexoes, correspondetes aos nós.
        '''
        self.DADOS_PU = DADOS_PU
        self.nos = args #args = nos
        self.ordem_matriz = len(args)
        self.nos_conectados = self._pega_nos_conectados()

    def _pega_nos_conectados(self):
        sera_se_achou = []
        for i in self.nos:
            sera_se_achou_dentro = []
            for j in self.nos:
                Pu.__init__(self, j.setor, self.DADOS_PU)
                if i.numero_no != j.numero_no:
                    sera_se_achou_dentro.append(i.numero_no)
                    sera_se_achou_dentro.append(j.numero_no)
                    for k,linha in enumerate(i.lista_conexoes):
                        if linha in j.lista_conexoes:
                            sera_se_achou_dentro.append(j.conectados[k].admitancia*self.zbase)
                else:
                    sera_se_achou.append([i.numero_no, i.numero_no, i.admitancia_total*self.zbase])
            sera_se_achou.append(sera_se_achou_dentro)
        return sera_se_achou

    def gera_matriz(self):
        ibase = self.sbase/self.vbase
        zbase = self.vbase/ibase
        matriz_y = numpy.zeros((self.ordem_matriz,self.ordem_matriz), numpy.complex_)
        for i,l in enumerate(matriz_y):
            for j,l in enumerate(matriz_y):
                for element in self.nos_conectados:
                    if (i + 1) == element[0] and (j + 1) == element[1]:
                        if i == j:
                            matriz_y[i,j] = element[2]*zbase
                        else:
                            matriz_y[i,j] = -element[2]*zbase
                        break
        return matriz_y