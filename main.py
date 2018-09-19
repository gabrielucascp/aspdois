import linhas
import nos

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

no1 = nos.Conexoes(1, linha1,linha2)
no2 = nos.Conexoes(2, linha1)
ybarra = nos.Ybarra(no1, no2)

# Definição dos nós para o programa

print(ybarra.gera_matriz())