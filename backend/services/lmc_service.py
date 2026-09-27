def calcular_lmc(estoque_inicial: float, recebimentos: float, vendas: float, estoque_fisico: float):
    """
    Realiza o balanco volumetrico diario e aplica a regra de tolerancia de 0.6% da ANP.
    """
    estoque_escritural = round(estoque_inicial + recebimentos - vendas, 1)
    perda_sobra = round(estoque_fisico - estoque_escritural, 1)

    base_calculo = estoque_inicial + recebimentos
    if base_calculo > 0:
        percentual = round((perda_sobra / base_calculo) * 100.0, 3)
    elif estoque_escritural > 0:
        percentual = round((perda_sobra / estoque_escritural) * 100.0, 3)
    else:
        percentual = 0.0

    # Margem de 0.6% da ANP
    if abs(percentual) <= 0.600:
        status_anp = "CONFORME"
    elif percentual < -0.600:
        status_anp = "PERDA_EXCESSIVA"
    else:
        status_anp = "SOBRA_EXCESSIVA"

    return {
        "estoque_escritural": estoque_escritural,
        "perda_sobra": perda_sobra,
        "percentual_variacao": percentual,
        "status_anp": status_anp
    }
