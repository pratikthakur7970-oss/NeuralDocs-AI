from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFLoader:

  def load_and_split_pdf(self, pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # Split the pages into smaller chunks for the vector store
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    chunks = text_splitter.split_documents(pages)
    return chunks


# Helper function so app.py can import it directly
def load_and_split_pdf(pdf_path):
  pdf_loader = PDFLoader()
  return pdf_loader.load_and_split_pdf(pdf_path)