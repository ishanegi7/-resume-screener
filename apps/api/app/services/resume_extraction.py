import io

import pdfplumber

async def extract_text_from_pdf(file_path: str) -> str:
    text_chunks: list[str] = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_chunks.append(page_text)

    return "\n\n".join(text_chunks).strip()
