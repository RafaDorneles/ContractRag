import ollama
from database import search
import time
from observabilidade import registrar

VERSAO_PROMPT = "v1"

CHAT_MODEL = "qwen2.5:7b"

INSTRUCTIONS = """You are an HR contracts assistant.
Answer in English, ONLY based on the contract passages provided.
Always cite the clause the information came from (e.g. "Clause 5").
If the information is not in the passages, say you could not find it. Do not make anything up."""


def build_context(passages):
    parts = []
    for p in passages:
        parts.append(f"[{p['file']} | {p['clause']}]\n{p['text']}")
    return "\n\n".join(parts)


def responder(pergunta):
    # R: busca, medindo o tempo
    inicio = time.perf_counter()
    trechos = search(pergunta, count=3)
    tempo_busca = time.perf_counter() - inicio

    contexto = build_context(trechos)
    mensagem = f"Trechos dos contratos:\n\n{contexto}\n\nPergunta: {pergunta}"

    # G: geração, medindo o tempo
    inicio = time.perf_counter()
    resposta = ollama.chat(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": mensagem},
        ],
        options={"temperature": 0}, 
    )
    tempo_geracao = time.perf_counter() - inicio
    texto = resposta["message"]["content"]

    registrar({
        "pergunta": pergunta,
        "modelo": CHAT_MODEL,
        "versao_prompt": VERSAO_PROMPT,
        "trechos": [
            {"arquivo": t["file"], "clausula": t["clause"], "nota": round(t.get("score", 0), 3)}
            for t in trechos
        ],
        "resposta": texto,
        "tempo_busca_s": round(tempo_busca, 2),
        "tempo_geracao_s": round(tempo_geracao, 2),
        "tokens_entrada": resposta["prompt_eval_count"],
        "tokens_saida": resposta["eval_count"],
    })

    return texto, trechos


if __name__ == "__main__":
    print("Make sure you have already run 'python database.py' to index the contracts.\n")

    while True:
        question = input("Question (or 'quit'): ")
        if question == "quit":
            break
        text, passages = responder(question)
        print(f"\n{text}")
        print("\nConsulted: " + ", ".join(f"{p['file']} ({p['clause']})" for p in passages))
        print()
