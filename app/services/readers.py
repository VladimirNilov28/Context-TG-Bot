"""Читалки файлов для ingest."""
from pathlib import Path
from typing import Optional

def read_txt(path: Path, encoding: Optional[str] = None) -> str:
    encodings = [encoding, "utf-8", "utf-16", "cp1251", "latin-1"]
    data = None
    for enc in [e for e in encodings if e]:
        try:
            data = path.read_text(encoding=enc, errors="ignore")
            break
        except Exception:
            continue
    if data is None:
        data = path.read_bytes().decode("utf-8", errors="ignore")
    return data

def read_pdf(path: Path) -> str:
    # pdfplumber уже в requirements
    import pdfplumber
    parts: list[str] = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            if txt.strip():
                parts.append(txt)
    return "\n\n".join(parts)
