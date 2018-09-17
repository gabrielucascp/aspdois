import math
import cmath

class Linha:
    '''
        No caso de geometria triangular:
        argumentos: (comprimento = inteiro
                    raio = inteiro
                    geminado = boleano
                    qts_geminados = inteiro, apenas se geminado for verdadeiro
                    distancia_fases = inteiro
                    resistencia_dc = inteiro
                    )
        Já no caso de geometria triangular:
        argumentos: (comprimento = inteiro
                    raio = inteiro
                    geminado = boleano
                    qts_geminados = inteiro, apenas se geminado for verdadeiro
                    distancia_a_b = inteiro
                    distancia_b_c = inteiro
                    distancia_c_a = inteiro
                    resistencia_dc = inteiro
                    )
    '''
    def __init__(self, **kwargs):
        self.comprimento = kwargs['comprimento']
        self.resistencia_dc = kwargs['resistencia_dc']
        self.raio = kwargs['raio'] * 0.7788
        self.geometria = kwargs['geometria']
        if kwargs['geminado']:
            if kwargs['qts_geminados'] == 2:
                self.raio_medio_geometrico = (self.raio * 
                                                kwargs['distancia_geminados']) ** (1/2)
            elif kwargs['qts_geminados'] == 3:
                self.raio_medio_geometrico = ((kwargs['distancia_geminados'] * 
                                                self.raio) ** 2) ** (1/3)
            elif kwargs['qts_geminados'] == 4:
                self.raio_medio_geometrico = (((kwargs['distancia_geminados']** 2) +
                                               kwargs['distancia_geminados'] * (2 ** (1/2))) *
                                               self.raio) ** (1/4)
            else:
                print(f'Erro. Este programa não pode calcular {kwargs['qts_geminados']} \
                        geminados. Tente um valor de 2 a 4')
                raise
        else:
            self.raio_medio_geometrico = self.raio

        if kwargs['geometria'] == 'triangular':
            self.distancia_fases = kwargs['distancia_fases']
        elif kwargs['geometria'] == 'transposta':
            self.distancia_a_b = kwargs['distancia_a_b']
            self.distancia_b_c = kwargs['distancia_b_c']
            self.distancia_c_a = kwargs['distancia_c_a']
        else:
            print(f'Erro. Este programa não suporta a geometria {kwargs['geometria']}.\
                    tente usar geometria transposta ou triangular')
        
    def calcular_parametros(self):
        GMR = self.raio_medio_geometrico
        resistencia = self.resistencia_dc * self.comprimento

        if self.geometria == 'triangular':
            GMD = self.distancia_fases            
            L_fase = 2E-7 * math.log(GMD/GMR)
        else:
            GMD = (self.distancia_a_b*self.distancia_b_c*self.distancia_c_a)**(1/3)
            L_fase = 2E-7 * math.log(GMD/GMR)

        Z_fase = complex(resistencia, 60*L_fase)

        if self.comprimento >= 80 and self.comprimento < 250:
            C_fase = ((2*3.14*8.85E-12)/math.log(GMD/GMR))
            Y_fase = complex(0,60*C_fase)
            return (Z_fase*self.comprimento, Y_fase*self.comprimento/2)
        elif self.comprimento >= 250:
            C_fase = ((2*3.14*8.85E-12)/math.log(GMD/GMR))
            Y_fase = complex(0,60*C_fase)
            y = (Z_fase*Y_fase)**(1/2)
            Z_linha = Z_fase * cmath.sinh(y*self.comprimento)/(y*self.comprimento)
            Y_linha = Y_fase * cmath.tanh(y*self.comprimento/2)/(y*self.comprimento/2)
            return (Z_linha, Y_linha)
        else:
            return Z_fase*self.comprimento
