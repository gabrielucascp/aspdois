from elementos import linhas, trafos
from elementos.nos import Conexoes
from mecanicas.ybarra import Ybarra

# ESCREVENDO O PROGRAMA PROPRIAMENTE DITO
linha1 = linhas.Linha(  nome_linha='linha1',
                        comprimento=32E3,
                        geometria='transposta',
                        resistencia_dc=1.47E-5,
                        raio=2.5E-2, 
                        geminado=True, 
                        qts_geminados=2, 
                        distancia_a_b=3.5, 
                        distancia_b_c=4,
                        distancia_c_a=7.5,
                        distancia_geminados=0.4,
                        )

linha2 = linhas.Linha(  nome_linha="linha2",
                        comprimento=250E3,
                        geometria='triangular',
                        resistencia_dc=11.4844E-5,
                        raio=2.5E-2,
                        geminado=True,
                        qts_geminados=3,
                        distancia_fases=4,
                        distancia_geminados=.4,
                        )

trafo1 = trafos.Trafo( nome_trafo='trafo1',
                        reatancia_indutiva=12,
                        geometria="estrela-triangulo")

# argumentos: numero_no, tipo_no, setor, *linhas
no1 = Conexoes(1, 'slack', 1, linha1, linha2, trafo1)
no2 = Conexoes(2, 'carga', 1, linha1, potencia_ativa=10, potencia_reativa=20)
ybarra = Ybarra(no1, no2)

print(ybarra.gera_matriz())