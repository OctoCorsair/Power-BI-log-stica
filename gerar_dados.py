#!/usr/bin/env python3
"""Gera o conjunto de dados SINTÉTICO do dashboard de logística e tráfego.

Só usa a biblioteca padrão. A mesma seed gera sempre os mesmos arquivos.

    python gerar_dados.py --saida ../data
    python gerar_dados.py --seed 7 --viagens-por-dia 40 --inicio 2025-01-01 --fim 2026-10-31
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import random
from datetime import date, datetime, timedelta

# ----------------------------------------------------------------------------
# Geografia
# ----------------------------------------------------------------------------
CIDADES = [  # nome, uf, lat, lon, peso (quantos clientes)
    ("São Paulo", "SP", -23.5505, -46.6333, 14), ("Guarulhos", "SP", -23.4543, -46.5333, 6),
    ("Campinas", "SP", -22.9099, -47.0626, 8), ("Santos", "SP", -23.9608, -46.3336, 6),
    ("Sorocaba", "SP", -23.5015, -47.4526, 5), ("São José dos Campos", "SP", -23.2237, -45.9009, 5),
    ("Ribeirão Preto", "SP", -21.1775, -47.8103, 7), ("Jundiaí", "SP", -23.1857, -46.8978, 4),
    ("Santo André", "SP", -23.6737, -46.5432, 5), ("Osasco", "SP", -23.5329, -46.7917, 5),
    ("Piracicaba", "SP", -22.7253, -47.6492, 4), ("Bauru", "SP", -22.3246, -49.0871, 4),
    ("Franca", "SP", -20.5386, -47.4009, 3), ("São Carlos", "SP", -22.0087, -47.8909, 3),
    ("Araraquara", "SP", -21.7947, -48.1756, 3), ("Taubaté", "SP", -23.0204, -45.5559, 3),
    ("Mogi das Cruzes", "SP", -23.5225, -46.1883, 4), ("Limeira", "SP", -22.5647, -47.4017, 3),
    ("Rio de Janeiro", "RJ", -22.9068, -43.1729, 5), ("Curitiba", "PR", -25.4284, -49.2733, 4),
    ("Belo Horizonte", "MG", -19.9167, -43.9345, 4),
]

HUBS = [  # id, nome, cidade, uf, lat, lon, docas, peso
    ("HUB01", "CD Guarulhos", "Guarulhos", "SP", -23.4543, -46.5333, 24, 0.40),
    ("HUB02", "CD Campinas", "Campinas", "SP", -22.9099, -47.0626, 16, 0.25),
    ("HUB03", "CD Santos", "Santos", "SP", -23.9608, -46.3336, 12, 0.20),
    ("HUB04", "CD Ribeirão Preto", "Ribeirão Preto", "SP", -21.1775, -47.8103, 10, 0.15),
]

RODOVIAS = {
    "HUB01": ["Via Dutra (BR-116)", "Fernão Dias (BR-381)", "Ayrton Senna (SP-070)",
              "Anhanguera (SP-330)", "Bandeirantes (SP-348)", "Castello Branco (SP-280)",
              "Rodoanel (SP-021)"],
    "HUB02": ["Anhanguera (SP-330)", "Bandeirantes (SP-348)", "Dom Pedro I (SP-065)",
              "Santos Dumont (SP-075)", "Campinas-Monte Mor (SP-101)"],
    "HUB03": ["Imigrantes (SP-160)", "Anchieta (SP-150)", "Rodoanel (SP-021)",
              "Cônego Domênico Rangoni (SP-055)", "Via Dutra (BR-116)"],
    "HUB04": ["Anhanguera (SP-330)", "Cândido Portinari (SP-334)", "Washington Luís (SP-310)",
              "Faria Lima (SP-326)", "Atílio Balbo (SP-322)"],
}

SEGMENTOS = {
    "Varejo": ["Mercado", "Atacadão", "Empório", "Magazine"],
    "Indústria": ["Metalúrgica", "Plásticos", "Têxtil", "Fundição"],
    "E-commerce": ["Loja Virtual", "Mega Store", "Click"],
    "Farmacêutico": ["Drogaria", "Farma", "Laboratório"],
    "Alimentício": ["Padaria", "Frigorífico", "Distribuidora"],
    "Autopeças": ["Auto Center", "Retífica", "Peças"],
}
NOMES_EMPRESA = ["Aurora", "Bandeirante", "Central", "Dom Pedro", "Estrela", "Ipiranga", "Jaguar",
                 "Liberdade", "Monte Azul", "Nova Era", "Ouro Verde", "Paulista", "Real",
                 "Santa Clara", "Tropical", "União", "Vale Verde", "Horizonte", "Atlântica",
                 "Pioneira"]

# tipo: capacidade kg, consumo km/L, velocidade média km/h, serviço h/parada,
# pedágio R$/km, fator manutenção, raio de atuação km, (min, max) paradas
TIPOS = {
    "VUC":     (3000, 9.5, 34, 0.30, 0.09, 0.70, 70, (3, 7)),
    "Toco":    (6000, 6.5, 42, 0.40, 0.16, 0.90, 160, (3, 6)),
    "Truck":   (14000, 4.2, 50, 0.50, 0.28, 1.20, 400, (2, 5)),
    "Carreta": (28000, 2.6, 54, 0.60, 0.50, 1.60, 900, (1, 4)),
}
MARCAS = {"VUC": ["Renault", "Fiat", "Iveco"], "Toco": ["Mercedes-Benz", "Volkswagen", "Ford"],
          "Truck": ["Volvo", "Scania", "Mercedes-Benz"], "Carreta": ["Scania", "Volvo", "DAF"]}

PRIMEIROS = ["Adriano", "Bruno", "Carlos", "Diego", "Edson", "Fábio", "Gilberto", "Hélio", "Igor",
             "João", "Kleber", "Luiz", "Marcos", "Nelson", "Orlando", "Paulo", "Rafael", "Sérgio",
             "Thiago", "Valdir", "Wagner", "Antônio", "Roberto", "Cláudio", "Leandro", "Márcio",
             "José", "Fernando", "Ricardo", "Jorge"]
SOBRENOMES = ["Almeida", "Barbosa", "Cardoso", "Dias", "Ferreira", "Gomes", "Lima", "Martins",
              "Nascimento", "Oliveira", "Pereira", "Ramos", "Santos", "Teixeira", "Vieira",
              "Souza", "Rocha", "Araújo", "Costa", "Moreira"]

CONGESTIONAMENTO_HORA = {0: .01, 1: .01, 2: .01, 3: .01, 4: .02, 5: .03, 6: .12, 7: .36, 8: .44,
                         9: .28, 10: .08, 11: .05, 12: .07, 13: .06, 14: .06, 15: .08, 16: .18,
                         17: .42, 18: .48, 19: .30, 20: .07, 21: .03, 22: .02, 23: .01}
FATOR_HUB = {"HUB01": 1.35, "HUB02": 1.00, "HUB03": 1.15, "HUB04": 0.70}
FATOR_DIA = {0: 1.05, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.15, 5: 0.7, 6: 0.5}
FATOR_MES_CHUVA = {12: 1.2, 1: 1.25, 2: 1.25, 3: 1.2}
SAZONALIDADE = {1: .85, 2: .88, 3: .95, 4: .95, 5: 1.0, 6: .98, 7: .97, 8: 1.0, 9: 1.02,
                10: 1.08, 11: 1.28, 12: 1.35}
FATOR_DIA_SEMANA_VOLUME = {0: 1.05, 1: 1.1, 2: 1.1, 3: 1.05, 4: 1.0, 5: 0.55, 6: 0.12}
FERIADOS = {(1, 1), (4, 21), (5, 1), (9, 7), (10, 12), (11, 2), (11, 15), (12, 25)}

# tipo: (peso base, mediana de duração em min)
OCORRENCIAS = {
    "Congestionamento": (0.38, 35), "Obra na pista": (0.14, 25), "Acidente na via": (0.12, 55),
    "Clima adverso": (0.14, 30), "Pane mecânica": (0.04, 90), "Fiscalização": (0.07, 25),
    "Bloqueio/Interdição": (0.05, 70),
}
HORAS_SAIDA = [4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 18, 20, 22]
PESOS_SAIDA = [4, 10, 16, 16, 12, 9, 6, 3, 4, 3, 2, 2, 1, 1]

ANO_REF = 2026


def haversine(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 6371 * 2 * math.asin(math.sqrt(h))


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def escrever(caminho, cabecalho, linhas):
    with open(caminho, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cabecalho)
        w.writerows(linhas)


def fmt_dt(d):
    return d.strftime("%Y-%m-%d %H:%M:%S")


def gerar(args):
    rng = random.Random(args.seed)
    inicio = date.fromisoformat(args.inicio)
    fim = date.fromisoformat(args.fim)
    os.makedirs(args.saida, exist_ok=True)

    hubs = [dict(id=h[0], nome=h[1], cidade=h[2], uf=h[3], lat=h[4], lon=h[5], docas=h[6], peso=h[7])
            for h in HUBS]

    cidades_pool = [c for c in CIDADES for _ in range(c[4])]
    rng.shuffle(cidades_pool)
    nomes_usados = set()
    clientes = []
    for i in range(args.clientes):
        cidade = cidades_pool[i % len(cidades_pool)]
        seg = rng.choice(list(SEGMENTOS))
        tentativas_nome = 0
        while True:
            nome = f"{rng.choice(SEGMENTOS[seg])} {rng.choice(NOMES_EMPRESA)}"
            tentativas_nome += 1
            if nome not in nomes_usados:
                break
            if tentativas_nome > 30:
                nome += f" {cidade[0]}"
                if nome not in nomes_usados:
                    break
        nomes_usados.add(nome)
        clientes.append(dict(
            id=f"C{i + 1:03d}", nome=nome, cidade=cidade[0], uf=cidade[1], segmento=seg,
            prioridade=rng.choices(["A", "B", "C"], [0.2, 0.5, 0.3])[0],
            lat=round(cidade[2] + rng.uniform(-0.05, 0.05), 5),
            lon=round(cidade[3] + rng.uniform(-0.05, 0.05), 5)))

    veiculos = []
    por_tipo = args.veiculos // len(TIPOS)
    n = 0
    for tipo, cfg in TIPOS.items():
        for _ in range(por_tipo):
            n += 1
            ano = rng.randint(2014, 2025)
            letras = "".join(rng.choice("ABCDEFGHJKLMNPRSTUVWXYZ") for _ in range(3))
            placa = f"{letras}{rng.randint(0, 9)}{rng.choice('ABCDEFGHJ')}{rng.randint(10, 99)}"
            veiculos.append(dict(
                id=f"V{n:03d}", placa=placa, tipo=tipo, marca=rng.choice(MARCAS[tipo]), ano=ano,
                cap=cfg[0], kml=round(cfg[1] * rng.uniform(0.95, 1.05), 2), idade=ANO_REF - ano))

    motoristas = []
    usados = set()
    for i in range(args.motoristas):
        for _ in range(50):
            nome = f"{rng.choice(PRIMEIROS)} {rng.choice(SOBRENOMES)}"
            if nome not in usados:
                break
        else:
            nome = f"{nome} {i + 1}"
        usados.add(nome)
        exp = rng.randint(1, 30)
        skill = clamp(0.45 + 0.012 * exp + rng.gauss(0, 0.12), 0.15, 0.95)
        motoristas.append(dict(
            id=f"M{i + 1:03d}", nome=nome, cnh=rng.choices(["C", "D", "E"], [0.3, 0.2, 0.5])[0],
            exp=exp, turno=rng.choices(["Manhã", "Tarde", "Noite"], [0.55, 0.3, 0.15])[0],
            skill=skill))

    pools = {}
    for h in hubs:
        ordenados = sorted(clientes, key=lambda c: haversine((h["lat"], h["lon"]), (c["lat"], c["lon"])))
        for tipo, cfg in TIPOS.items():
            raio = cfg[6]
            pool = [c for c in ordenados
                    if haversine((h["lat"], h["lon"]), (c["lat"], c["lon"])) <= raio]
            pools[(h["id"], tipo)] = pool if len(pool) >= 6 else ordenados[:6]

    viagens, entregas, ocorrencias = [], [], []
    seq_v = seq_e = seq_o = 0
    dia = inicio
    while dia <= fim:
        meses = (dia.year - inicio.year) * 12 + dia.month - inicio.month
        fator = (FATOR_DIA_SEMANA_VOLUME[dia.weekday()] * SAZONALIDADE[dia.month]
                 * (1 + 0.012 * meses))
        if (dia.month, dia.day) in FERIADOS:
            fator *= 0.15
        if dia.month == 11 and dia.weekday() == 4 and dia.day + 7 > 30:  # Black Friday
            fator *= 1.3
        n_viagens = int(round(args.viagens_por_dia * fator * rng.uniform(0.9, 1.1)))
        n_viagens = min(n_viagens, len(veiculos), len(motoristas))
        preco_diesel = 5.80 + 0.02 * meses + 0.10 * math.sin(meses / 2.5) + rng.uniform(-0.04, 0.04)

        for veic, mot in zip(rng.sample(veiculos, n_viagens), rng.sample(motoristas, n_viagens)):
            seq_v += 1
            vid = f"V{seq_v:06d}"
            cap, kml_base, vel, servico, pedagio_km, f_manut, _, (pmin, pmax) = TIPOS[veic["tipo"]]
            hub = rng.choices(hubs, [h["peso"] for h in hubs])[0]
            pool = pools[(hub["id"], veic["tipo"])]
            paradas = rng.sample(pool, min(rng.randint(pmin, pmax), len(pool)))

            atual = (hub["lat"], hub["lon"])
            restantes = paradas[:]
            ordem, pernas = [], []
            fator_estrada = rng.uniform(1.18, 1.32)
            while restantes:
                prox = min(restantes, key=lambda c: haversine(atual, (c["lat"], c["lon"])))
                restantes.remove(prox)
                pernas.append(max(3.0, haversine(atual, (prox["lat"], prox["lon"])) * fator_estrada))
                ordem.append(prox)
                atual = (prox["lat"], prox["lon"])
            volta = max(3.0, haversine(atual, (hub["lat"], hub["lon"])) * fator_estrada)
            km_plan = sum(pernas) + volta

            carga_alvo = cap * rng.uniform(0.45, 0.98)
            brutos = [rng.uniform(0.5, 1.5) for _ in ordem]
            pesos = [carga_alvo * b / sum(brutos) for b in brutos]
            carga = sum(pesos)
            uso = carga / cap

            t_carga = 0.5
            dir_h = [km / vel for km in pernas]
            dur_plan = t_carga + sum(dir_h) + volta / vel + servico * len(ordem)

            hora = rng.choices(HORAS_SAIDA, PESOS_SAIDA)[0]
            saida = datetime(dia.year, dia.month, dia.day, hora, rng.randint(0, 59))

            f_mult = (FATOR_HUB[hub["id"]] * FATOR_DIA[dia.weekday()]
                      * FATOR_MES_CHUVA.get(dia.month, 1.0))
            horas_dir = max(1, int(math.ceil(sum(dir_h) + volta / vel)))
            atraso = 0.0
            for k in range(horas_dir):
                peso_h = 1.0 if k in (0, horas_dir - 1) else 0.25
                atraso += CONGESTIONAMENTO_HORA[(hora + k) % 24] * 60 * peso_h
            atraso *= 0.34 * f_mult * rng.lognormvariate(0, 0.35)

            p_inc = clamp(0.08 + 0.010 * dur_plan, 0.08, 0.30)
            qtd_inc = 1 if rng.random() < p_inc else 0
            if qtd_inc and rng.random() < 0.25:
                qtd_inc = 2
            atraso_mec = 0.0
            pendentes = []  # ocorrências desta viagem, ajustadas depois que a duração real é conhecida
            for _ in range(qtd_inc):
                tipos = list(OCORRENCIAS)
                pesos_o = []
                for t in tipos:
                    w = OCORRENCIAS[t][0]
                    if t == "Pane mecânica":
                        w = 0.02 + 0.010 * veic["idade"]
                    if t == "Clima adverso":
                        w *= FATOR_MES_CHUVA.get(dia.month, 1.0)
                    pesos_o.append(w)
                tipo_o = rng.choices(tipos, pesos_o)[0]
                dur_o = max(5, int(rng.lognormvariate(math.log(OCORRENCIAS[tipo_o][1]), 0.5)))
                custo_o = 0.0
                if tipo_o == "Pane mecânica":
                    atraso_mec += dur_o
                    custo_o = rng.lognormvariate(math.log(650), 0.5)
                else:
                    atraso += dur_o * 0.5
                    if tipo_o == "Fiscalização" and rng.random() < 0.15:
                        custo_o = 195.23
                alvo = ordem[0]
                t = rng.uniform(0.1, 0.9)
                lat = hub["lat"] + (alvo["lat"] - hub["lat"]) * t + rng.gauss(0, 0.02)
                lon = hub["lon"] + (alvo["lon"] - hub["lon"]) * t + rng.gauss(0, 0.02)
                pendentes.append((tipo_o, rng.choice(RODOVIAS[hub["id"]]), dur_o, custo_o, lat, lon,
                                  rng.uniform(0.05, 0.95)))

            atraso = round(atraso, 1)
            dur_real = max(dur_plan * 0.9,
                           dur_plan + (atraso + atraso_mec) / 60 + rng.gauss(0, 0.1))
            chegada = saida + timedelta(hours=dur_real)

            for tipo_o, rodovia, dur_o, custo_o, lat, lon, frac in pendentes:
                seq_o += 1
                momento = saida + timedelta(hours=dur_real * frac)
                ocorrencias.append((
                    f"O{seq_o:06d}", vid, fmt_dt(momento), tipo_o, rodovia, dur_o,
                    "Baixa" if dur_o < 30 else ("Média" if dur_o < 75 else "Alta"),
                    round(custo_o, 2), round(lat, 5), round(lon, 5)))

            km_real = km_plan * (1 + max(0, rng.gauss(0.035, 0.03)))

            kml = (kml_base * (1 - 0.007 * veic["idade"]) * (1 + (mot["skill"] - 0.5) * 0.12)
                   * (1 - 0.22 * uso) * (1 - min(0.12, atraso / 60 * 0.04)))
            litros = km_real / kml
            custo_comb = litros * preco_diesel
            custo_ped = km_real * pedagio_km * rng.uniform(0.35, 0.70)
            custo_man = km_real * (0.10 + 0.028 * veic["idade"]) * f_manut
            custo_mot = dur_real * (22 + 0.5 * mot["exp"])

            custo_plan = (km_plan * (preco_diesel / kml_base + pedagio_km * 0.5
                                     + (0.10 + 0.028 * veic["idade"]) * f_manut)
                          + dur_plan * (22 + 0.5 * mot["exp"]))
            frete_total = custo_plan * rng.uniform(1.22, 1.42)

            viagens.append((
                vid, fmt_dt(saida), fmt_dt(chegada), veic["id"], mot["id"], hub["id"], len(ordem),
                cap, round(carga, 1), round(km_plan, 1), round(km_real, 1), round(dur_plan, 2),
                round(dur_real, 2), atraso, round(litros, 1), round(custo_comb, 2),
                round(custo_ped, 2), round(custo_man, 2), round(custo_mot, 2)))

            atraso_total = atraso + atraso_mec
            acumulado = t_carga
            for i, (cli, peso) in enumerate(zip(ordem, pesos), start=1):
                acumulado += dir_h[i - 1] + (servico if i > 1 else 0)
                previsto = saida + timedelta(hours=acumulado)
                atraso_i = (atraso_total * 0.75 * (i / (len(ordem) + 0.5)) * rng.uniform(0.8, 1.2)
                            + rng.gauss(0, 6))
                tentativas, motivo = 1, ""
                r = rng.random()
                if r < 0.022:
                    tentativas = 2 if rng.random() < 0.75 else 3
                    motivo = rng.choice(["Cliente ausente", "Endereço incorreto"])
                    atraso_i += 240 * (tentativas - 1)
                elif r < 0.04:
                    motivo = "Doca ocupada"
                    atraso_i += rng.uniform(60, 120)
                completa = 1 if rng.random() < 0.975 - (0.5 - mot["skill"]) * 0.02 else 0
                avaria = 1 if rng.random() < clamp(
                    0.005 * (1 + (0.5 - mot["skill"]) * 2) + 0.0004 * veic["idade"], 0.001, 0.03) else 0
                no_prazo = 1 if atraso_i <= 30 else 0
                if avaria:
                    motivo = "Avaria na carga"
                elif not completa:
                    motivo = rng.choice(["Falta de estoque", "Recusa parcial", "Divergência de pedido"])
                elif not no_prazo and not motivo:
                    motivo = "Trânsito/Ocorrência na via" if atraso > 20 else "Atraso operacional"
                real = previsto + timedelta(minutes=atraso_i)
                seq_e += 1
                frete = max(80.0, frete_total * peso / carga)
                entregas.append((
                    f"E{seq_e:07d}", vid, cli["id"], i, fmt_dt(previsto), fmt_dt(real),
                    round(atraso_i, 1), round(peso, 1), max(1, int(round(peso / rng.uniform(18, 35)))),
                    round(frete, 2), no_prazo, completa, avaria, tentativas, motivo))
        dia += timedelta(days=1)

    d = args.saida
    escrever(os.path.join(d, "dim_hub.csv"),
             ["hub_id", "hub_nome", "cidade", "uf", "latitude", "longitude", "docas"],
             [(h["id"], h["nome"], h["cidade"], h["uf"], h["lat"], h["lon"], h["docas"]) for h in hubs])
    escrever(os.path.join(d, "dim_cliente.csv"),
             ["cliente_id", "cliente_nome", "cidade", "uf", "segmento", "prioridade", "latitude", "longitude"],
             [(c["id"], c["nome"], c["cidade"], c["uf"], c["segmento"], c["prioridade"], c["lat"], c["lon"])
              for c in clientes])
    escrever(os.path.join(d, "dim_veiculo.csv"),
             ["veiculo_id", "placa", "tipo", "marca", "ano_fabricacao", "capacidade_kg", "consumo_nominal_kml"],
             [(v["id"], v["placa"], v["tipo"], v["marca"], v["ano"], v["cap"], v["kml"]) for v in veiculos])
    escrever(os.path.join(d, "dim_motorista.csv"),
             ["motorista_id", "motorista_nome", "categoria_cnh", "anos_experiencia", "turno"],
             [(m["id"], m["nome"], m["cnh"], m["exp"], m["turno"]) for m in motoristas])
    escrever(os.path.join(d, "fato_viagens.csv"),
             ["viagem_id", "data_saida", "data_chegada", "veiculo_id", "motorista_id", "hub_id",
              "qtd_entregas", "capacidade_kg", "carga_kg", "km_planejado", "km_real",
              "duracao_planejada_h", "duracao_real_h", "atraso_transito_min", "litros_combustivel",
              "custo_combustivel", "custo_pedagio", "custo_manutencao", "custo_motorista"], viagens)
    escrever(os.path.join(d, "fato_entregas.csv"),
             ["entrega_id", "viagem_id", "cliente_id", "seq_parada", "data_hora_prevista",
              "data_hora_entrega", "atraso_min", "peso_kg", "volumes", "valor_frete", "no_prazo",
              "completa", "avaria", "tentativas", "motivo_falha"], entregas)
    escrever(os.path.join(d, "fato_ocorrencias.csv"),
             ["ocorrencia_id", "viagem_id", "data_hora", "tipo", "rodovia", "duracao_min",
              "gravidade", "custo_adicional", "latitude", "longitude"], ocorrencias)
    return viagens, entregas, ocorrencias


def resumo(viagens, entregas, ocorrencias):
    nv, ne = len(viagens), len(entregas)
    km = sum(v[10] for v in viagens)
    custo = sum(v[15] + v[16] + v[17] + v[18] for v in viagens) + sum(o[7] for o in ocorrencias)
    litros = sum(v[14] for v in viagens)
    receita = sum(e[9] for e in entregas)
    otd = sum(e[10] for e in entregas) / ne
    otif = sum(1 for e in entregas if e[10] and e[11]) / ne
    print(f"viagens={nv:,} entregas={ne:,} ocorrencias={len(ocorrencias):,}")
    print(f"%no_prazo={otd:.1%} OTIF={otif:.1%} avaria={sum(e[12] for e in entregas) / ne:.2%} "
          f"completa={sum(e[11] for e in entregas) / ne:.1%}")
    print(f"custo/km={custo / km:.2f} custo/entrega={custo / ne:.2f} km/L={km / litros:.2f} "
          f"margem={(receita - custo) / receita:.1%}")
    print(f"utilizacao={sum(v[8] for v in viagens) / sum(v[7] for v in viagens):.1%} "
          f"atraso_transito_medio={sum(v[13] for v in viagens) / nv:.1f}min "
          f"ocorr/100viagens={100 * len(ocorrencias) / nv:.1f}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--saida", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--inicio", default="2025-01-01")
    p.add_argument("--fim", default="2026-10-31")
    p.add_argument("--viagens-por-dia", type=float, default=28)
    p.add_argument("--clientes", type=int, default=120)
    p.add_argument("--veiculos", type=int, default=40)
    p.add_argument("--motoristas", type=int, default=55)
    args = p.parse_args()
    v, e, o = gerar(args)
    resumo(v, e, o)
    print(f"Arquivos gravados em {os.path.abspath(args.saida)}")


if __name__ == "__main__":
    main()
