from pypdf import PdfReader


def read_pdf(path): 
    reader = PdfReader(path)
    pages= []
    
    for page in reader.pages:
        
        text = page.extract_text() or ""
        pages.append(text)
        
    return "\n".join(pages)


def read_file(caminho):
    if caminho.lower().endswith(".pdf"):
        return read_pdf(caminho)
    with open(caminho, encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    texto = read_pdf("contratos/exemplo.pdf")
    print(f"{len(texto)} caracteres lidos\n")
    print(texto[:1000])