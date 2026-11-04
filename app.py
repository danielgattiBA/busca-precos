from fastapi import FastAPI
from fastapi import BackgroundTasks
from pydantic import BaseModel

from uuid import uuid4

from mercados import mercados
from processamento import processar_lista
from processamento import resultados

app = FastAPI(title="BuscaPreço")


# --------------------------------------------------
# MODELS
# --------------------------------------------------

class ListaCompras(BaseModel):
    itens: list[str]


# --------------------------------------------------
# SÍNCRONO
# --------------------------------------------------

@app.get("/precos")
def pesquisar_produto(produto: str):

    resposta = []

    for mercado, produtos in mercados.items():

        if produto in produtos:

            resposta.append({
                "mercado": mercado,
                "preco": produtos[produto]
            })

    return {
        "produto": produto,
        "precos": resposta
    }


# --------------------------------------------------
# ASSÍNCRONO
# --------------------------------------------------

@app.post("/listas")
def enviar_lista(
        lista: ListaCompras,
        background_tasks: BackgroundTasks):

    protocolo = str(uuid4())

    resultados[protocolo] = {
        "status": "EM_PROCESSAMENTO"
    }

    background_tasks.add_task(
        processar_lista,
        protocolo,
        lista.itens
    )

    return {
        "protocolo": protocolo,
        "status": "EM_PROCESSAMENTO"
    }


# --------------------------------------------------
# CONSULTA STATUS
# --------------------------------------------------

@app.get("/listas/{protocolo}")
def consultar_lista(protocolo: str):

    if protocolo not in resultados:
        return {
            "erro": "Protocolo não encontrado"
        }

    return resultados[protocolo]
