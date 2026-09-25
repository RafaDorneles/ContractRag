import ollama

MODELO = "qwen2.5:7b"

mensagens = [
    {"role": "system", "content": "Você é um assistente que responde em português, de forma breve."},
    {"role": "user", "content": "O que é período de experiência num contrato de trabalho?"},
]

resposta = ollama.chat(
    model=MODELO,
    messages=mensagens,
    options={"temperature": 0.7},
)

print(resposta["message"]["content"])