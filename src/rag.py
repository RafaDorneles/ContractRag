import ollama
import time
from dotenv import load_dotenv
load_dotenv()

from langfuse import get_client

langfuse = get_client()

from database import search
from observability import log_event


PROMPT_VERSION = "v1"

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
    with langfuse.start_as_current_observation(
        as_type="span",
        name="contracts-rag",
        input={"question": question},
    ) as rag:
        rag.update(metadata={"model": CHAT_MODEL, "prompt_version": PROMPT_VERSION})

        # R: retrieval
        with langfuse.start_as_current_observation(
            as_type="span",
            name="retrieval",
            input={"question": question},
        ) as retrieval_span:
            start = time.perf_counter()
            passages = search(question, count=3)
            retrieval_time = time.perf_counter() - start
            retrieval_span.update(output=[
                {
                    "file": p["file"],
                    "clause": p["clause"],
                    "score": round(p.get("score", 0), 3),
                    "text": p["text"],
                }
                for p in passages
            ])

        # A: build the prompt
        context = build_context(passages)
        messages = [
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": f"Contract passages:\n\n{context}\n\nQuestion: {question}"},
        ]

        # G: generation
        with langfuse.start_as_current_observation(
            as_type="generation",
            name="generation",
            model=CHAT_MODEL,
            input=messages,
        ) as generation:
            start = time.perf_counter()
            response = ollama.chat(model=CHAT_MODEL, messages=messages, options={"temperature": 0})
            generation_time = time.perf_counter() - start
            text = response["message"]["content"]
            generation.update(
                output=text,
                usage_details={
                    "input_tokens": response["prompt_eval_count"],
                    "output_tokens": response["eval_count"],
                },
            )

        rag.update(output={"answer": text})

    # hand-made log, kept to compare with Langfuse
    log_event({
        "question": question,
        "model": CHAT_MODEL,
        "prompt_version": PROMPT_VERSION,
        "passages": [
            {"file": p["file"], "clause": p["clause"], "score": round(p.get("score", 0), 3)}
            for p in passages
        ],
        "answer": text,
        "retrieval_time_s": round(retrieval_time, 2),
        "generation_time_s": round(generation_time, 2),
        "input_tokens": response["prompt_eval_count"],
        "output_tokens": response["eval_count"],
    })

    return text, passages


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

        langfuse.flush()
