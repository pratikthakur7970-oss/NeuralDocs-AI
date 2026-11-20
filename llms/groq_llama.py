from config import GROQ_API_KEY, GROQ_MODEL
from langchain_groq import ChatGroq


class GroqLLM:

  def __init__(self):
    self.llm = ChatGroq(
        api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0
    )

  def invoke(self, prompt):
    return self.llm.invoke(prompt)


# Add this function so app.py can import it successfully
def get_groq_llm():
  return GroqLLM()