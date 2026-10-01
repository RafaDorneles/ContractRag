import json
from collections import Counter
from observabilidade import ARQUIVO_LOG


def ler_log():
    registros = []
    with open(ARQUIVO_LOG, encoding="utf-8") as f:
        for linha in f:
            if linha.strip():
                registros.append(json.loads(linha))
    return registros


def media(valores):
    return sum(valores) / len(valores) if valores else 0


if __name__ == "__main__":
    registros = [r for r in ler_log() if "tempo_busca_s" in r]
    print(f"Perguntas registradas: {len(registros)}\n")

    print("  Tempo médio")
    print(f"   Busca:   {media([r['tempo_busca_s'] for r in registros]):.2f} s")
    print(f"   Geração: {media([r['tempo_geracao_s'] for r in registros]):.2f} s\n")

    print(" Tokens")
    print(f"   Média de entrada: {media([r['tokens_entrada'] for r in registros]):.0f}")
    print(f"   Média de saída:   {media([r['tokens_saida'] for r in registros]):.0f}")
    print(f"   Total:            {sum(r['tokens_entrada'] + r['tokens_saida'] for r in registros)}\n")

    print(" Perguntas por modelo e versão do prompt")
    combos = Counter(f"{r['modelo']} | prompt {r['versao_prompt']}" for r in registros)
    for combo, qtd in combos.most_common():
        print(f"   {qtd:3}  {combo}")

    print("\n Cláusulas mais recuperadas pela busca")
    clausulas = Counter(
        f"{t['arquivo']} ({t['clausula']})"
        for r in registros
        for t in r["trechos"]
    )
    for clausula, qtd in clausulas.most_common(5):
        print(f"   {qtd:3}  {clausula}")

    print("\n Buscas com nota baixa (melhor trecho abaixo de 0.5)")
    for r in registros:
        melhor = max(t["nota"] for t in r["trechos"])
        if melhor < 0.5:
            print(f"   {melhor:.2f}  {r['pergunta']}")