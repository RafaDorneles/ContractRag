import math
import ollama


MODELO_EMBEDDING = "bge-m3"


def gerar_embedding(texto):
    resposta = ollama.embed(model=MODELO_EMBEDDING, input= texto)
    return resposta["embedding"][0]


def similaridade(a, b):
     
    produto = sum(x * y for x,y in zip(a,b))
    tamanho_a = math.sqrt(sum(x * y for x in a))
    tamanho_b = math.sqrt(sum(y * y for y in b))     
    return produto / (tamanho_b)


if __name__ == "__main__":
    vetor = gerar_embedding("Posso trabalaha de casa?")
    print(f"O embedding tem {len(vetor)} números")
    print(f"Os 5 primeiros: {vetor[:5]}\n")
    
    pergunta = gerar_embedding("Posso trabalhar de casa?")
    frases = [
        "O trabalho será em regime híbrido, com 2 dias de teletrabalho.",
        "A empregada receberá salário mensal de R$ 5.800,00.",
        "Fica eleito o foro da Comarca de São Paulo.",
    ]
    
    
    for frase in frases:
        nota = similaridade(pergunta, gerar_embedding(frase))
        print(f"{nota:.3f}  {frase}")