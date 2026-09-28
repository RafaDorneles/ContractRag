import sys
import os
import chromadb

sys.stdout.reconfigure(encoding="utf-8")
from reading import read_file
from chunking import split_into_clauses
from embeddings import generate_embedding

DB_FOLDER = "vector_db"
CONTRACTS_FOLDER = "contratos"


def open_collection():
    client = chromadb.PersistentClient(path=DB_FOLDER)
    return client.get_or_create_collection(
        name="contracts",
        metadata={"hnsw:space": "cosine"},
    )


def search(question, count=3):
    collection = open_collection()
    result = collection.query(
        query_embeddings=[generate_embedding(question)],
        n_results=count,
    )

    passages = []
    for text, metadata in zip(result["documents"][0], result["metadatas"][0]):
        passages.append({
            "file": metadata["file"],
            "clause": metadata["clause"],
            "text": text,
        })
    return passages


def index_contracts(folder):
    collection = open_collection()
    for name in os.listdir(folder):
        if not name.lower().endswith((".pdf", ".txt")):
            continue

        text = read_file(os.path.join(folder, name))
        clauses = split_into_clauses(text)

        # delete the old version of this contract to avoid duplicates
        collection.delete(where={"file": name})

        collection.add(
            ids=[f"{name}::{i}" for i in range(len(clauses))],
            documents=[c["text"] for c in clauses],
            embeddings=[generate_embedding(c["text"]) for c in clauses],
            metadatas=[{"file": name, "clause": c["clause"]} for c in clauses],
        )
        print(f"✓ {name}: {len(clauses)} clauses")

    print(f"\nTotal in database: {collection.count()} clauses")


if __name__ == "__main__":
    index_contracts(CONTRACTS_FOLDER)
