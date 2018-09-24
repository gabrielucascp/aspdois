import cmath

def iteracao_gauss(ybarra, *args):
    for i,no in enumerate(args):
        if no.tipo_no == 'ger':
            potencia_reativa = 0
            for j,no_ in enumerate(args):
                potencia_reativa += cmath.rect(no.tensao*ybarra[i,j]*no_.tensao, cmath.phase(ybarra[i,j])+no_.fase - no.fase)
            no.potencia_reativa = potencia_reativa.imag
        somatorio = 0
        for j,no_ in enumerate(args):
            if i != j:
                somatorio += cmath.rect(ybarra[i,j]*no_.tensao,cmath.phase(ybarra[i,j]) + no_.fase)
        no.tensao = (1/ybarra[i,i])*((no.potencia_ativa - potencia_reativa)/no.tensao - somatorio)


