# DocuMind

### Grounded document intelligence with RAG, vector search, and reranking

DocuMind is a document question-answering application that allows users to upload documents, organize them, and ask questions about their contents.

Instead of treating a document as one large prompt, DocuMind builds a retrieval pipeline that finds relevant pieces of the user's documents before generating an answer.

The project was built as a practical exploration of **backend engineering, retrieval-augmented generation, vector search, embeddings, reranking, PostgreSQL, FastAPI, and production-oriented system design**.

---

## Demo

> 🎥 **Full application demo:**  
> Add your YouTube/Loom demo link here.

[![DocuMind Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

The demo shows:

- User authentication
- Document upload
- Document processing
- Document organization
- Conversational question answering
- Retrieval from uploaded documents
- Source citations
- Vector search
- Cross-encoder reranking
- Conversation history

---

# Why DocuMind?

Large language models are good at generating answers, but they do not automatically know the contents of a user's private documents.

A basic approach would be:

```text
Document
   ↓
Put entire document into prompt
   ↓
LLM
   ↓
Answers