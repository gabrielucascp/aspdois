import numpy

class Conexoes:
    def __init__(self, numero_no, *args):
        '''
            argumentos:
            1 argumento: numero do no
            n argumentos: conexoes do no
        '''
        self.numero_no = numero_no
        self.conectados = args
        self.lista_conexoes = self.func_lista_conexoes()
        self.admitancia_total = self.func_admitancia_total()

    def func_lista_conexoes(self):
        resposta = []
        for elemento in self.conectados:
            resposta.append(str(elemento))
        return resposta

    def func_admitancia_total(self):
        admitancia_total = 0
        for conectado in self.conectados:
            params = conectado.parametros
            if len(params) == 2:
                admitancia_total += params[1]
                admitancia_total += 1/params[0]
            else:
                admitancia_total += params
        return admitancia_total


class Ybarra:
    def __init__(self, *args):
        '''
            deve receber como argumentos os objetos Conexoes, correspondetes aos nós.
        '''
        self.nos = args
        self.ordem_matriz = len(args)
        self.nos_conectados = self._pega_nos_conectados()

    def _pega_nos_conectados(self):
        i = 0
        sera_se_achou = []
        for i in self.nos:
            sera_se_achou_dentro = []
            for j in self.nos:
                if i.numero_no != j.numero_no:
                    sera_se_achou_dentro.append(i.numero_no)
                    sera_se_achou_dentro.append(j.numero_no)
                    for i,linha in enumerate(i.lista_conexoes):
                        if linha in j.lista_conexoes:
                            sera_se_achou_dentro.append(j.conectados[i].admitancia)
                else:
                    sera_se_achou.append([i.numero_no, i.numero_no, i.admitancia_total])
            sera_se_achou.append(sera_se_achou_dentro)
        return sera_se_achou

    def gera_matriz(self):
        matriz_y = numpy.zeros((self.ordem_matriz,self.ordem_matriz))
        for i, linha in enumerate(matriz_y):
            for j, linha in enumerate(matriz_y):
                for element in self.nos_conectados:
                    if i == element[0] and j == element[1]:
                        matriz_y[i,j] = element[2]
        return matriz_y

                


        
        











            
    
