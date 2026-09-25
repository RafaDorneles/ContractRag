import ollama

from leitura import read_pdf



MODELO = "qwen2.5:7b"
contrato = read_pdf("contratos/exemplo.pdf")

instrucoes = """Você é um assistente de contratos de RH.
Responda em português, SOMENTE com base no contrato fornecido.
Sempre cite a cláusula de onde tirou a informação (ex.: "Cláusula 5ª").
Se a informação não estiver no contrato, diga que não encontrou. Não invente."""


question = input("Sua pergunta: ")

resposta = ollama.chat(
    model=MODELO,
    messages=[
        {"role": "system", "content": instrucoes},
        {"role": "user", "content": f"Contrato:\n{contrato}\n\nPergunta: {question}"},
    ],
    options={"temperature": 0},
)
print("\n" + resposta["message"]["content"])