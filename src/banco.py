import os
import chromadb
from leitura import read_file
from chunking import dividir_em_clausulas as split_clauses
from embeddings import gerar_embedding

PASTA_BANCO = "banco_vetorial"
PASTA_CONTRATOS = "contratos"


def abrir_colecao():
    cliente = chromadb.PersistentClient(path=PASTA_BANCO)
    return cliente.get_or_create_collection(
        name="contratos",
        metadata={"hnsw:space": "cosine"},
    )


def buscar(pergunta, quantidade=3):
    colecao = abrir_colecao()
    resultado = colecao.query(
        query_embeddings=[gerar_embedding(pergunta)],
        n_results=quantidade,
    )

    trechos = []
    for texto, metadado in zip(resultado["documents"][0], resultado["metadatas"][0]):
        trechos.append({
            "arquivo": metadado["arquivo"],
            "clausula": metadado["clausula"],
            "texto": texto,
        })
    return trechos


def indexar(pasta):
    colecao = abrir_colecao()
    for nome in os.listdir(pasta):
        if not nome.lower().endswith((".pdf", ".txt")):
            continue

        texto = read_file(os.path.join(pasta, nome))
        clausulas = split_clauses(texto)

        # apaga a versão antiga desse contrato, para não duplicar
        colecao.delete(where={"arquivo": nome})

        colecao.add(
            ids=[f"{nome}::{i}" for i in range(len(clausulas))],
            documents=[c["texto"] for c in clausulas],
            embeddings=[gerar_embedding(c["texto"]) for c in clausulas],
            metadatas=[{"arquivo": nome, "clausula": c["clausula"]} for c in clausulas],
        )
        print(f"✓ {nome}: {len(clausulas)} cláusulas")

    print(f"\nTotal no banco: {colecao.count()} cláusulas")


if __name__ == "__main__":
    indexar(PASTA_CONTRATOS)