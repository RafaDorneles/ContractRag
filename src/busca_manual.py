from leitura import read_pdf
from chunking import dividir_em_clausulas
from embeddings import gerar_embedding, similaridade


def criar_indice(caminho_pdf):
    texto = read_pdf(caminho_pdf)
    clausulas = dividir_em_clausulas(texto)

    indice = []
    for c in clausulas:
        print(f"Gerando embedding: {c['clausula']}")
        indice.append({
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
        resultados.append({"clausula": item["clausula"], "texto": item["texto"], "nota": nota})

    # ordena da maior nota para a menor e pega só as primeiras
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
            print(f"  {r['nota']:.3f}  {r['clausula']}")
        print()