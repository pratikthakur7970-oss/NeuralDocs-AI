| Module                    | Responsibility                         |
| ------------------------- | -------------------------------------- |
|  pdf_loader.py            | Load PDFs into `Document` objects      |
|  text_splitter.py         | Split documents into chunks            |
|  sentence_transformer.py  | Generate embeddings                    |
|  pinecone_store.py        | Create and query the vector index      |
|  retriever.py             | Retrieve relevant chunks               |
|  groq_llama.py            | Interface with the Groq Llama model    |
|  rag_prompt.py            | Prompt template                        |
|  pipeline.py              | Orchestrate the end-to-end RAG flow    |
|  ingest.py                | Read documents and populate Pinecone   |
|  query.py                 | Ask questions against the indexed data |

For a production RAG system on Groq

Model: llama-3.3-70b-versatile (excellent quality for RAG)
Embeddings: sentence-transformers/all-MiniLM-L6-v2 (fast and lightweight) or BAAI/bge-base-en-v1.5 (better retrieval quality for English)
Vector Database: Pinecone
Chunk Size: 500
Chunk Overlap: 50
Top-K: 5