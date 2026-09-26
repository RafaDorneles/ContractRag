import os
from leitura import read_file
from chunking import dividir_em_clausulas
from embeddings import gerar_embedding, similaridade


def criar_indice(pasta):
    indice = []
    for nome in os.listdir(pasta):
        if not nome.lower().endswith((".pdf", ".txt")):
            continue
        texto = read_file(os.path.join(pasta, nome))
        for c in dividir_em_clausulas(texto):
            print(f"Gerando embedding: {nome} | {c['clausula']}")
            indice.append({
                "arquivo": nome,
                "clausula": c["clausula"],
                "texto": c["texto"],
                "embedding": gerar_embedding(c["texto"]),
            })
    return indice


def buscar(pergunta, indice, quantidade=3):
    vetor_pergunta = gerar_embedding(pergunta)
    resultados = []
    for item in indice:
        nota = similaridade(vetor_pergunta, item["embedding"])
        resultados.append({**item, "nota": nota})
    resultados.sort(key=lambda r: r["nota"], reverse=True)
    return resultados[:quantidade]


if __name__ == "__main__":
    indice = criar_indice("contratos/exemplo.pdf")
    print(f"\nÍndice pronto com {len(indice)} cláusulas.\n")

    while True:
        pergunta = input("Pergunta (ou 'sair'): ")
        if pergunta == "sair":
            break
        for r in buscar(pergunta, indice):
            print(f"  {r['nota']:.3f}  {r['arquivo']} | {r['clausula']}")
        print()