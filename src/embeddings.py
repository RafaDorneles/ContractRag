import math
import ollama


EMBEDDING_MODEL = "bge-m3"


def generate_embedding(text):
    response = ollama.embed(model=EMBEDDING_MODEL, input=text)
    return response["embeddings"][0]


def similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot_product / (length_a * length_b)
