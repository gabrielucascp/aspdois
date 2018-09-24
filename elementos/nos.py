import numpy
from settings import DADOS_PU
from mecanicas.pu import Pu

class Conexoes(Pu):
    def __init__(self, numero_no, tipo_no, setor,
                    *args, 
                    potencia_ativa=None, 
                    potencia_reativa=None, 
                    tensao=None, 
                    fase=None, 
                    DADOS_PU=DADOS_PU):
        '''
            argumentos:
            argumentos obrigatórios:
            numero_no = int
            tipo_no = 'ger' para geracao, 'slack' para slack e 'carga' para carga
            argumentos optativos:
            linhas (número ilimitado)
            argumentos chave-valor:
            potencia_ativa, potencia_reativa, tensao e fase
        '''
        Pu.__init__(self,setor, DADOS_PU)
        self.setor = setor
        self.tipo_no = tipo_no
        self.numero_no = numero_no
        self.conectados = args
        self.lista_conexoes = self._lista_conexoes()
        self.admitancia_total = self._admitancia_total()
        # definindo parâmetros do método de gauss
        self.potencia_ativa = potencia_ativa
        if self.potencia_ativa:
            self.potencia_ativa = potencia_ativa/self.sbase
        self.potencia_reativa = potencia_reativa
        if self.potencia_reativa:
            self.potencia_reativa = potencia_reativa/self.sbase
        self.tensao = tensao
        if self.tensao:
            self.tensao = tensao/self.vbase
        self.fase = fase
        # estimativas iniciais
        if tipo_no == 'carga':
            self.tensao = 1
            self.fase = 0
        elif tipo_no == 'geracao':
            self.fase = 0
        elif tipo_no == 'slack':
            self.tensao = 1
            self.fase = 0

    def _lista_conexoes(self):
        resposta = []
        for elemento in self.conectados:
            resposta.append(str(elemento))
        return resposta

    def _admitancia_total(self):
        admitancia_total = 0
        for conectado in self.conectados:
            params = conectado.parametros
            if len(params) == 2:
                admitancia_total += params[1]
                admitancia_total += 1/params[0]
            else:
                admitancia_total += params
        return admitancia_total*self.zbase


class Ybarra(Pu):
    def __init__(self, *args, DADOS_PU=DADOS_PU):
        '''
            deve receber como argumentos
            vbase, sbase e após isso
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

                


        
        











            
    
