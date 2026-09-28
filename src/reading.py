from pypdf import PdfReader


def read_pdf(path):
    reader = PdfReader(path)
    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages)


def read_file(path):
    if path.lower().endswith(".pdf"):
        return read_pdf(path)
    with open(path, encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    text = read_pdf("contratos/exemplo.pdf")
    print(f"{len(text)} characters read\n")
    print(text[:1000])
