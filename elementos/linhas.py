import math
import cmath

class Linha:
    '''
        No caso de geometria triangular:
        argumentos: (
                    nome_linha = preferencialmente nome da variavel
                    comprimento = numero
                    raio = numero
                    geminado = boleano
                    qts_geminados = numero, apenas se geminado for verdadeiro
                    distancia_geminados = numero, apenas se geminado for verdadeiro
                    distancia_fases = numero
                    resistencia_dc = numero
                    geometria = string
                    )
        Ja no caso de geometria transposta:
        argumentos: (
                    nome_linha = preferencialmente nome da variavel
                    comprimento = numero
                    raio = numero
                    geminado = boleano
                    qts_geminados = numero, apenas se geminado for verdadeiro
                    distancia_geminados = numero, apenas se geminado for verdadeiro
                    distancia_a_b = numero
                    distancia_b_c = numero
                    distancia_c_a = numero
                    resistencia_dc = numero
                    geometria = string
                    )
    '''
    def __init__(self, **kwargs):
        self.admitancia = 0
        self.nome_linha = kwargs['nome_linha']
        self.comprimento = kwargs['comprimento']
        self.resistencia_dc = kwargs['resistencia_dc']
        self.raio = kwargs['raio'] * 0.7788
        self.raio_c = kwargs['raio']
        self.geometria = kwargs['geometria']
        self.geminado = kwargs.get('geminado',False)
        self.qts_geminados = kwargs.get('qts_geminados',None)
        self.distancia_geminados = kwargs.get('distancia_geminados',None)
        self.distancia_geminados = self.qts_geminados
        self._raio_medio_geometrico()
        if kwargs['geometria'] == 'triangular':
            self.distancia_fases = kwargs['distancia_fases']
        elif kwargs['geometria'] == 'transposta':
            self.distancia_a_b = kwargs['distancia_a_b']
            self.distancia_b_c = kwargs['distancia_b_c']
            self.distancia_c_a = kwargs['distancia_c_a']
        else:
            raise EnvironmentError(f'''Erro. Este programa nao suporta a geometria {kwargs['geometria']}.
                    tente usar geometria transposta ou triangular''')
        # Isso deve ser consultado após gerar a linha
        self.parametros = self._calcular_parametros()
    
    def __repr__(self):
        return self.nome_linha

    def _raio_medio_geometrico(self):
        if self.geminado:
            if self.qts_geminados == 2:
                self.raio_medio_geometrico = (self.raio * self.distancia_geminados) ** (1/2)
                self.raio_medio_geometrico_c = (self.raio_c * 
                                                self.distancia_geminados) ** (1/2)
            elif self.qts_geminados == 3:
                self.raio_medio_geometrico = ((self.distancia_geminados * 
                                                self.raio) ** 2) ** (1/3)
                self.raio_medio_geometrico_c = ((self.distancia_geminados * 
                                                self.raio_c) ** 2) ** (1/3)
            elif self.qts_geminados == 4:
                self.raio_medio_geometrico = (((self.distancia_geminados** 2) +
                                               self.distancia_geminados * (2 ** (1/2))) *
                                               self.raio) ** (1/4)
                self.raio_medio_geometrico_c = (((self.distancia_geminados** 2) +
                                               self.distancia_geminados * (2 ** (1/2))) *
                                               self.raio_c) ** (1/4)
            else:
                raise EnvironmentError(f'''Erro. Este programa não pode calcular {self.qts_geminados}
                                        geminados. Tente um valor de 2 a 4''')
        else:
            self.raio_medio_geometrico = self.raio
            self.raio_medio_geometrico_c = self.raio_c
        
    def _calcular_parametros(self):
        GMR = self.raio_medio_geometrico
        resistencia = self.resistencia_dc * self.comprimento

        if self.geometria == 'triangular':
            GMD = self.distancia_fases            
            L_fase = 2E-7 * GMD / math.log(GMR)
        else:
            GMD = (self.distancia_a_b*self.distancia_b_c*self.distancia_c_a)**(1/3)
            L_fase = 2E-7 * GMD / math.log(GMR)

        Z_fase = complex(resistencia, 60*L_fase) # não multiplica o L_fase por 2*pi*60  ?

        if self.comprimento >= 80 and self.comprimento < 250:
            C_fase = ((2*3.14*8.85E-12)/math.log(GMD/self.raio_medio_geometrico_c))
            Y_fase = complex(0,60*C_fase)
            Z_fase = Z_fase*self.comprimento
            Y_fase = Y_fase*self.comprimento/2
            self.admitancia = 1/Z_fase + Y_fase
            return (Z_fase, Y_fase)
        elif self.comprimento >= 250:
            C_fase = ((2*3.14*8.85E-12)/math.log(GMD/self.raio_medio_geometrico_c))
            Y_fase = complex(0,60*C_fase)
            y = (Z_fase*Y_fase)**(1/2)
            Z_linha = Z_fase * cmath.sinh(y*self.comprimento)/(y*self.comprimento)
            Y_linha = Y_fase * cmath.tanh(y*self.comprimento/2)/(y*self.comprimento/2)
            Z_linha = Z_linha*self.comprimento
            Y_linha = Y_linha*self.comprimento/2
            self.admitancia = 1/Z_linha + Y_linha
            return (Z_linha, Y_linha)
        else:
            Z_fase = Z_fase*self.comprimento
            self.admitancia = 1/Z_fase
            return Z_fase

