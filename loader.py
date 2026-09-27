from pathlib import Path
from pypdf import PdfReader
from docx import Document

def extract_file(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if ext == ".docx":
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    return path.read_text(encoding="utf-8", errors="ignore")

def load_documents(folder: Path):
    docs = []
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".pdf", ".docx", ".txt", ".md"}:
            text = extract_file(p).strip()
            if text:
                docs.append({"source": p.name, "text": text})
    return docs

def chunk_text(text: str, chunk_size=900, overlap=120):
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks
