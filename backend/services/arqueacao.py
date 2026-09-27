import math

CONFIG_TANQUES = {
    10000.0: {"raio": 0.955, "comprimento": 3.65},
    15000.0: {"raio": 0.955, "comprimento": 5.45},
    20000.0: {"raio": 0.955, "comprimento": 7.25},
    7500.0:  {"raio": 0.955, "comprimento": 2.64},
}

def calcular_volume_por_regua(capacidade_maxima: float, altura_cm: float) -> float:
    if altura_cm <= 0:
        return 0.0
    if altura_cm >= 191.0:
        return float(capacidade_maxima)

    config = CONFIG_TANQUES.get(capacidade_maxima)
    h = altura_cm / 100.0

    if config:
        r = config["raio"]
        l = config["comprimento"]
        termo_acos = math.acos((r - h) / r)
        termo_raiz = (r - h) * math.sqrt(max(0.0, 2 * r * h - h**2))
        area_liquido = (r**2 * termo_acos) - termo_raiz
        volume_litros = area_liquido * l * 1000.0
        return round(volume_litros, 1)

    r = 0.955
    termo_acos = math.acos((r - h) / r)
    termo_raiz = (r - h) * math.sqrt(max(0.0, 2 * r * h - h**2))
    fracao_cheio = ((r**2 * termo_acos) - termo_raiz) / (math.pi * r**2)
    return round(capacidade_maxima * fracao_cheio, 1)
