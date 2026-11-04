import time
from mercados import mercados

resultados = {}


def processar_lista(protocolo, itens):
    """
    Simula processamento demorado
    """

    resultados[protocolo] = {
        "status": "EM_PROCESSAMENTO"
    }

    time.sleep(10)

    melhor_mercado = None
    menor_total = float("inf")

    totais = {}

    for nome_mercado, produtos in mercados.items():

        total = 0

        for item in itens:
            total += produtos.get(item, 0)

        totais[nome_mercado] = total

        if total < menor_total:
            menor_total = total
            melhor_mercado = nome_mercado

    resultados[protocolo] = {
        "status": "CONCLUIDO",
        "melhor_mercado": melhor_mercado,
        "valor_total": round(menor_total, 2),
        "comparativo": totais
    }
    