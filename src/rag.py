import ollama 
from busca_manual import criar_indice , buscar


MODELO_CHAT = "qwen2.5:7b"
PASTA_CONTRATOS = "contratos"

INSTRUCOES = """Você é um assistente de contratos de RH.
Responda em português, SOMENTE com base nos trechos de contrato fornecidos.
Sempre cite a cláusula de onde tirou a informação (ex.: "Cláusula 5ª").
Se a informação não estiver nos trechos, diga que não encontrou. Não invente."""

def montar_contexto(trechos):
    partes = []
    for t in trechos:
        partes.append(f"[{t['arquivo']} | {t['clausula']}]\n{t['texto']}")
    return "\n\n".join(partes)


def responder(pergunta, indice):
    trechos = buscar(pergunta, indice, quantidade=3)

    contexto = montar_contexto(trechos)
    mensagem = f"Trechos dos contratos:\n\n{contexto}\n\nPergunta: {pergunta}"

    resposta = ollama.chat(
        model=MODELO_CHAT,
        messages=[
            {"role": "system", "content": INSTRUCOES},
            {"role": "user", "content": mensagem},
        ],
        options={"temperature": 0},
    )
    return resposta["message"]["content"], trechos



if __name__ == "__main__":
    indice = criar_indice(PASTA_CONTRATOS)
    print(f"\nÍndice pronto com {len(indice)} cláusulas.\n")

    while True:
        pergunta = input("Pergunta (ou 'sair'): ")
        if pergunta == "sair":
            break
        texto, trechos = responder(pergunta, indice)
        print(f"\n{texto}")
        print("\nConsultado: " + ", ".join(f"{t['arquivo']} ({t['clausula']})" for t in trechos))
        print()
