from langchain_core.messages import AIMessage

from prompts.rag_prompt import PROMPT


class RAGPipeline:

    def __init__(self, retriever, llm):

        self.retriever = retriever
        self.llm = llm

    def ask_with_sources(self, question):
        docs = self.retriever.retrieve(question)

        if not docs:
            return (
                AIMessage(
                    content=(
                        "I couldn't find relevant information in the indexed "
                        "documents. Add PDF files to the project's data folder "
                        "and run `python ingest.py` to index them, or try "
                        "rephrasing your question."
                    )
                ),
                docs,
            )

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        prompt = PROMPT.format(
            context=context,
            question=question
        )

        return self.llm.invoke(prompt), docs

    def ask(self, question):
        response, _ = self.ask_with_sources(question)
        return response