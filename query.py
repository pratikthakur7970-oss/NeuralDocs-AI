from config import *

from embeddings.sentence_transformer import SentenceEmbedding
from vectorstores.pinecone_store import PineconeStore
from retrievers.retriever import Retriever
from llms.groq_llama import GroqLLM
from pipeline import RAGPipeline

embedding = SentenceEmbedding(
    EMBEDDING_MODEL
).get_model()

vectorstore = PineconeStore(
    PINECONE_INDEX,
    embedding
).connect()

retriever = Retriever(vectorstore)

llm = GroqLLM()

rag = RAGPipeline(retriever, llm)

while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break

    answer = rag.ask(question)

    print("\nAnswer:\n")
    print(answer.content)