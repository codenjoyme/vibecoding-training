# RAG: Document Question Answering

**Duration:** 5-7 minutes

**Skill:** Build Retrieval-Augmented Generation (RAG) systems that search your documents, find relevant context, and generate accurate answers using AI

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Understanding RAG architecture: retrieval + generation
- Vector embeddings for semantic document search
- Creating and querying vector stores with FAISS
- Filtering search results by relevance threshold
- Combining retrieved context with AI generation
- Preventing hallucinations by grounding responses in documents

## Learning Outcome

You'll build a working RAG system that converts documents to vector embeddings, searches for semantically similar content, filters by relevance, and generates AI responses grounded in your documents. This technique prevents AI hallucinations by ensuring responses come from actual source material, not model imagination.

## Prerequisites

- **180-dial-langchain-python-integration** - Python environment with Langchain installed
- **185-prompt-templates-dynamic-queries** - Understanding prompt templates
- Python virtual environment activated in `work/python-ai-workspace`
- DIAL API credentials configured in `.env` file with embedding model
- Basic understanding of semantic similarity concepts

## When to Use

- Building Q&A systems over company documentation
- Creating chatbots that answer from specific knowledge base
- Developing document search with AI-generated summaries
- Implementing support systems that cite source material
- Any application requiring factual answers grounded in documents
- Reducing hallucinations by constraining AI to known information

## Resources

- [Langchain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [FAISS Vector Store Documentation](https://python.langchain.com/docs/integrations/vectorstores/faiss/)
- [Understanding Embeddings](https://platform.openai.com/docs/guides/embeddings)
- Module workspace: `work/python-ai-workspace`
