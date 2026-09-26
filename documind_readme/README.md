🧠 DocuMind

Ask questions about your documents — and see where the answers come from.

DocuMind is a full-stack document question-answering application built around Retrieval-Augmented Generation (RAG).

Upload documents, build a searchable knowledge base, ask questions in natural language, and receive answers grounded in retrieved document content.

<p align="center">
  <a href="https://youtu.be/ZbwSCWUdKiQ">
    <img src="https://img.youtube.com/vi/ZbwSCWUdKiQ/maxresdefault.jpg" alt="Watch the DocuMind demo" width="850">
  </a>
</p>

<p align="center">
  <b>▶ Click the preview above to watch the full demo</b>
</p>

🚧 Deployment in progress

DocuMind is currently being prepared for public deployment.
The application is not publicly hosted yet, but the complete workflow is demonstrated in the video above.

Want to see it in action?
Watch the full demo on YouTube

📌 What is DocuMind?

DocuMind is designed to turn a collection of documents into a searchable, conversational knowledge base.

Instead of sending an entire document to an LLM for every question, DocuMind uses a retrieval pipeline to find relevant pieces of information first and then provides that context to the language model.

The core idea is:

Documents
    ↓
Parse
    ↓
Chunk
    ↓
Generate embeddings
    ↓
Store in PostgreSQL + pgvector
    ↓
User asks a question
    ↓
Vector retrieval
    ↓
Reranking
    ↓
Relevant context
    ↓
LLM
    ↓
Answer + retrieved sources

🎯 The Problem

Important information is often buried inside long documents.

Imagine an employee has a 100-page company policy document and wants to know:

"How many paid leave days does a full-time employee receive each year?"

Manually searching the document is slow.

Sending the entire document to an LLM for every question is also inefficient and makes it harder to control what information the model uses.

DocuMind takes a retrieval-first approach:

User Question
     ↓
Find relevant document content
     ↓
Rank the retrieved candidates
     ↓
Give relevant context to the LLM
     ↓
Generate a grounded answer

This allows the application to work with a persistent document library rather than treating every question as an isolated prompt.

✨ Features

📚 Personal document library

Users can maintain a persistent library of documents that DocuMind can search and answer questions about.

💬 Natural-language document Q&A

Ask questions about your documents using a conversational interface rather than manually searching through files.

🎯 Scoped document retrieval

Users can query:

All documents in their library

A specific selected document

This allows retrieval to be constrained to the documents relevant to a conversation.

🔎 Document search

The library provides a search interface for finding documents within the knowledge base.

🧠 Retrieval-Augmented Generation

DocuMind retrieves relevant document chunks before sending context to the language model.

🔄 Reranking

Retrieved candidates can be passed through a reranking stage before the final context is constructed for generation.

📑 Retrieved source visibility

The chat interface exposes the sources used during retrieval, including the document, chunk identifier, and retrieval distance.

💾 Conversation history

Users can maintain multiple conversations and return to previous chats.

✏️ Conversation management

Conversations can be renamed or deleted from the chat interface.

🔐 Authentication

DocuMind provides account creation and sign-in so document libraries can be associated with individual users.

📸 Product Preview

🔐 Authentication

<p align="center">
  <img src="assets/screenshots/01-sign-in.png" alt="DocuMind sign in" width="900">
</p>

DocuMind provides a dedicated authentication flow for accessing a user's document library.

📚 Document Library

<p align="center">
  <img src="assets/screenshots/04-library-ready.png" alt="DocuMind document library" width="900">
</p>

The library provides a central place to manage documents that are available to the retrieval system.

Documents expose their processing state, allowing the application to distinguish documents that are ready to be queried.

🎯 Select the documents you want to query

<p align="center">
  <img src="assets/screenshots/06-document-selection.png" alt="DocuMind document selection" width="700">
</p>

A conversation can search the entire library or be restricted to a specific document.

💬 Ask questions and inspect retrieved sources

<p align="center">
  <img src="assets/screenshots/07-rag-answer-sources.png" alt="DocuMind RAG answer with retrieved sources" width="900">
</p>

The answer interface exposes the retrieved sources alongside the generated response.

This makes the retrieval stage visible instead of hiding the entire RAG process behind the final LLM answer.

🗂️ Conversation history

<p align="center">
  <img src="assets/screenshots/05-chat-history.png" alt="DocuMind conversation history" width="900">
</p>

Users can maintain multiple conversations and manage them from the sidebar.

🏗️ Architecture

At a high level, DocuMind separates the application into a frontend, backend API, persistence layer, retrieval layer, and LLM generation layer.

┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                            │
│                     React + Vite                            │
│                                                             │
│  Authentication · Library · Chat · Document Selection       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                            HTTP API
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                         BACKEND                             │
│                         FastAPI                             │
│                                                             │
│  Auth · Documents · Conversations · Query Orchestration     │
└───────────────┬─────────────────────┬───────────────────────┘
                │                     │
                ▼                     ▼
      ┌─────────────────┐    ┌────────────────────────┐
      │   PostgreSQL    │    │    RAG / Retrieval     │
      │                 │    │                        │
      │ Users            │    │ Query Embedding       │
      │ Documents        │    │ Vector Search         │
      │ Chunks           │    │ Candidate Retrieval   │
      │ Conversations    │    │ Reranking             │
      └────────┬────────┘    └───────────┬────────────┘
               │                         │
               │                    ┌────▼─────┐
               │                    │ pgvector │
               │                    │           │
               │                    │ Embeddings
               │                    └────┬─────┘
               │                         │
               └─────────────────────────┤
                                         │
                                   Relevant Context
                                         │
                                         ▼
                                ┌─────────────────┐
                                │       LLM       │
                                │    Generation   │
                                └────────┬────────┘
                                         │
                                         ▼
                                Answer + Sources

🔍 RAG Pipeline

1. Document ingestion

When a document is added to the library, its content needs to become searchable.

Document
   ↓
Parse / Extract text
   ↓
Clean text
   ↓
Split into chunks
   ↓
Generate embeddings
   ↓
Store chunks + embeddings
   ↓
PostgreSQL + pgvector

The important design choice is that the application stores document chunks as retrievable units rather than treating an entire document as one large piece of context.

2. Query processing

When a user asks a question:

User Question
      ↓
Create query representation / embedding
      ↓
Vector similarity search
      ↓
Retrieve candidate chunks
      ↓
Rerank candidates
      ↓
Select relevant context
      ↓
Send context + question to LLM
      ↓
Generate answer
      ↓
Return answer + sources

The retrieval stage is intentionally separated from generation.

The LLM is not responsible for searching the entire document collection itself. The application first determines which pieces of the knowledge base are relevant.

🧠 Why RAG?

A basic document chatbot can place large amounts of document content directly into an LLM prompt.

That approach becomes increasingly expensive and difficult to manage as the document collection grows.

RAG introduces a retrieval stage:

                    Without retrieval

Document ───────────────► Large prompt ─────────► LLM


                    With retrieval

Documents
    │
    ▼
Vector index
    │
    ▼
Relevant chunks ───────► Focused context ───────► LLM

The model receives context selected for the current question instead of blindly receiving the entire document collection.

🔄 Why reranking?

Vector search is useful for efficiently finding candidate chunks that are semantically related to a query.

However, the initial retrieval stage can return multiple plausible candidates.

A reranking stage provides another filtering step:

Question
   │
   ▼
Vector Search
   │
   ├── Candidate 1
   ├── Candidate 2
   ├── Candidate 3
   ├── Candidate 4
   └── Candidate 5
          │
          ▼
    Cross-Encoder
       Reranker
          │
          ▼
   Best candidates
          │
          ▼
        LLM

This separates two different responsibilities:

Vector search: efficiently retrieve candidate information.

Reranking: more carefully evaluate the relationship between the query and retrieved candidates.

🛠️ Tech Stack

Layer

Technology

Frontend

React

Frontend tooling

Vite

Backend

Python

API framework

FastAPI

ORM

SQLAlchemy

Database

PostgreSQL

Vector search

pgvector

Retrieval

Embeddings + vector similarity search

Reranking

Cross-Encoder

LLM

Qwen via LM Studio

API style

REST

Note: The exact embedding, reranker, and Qwen model configurations are intentionally not hard-coded into this README yet. They can be added once the production configuration is finalized.

⚙️ Engineering Focus

DocuMind was built as a hands-on project for exploring production-oriented backend and AI engineering concepts.

Backend engineering

REST API design with FastAPI

Authentication and user-specific resources

PostgreSQL data modeling

SQLAlchemy ORM

Document and conversation persistence

API-level separation of application responsibilities

Frontend/backend integration

AI engineering

Document ingestion

Text chunking

Embeddings

Vector similarity search

Retrieval-Augmented Generation

Candidate retrieval

Cross-encoder reranking

LLM integration

Grounded answer generation

System design

The project explores an architecture where:

User-facing application
        ↓
Backend API
        ↓
Persistence + retrieval
        ↓
AI orchestration
        ↓
LLM generation

Each stage has a separate responsibility rather than putting the entire workflow inside a single LLM call.

🗃️ Data Flow

Document side

User
 │
 │ Upload
 ▼
FastAPI
 │
 ▼
Document processing
 │
 ├── Document metadata
 │
 └── Text chunks
          │
          ▼
      Embeddings
          │
          ▼
   PostgreSQL + pgvector

Question side

User
 │
 │ Question
 ▼
FastAPI
 │
 ▼
Query representation
 │
 ▼
Vector retrieval
 │
 ▼
Candidate chunks
 │
 ▼
Reranking
 │
 ▼
Relevant context
 │
 ▼
LLM
 │
 ▼
Answer + sources

📁 Project Structure

The repository is organized into separate frontend and backend applications.

DocuMind/
│
├── backend/
│   └── ...
│
├── frontend/
│   └── ...
│
└── README.md

The exact directory structure may evolve as the project continues to be developed.

🚀 Running Locally

DocuMind is currently being developed as a local full-stack application.

The application requires the frontend, backend, PostgreSQL/pgvector database, and local LLM environment to be configured.

High-level setup

1. Clone the repository
        ↓
2. Configure the backend environment
        ↓
3. Start PostgreSQL + pgvector
        ↓
4. Configure the local LLM
        ↓
5. Start the FastAPI backend
        ↓
6. Start the React/Vite frontend
        ↓
7. Open the application in your browser

Detailed environment variables and deployment instructions will be added as the project moves toward public deployment.

🎥 Demo

The application is currently being prepared for public deployment.

Until the hosted version is available, the complete workflow can be viewed in the demo:

<p align="center">
  <a href="https://youtu.be/ZbwSCWUdKiQ">
    <img src="https://img.youtube.com/vi/ZbwSCWUdKiQ/maxresdefault.jpg" alt="DocuMind Demo" width="850">
  </a>
</p>

▶ Watch the full DocuMind demo on YouTube

🗺️ Roadmap

The project is actively evolving.

Current

User authentication

Document library

Document upload

Document search interface

Conversational Q&A

Document-scoped querying

Conversation history

Vector-based retrieval

Reranking

Retrieved source visibility

Local LLM integration

Planned / evolving

Public deployment

Production infrastructure

More robust document ingestion

Improved observability and evaluation

Expanded document format support

Retrieval quality benchmarking

Additional production hardening

📌 Project Status

Active development

DocuMind is primarily a hands-on engineering project focused on understanding how a production-oriented document Q&A system can be designed and built from the ground up.

The project is being developed incrementally, with particular attention to:

Backend engineering
        +
AI / RAG engineering
        +
Database design
        +
System architecture
        +
User experience

🎯 What I wanted to learn from this project

DocuMind was built not only as a document chatbot, but as a way to understand the engineering decisions behind AI-powered applications.

The project brings together:

Backend APIs

Databases

Authentication

Document processing

Embeddings

Vector databases

Information retrieval

Reranking

LLMs

Frontend integration

System design

The goal is to understand how these components work together as a complete system rather than treating the LLM as a black box.

📄 License

License information will be added as the project is finalized.

<p align="center">
  <b>DocuMind</b>
  <br>
  Document Q&A powered by retrieval and generation.
</p>