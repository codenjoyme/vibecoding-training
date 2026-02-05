from color import header
header("RAG example", "yellow")

import sys
import os
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI setup
llm = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_API_DEPLOYMENT"),
    api_version      = os.getenv("AZURE_OPENAI_API_VERSION"),
    api_key          = os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint   = os.getenv("AZURE_OPENAI_ENDPOINT"),
    max_tokens       = 1000,
    temperature      = 0,
    verbose          = False,
    seed             = 1234
)

embeddings = AzureOpenAIEmbeddings(
    model=os.getenv("AZURE_OPENAI_API_EMBEDDING_DEPLOYMENT"),
    deployment=os.getenv("AZURE_OPENAI_API_EMBEDDING_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Simple documents for search
docs = [
    "A cat is a domestic animal of the feline family. Cats love to sleep and play.",
    "A dog is a human's best friend. Dogs guard the house and love to walk.",
    "Python is a programming language. It's easy to write code in Python."
]

# Create documents
documents = [Document(page_content=doc) for doc in docs]

# Create vector store
vector_store = FAISS.from_documents(documents, embeddings)

# Simple RAG function
def ask_question(question):
    header("Question")
    print(question)
    
    header("Searching for relevant documents")

    # Search for similar documents with scores
    results_with_scores = vector_store.similarity_search_with_score(question, k=3)
    
    # Filter by relevance threshold (lower score = more similar)
    relevance_threshold = 0.5  # Adjust this value as needed
    relevant_docs = []
    
    for doc, score in results_with_scores:
        if score < relevance_threshold:  # Lower score means more similar
            relevant_docs.append(doc)
            print(f"📄 Document found (similarity: {1-score:.2f}): {doc.page_content[:50]}...")
        else:
            print(f"❌ Document filtered out (similarity: {1-score:.2f}): {doc.page_content[:50]}...")
    
    if not relevant_docs:
        print("⚠️ No relevant documents found!")
        return "I don't have relevant information to answer this question."
    
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    header("Found context")
    print(context)
    
    # Create prompt
    prompt = f"""Use the following context to answer the question.
    
Context: 
{context}

Question: {question}

Answer:"""
    
    # Get response from LLM
    response = llm.invoke(prompt)
    header("Response")
    print(response.content)
    return response.content

# Testing
ask_question("What do you know about animals?")

header("Demonstration completed!")
