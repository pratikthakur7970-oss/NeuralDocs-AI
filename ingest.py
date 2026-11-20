from pathlib import Path

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    PINECONE_API_KEY,
    PINECONE_INDEX,
)
from embeddings.sentence_transformer import SentenceEmbedding
from loaders.pdf_loader import PDFLoader
from splitters.text_splitter import TextSplitter
from vectorstores.pinecone_store import PineconeStore


def main():
    data_directory = Path(__file__).resolve().parent / "data"
    pdf_files = sorted(data_directory.glob("*.pdf"))
    if not pdf_files:
        raise SystemExit(
            f"No PDF files found in {data_directory}. Add PDFs to that folder, "
            "then run this command again."
        )

    missing_settings = [
        name
        for name, value in (
            ("PINECONE_API_KEY", PINECONE_API_KEY),
            ("PINECONE_INDEX", PINECONE_INDEX),
        )
        if not value
    ]
    if missing_settings:
        raise SystemExit(
            "Set these values in your .env file before indexing: "
            + ", ".join(missing_settings)
        )

    loader = PDFLoader()
    documents = []
    for pdf_file in pdf_files:
        documents.extend(loader.load(str(pdf_file)))

    chunks = TextSplitter(CHUNK_SIZE, CHUNK_OVERLAP).split(documents)
    if not chunks:
        raise SystemExit("The PDF files contained no extractable text to index.")

    embedding = SentenceEmbedding(EMBEDDING_MODEL).get_model()
    PineconeStore(PINECONE_INDEX, embedding).create_store(chunks)
    print(f"Indexed {len(chunks)} text chunks from {len(pdf_files)} PDF file(s).")


if __name__ == "__main__":
    main()