from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings  # Ya aapka jo bhi embedding model ho


class Retriever:

  def __init__(self, vectorstore):
    self.retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

  def retrieve(self, question):
    return self.retriever.invoke(question)


# 1. Vector store create karne ka main function jo chunks ko Chroma/FAISS mein store karega
def create_vector_store(chunks):
  # Yahan apna embedding model specify karein jo aapne project me use kiya hai
  embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

  # Vector store create karein
  vectorstore = Chroma.from_documents(chunks, embeddings)

  # Retriever object return karein (jisme .invoke() method available ho)
  return vectorstore.as_retriever(search_kwargs={"k": 5})