import re
from leitura import read_pdf

PADRAO = re.compile(r"^\s*CL[ÁA]USULA\s+(\d+)", re.IGNORECASE | re.MULTILINE)


def dividir_em_clausulas(texto):
    marcas = list(PADRAO.finditer(texto))
    pedacos = []

    if marcas and marcas[0].start() > 0:
        pedacos.append({"clausula": "Preâmbulo", "texto": texto[:marcas[0].start()].strip()})

    for i, marca in enumerate(marcas):
        inicio = marca.start()
        fim = marcas[i + 1].start() if i + 1 < len(marcas) else len(texto)
        numero = marca.group(1)
        pedacos.append({"clausula": f"Cláusula {numero}ª", "texto": texto[inicio:fim].strip()})

    return pedacos


if __name__ == "__main__":
    texto = read_pdf("contratos/exemplo.pdf")
    for p in dividir_em_clausulas(texto):
        print(f"--- {p['clausula']} ({len(p['texto'])} caracteres)")
        print(p["texto"][:80], "...\n")