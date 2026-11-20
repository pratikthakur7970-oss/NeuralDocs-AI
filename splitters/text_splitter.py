# splitters/text_splitter.py

from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextSplitter:

    def __init__(self, chunk_size, overlap):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap
        )

    def split(self, docs):

        return self.splitter.split_documents(docs)