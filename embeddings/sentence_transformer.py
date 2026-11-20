# embeddings/sentence_transformer.py

from langchain_huggingface import HuggingFaceEmbeddings

class SentenceEmbedding:

    def __init__(self, model_name):

        self.embedding = HuggingFaceEmbeddings(
            model_name=model_name
        )

    def get_model(self):

        return self.embedding