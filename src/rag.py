import ollama
from database import search

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


def answer(question):
    passages = search(question, count=3)

    context = build_context(passages)
    message = f"Contract passages:\n\n{context}\n\nQuestion: {question}"

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": message},
        ],
        options={"temperature": 0},
    )
    return response["message"]["content"], passages


if __name__ == "__main__":
    print("Make sure you have already run 'python database.py' to index the contracts.\n")

    while True:
        question = input("Question (or 'quit'): ")
        if question == "quit":
            break
        text, passages = answer(question)
        print(f"\n{text}")
        print("\nConsulted: " + ", ".join(f"{p['file']} ({p['clause']})" for p in passages))
        print()
