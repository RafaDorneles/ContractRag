import re
from reading import read_pdf

# Matches the Portuguese clause headings ("CLÁUSULA 5") used in the contracts
PATTERN = re.compile(r"^\s*CL[ÁA]USULA\s+(\d+)", re.IGNORECASE | re.MULTILINE)


def split_into_clauses(text):
    marks = list(PATTERN.finditer(text))
    pieces = []

    if marks and marks[0].start() > 0:
        pieces.append({"clause": "Preamble", "text": text[:marks[0].start()].strip()})

    for i, mark in enumerate(marks):
        start = mark.start()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        number = mark.group(1)
        pieces.append({"clause": f"Clause {number}", "text": text[start:end].strip()})

    return pieces


if __name__ == "__main__":
    text = read_pdf("contratos/exemplo.pdf")
    for p in split_into_clauses(text):
        print(f"--- {p['clause']} ({len(p['text'])} characters)")
        print(p["text"][:80], "...\n")
