import json
import os
from datetime import datetime

PASTA_LOGS = "logs"
ARQUIVO_LOG = os.path.join(PASTA_LOGS, "rag_log.jsonl")


def registrar(dados):
    os.makedirs(PASTA_LOGS, exist_ok=True)
    dados["data_hora"] = datetime.now().isoformat(timespec="seconds")
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(dados, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    registrar({"pergunta": "teste", "resposta": "funcionou"})
    print(f"Log gravado em {ARQUIVO_LOG}")