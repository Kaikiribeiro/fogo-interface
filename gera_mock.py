import json, math, shutil

LARGURA, ALTURA, CELULA_M = 200, 130, 30
ROS = 9            # m/min
DURACAO = 360      # min

COMBUSTIVEIS = [
    {"codigo": 0, "nome": "Água", "queima": False, "cor": "#2c5870"},
    {"codigo": 3, "nome": "Campo limpo", "queima": True, "duracao_queima_min": 4, "cor": "#b2a662"},
    {"codigo": 4, "nome": "Cerrado típico", "queima": True, "duracao_queima_min": 14, "cor": "#748448"},
]

def eh_rio(x, y):
    return abs(x - (70 + 0.25 * y)) < 2

def gera(id_, vento_graus, vento_kmh, ix=150, iy=50):
    destino = math.radians((vento_graus + 180) % 360)
    vx, vy = math.sin(destino), -math.cos(destino)
    k = min(vento_kmh / 40, 0.9)

    chegada, combustivel, elevacao = [], [], []
    for y in range(ALTURA):
        for x in range(LARGURA):
            rio = eh_rio(x, y)
            if rio:
                cod = 0
            else:
                cod = 3 if (x // 25 + y // 25) % 2 == 0 else 4
            combustivel.append(cod)
            elevacao.append(round(412 + 0.05 * x + 6 * math.sin(x / 20) + 4 * math.cos(y / 15), 1))

            dx, dy = x - ix, y - iy
            d = math.hypot(dx, dy)
            cos_ang = 1 if d == 0 else (dx * vx + dy * vy) / d
            t = d * CELULA_M / (ROS * (1 + k * cos_ang))
            chegada.append(None if rio or t > DURACAO else round(t, 1))

    sim = {
        "id": id_,
        "grade": {"largura": LARGURA, "altura": ALTURA, "celula_m": CELULA_M},
        "limites": {"norte": -16.55, "sul": -16.585, "oeste": -49.20, "leste": -49.144, "crs": "EPSG:4326"},
        "parametros": {"vento_de_graus": vento_graus, "vento_kmh": vento_kmh, "umidade_pct": 8},
        "duracao_min": DURACAO,
        "combustiveis": COMBUSTIVEIS,
        "camadas": {"elevacao_m": elevacao, "combustivel": combustivel, "chegada_min": chegada},
    }
    with open(f"{id_}.json", "w", encoding="utf-8") as f:
        json.dump(sim, f)

gera("sim-001", 90, 32)
gera("sim-002", 180, 20)
gera("sim-003", 45, 45)
shutil.copy("sim-001.json", "simulacao.json")