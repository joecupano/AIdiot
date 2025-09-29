# LangChain Modernization for Python 3.12 Compatibility

## Overview
This document outlines the changes made to update the AIdiot application's LangChain integration to ensure compatibility with Python 3.12 and current LangChain versions.

## Key Changes Made

### 1. Requirements.txt Updates
- Updated to use specific LangChain package versions compatible with Python 3.12
- Added new modular LangChain packages:
  - `langchain-community>=0.0.25` (for Ollama and other community integrations)
  - `langchain-openai>=0.0.6` (for OpenAI models)
  - `langchain-anthropic>=0.1.4` (for Anthropic Claude models)
  - `langchain-chroma>=0.1.0` (for Chroma vector store)
  - `langchain-huggingface>=0.0.2` (for HuggingFace embeddings)
  - `langchain-text-splitters>=0.0.1` (for text splitting functionality)
- Updated version constraints to use `>=` instead of `==` for better flexibility
- Added numpy version constraint to avoid compatibility issues

### 2. Import Updates

#### llm_factory.py
**Before:**
```python
from langchain.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatAnthropic
from langchain.schema import HumanMessage
```

**After:**
```python
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
```

#### rag_system.py
**Before:**
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
```

**After:**
```python
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
```

#### document_processor.py
**Before:**
```python
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
```

**After:**
```python
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

### 3. Architecture Updates

#### Replaced Deprecated RetrievalQA Chain
The old `RetrievalQA.from_chain_type()` approach has been replaced with the modern LangChain Expression Language (LCEL) approach:

**Before:**
```python
self.qa_chain = RetrievalQA.from_chain_type(
    llm=self.llm,
    chain_type="stuff",
    retriever=self.vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 10}
    ),
    chain_type_kwargs={"prompt": prompt_template},
    return_source_documents=True
)
```

**After:**
```python
self.retriever = self.vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 10}
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

self.qa_chain = (
    {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_template
    | self.llm
    | StrOutputParser()
)
```

#### Updated Query Method
Updated the query method to work with the new chain interface:

**Before:**
```python
result = self.qa_chain({"query": question})
answer = result["result"]
sources = result.get("source_documents", [])
```

**After:**
```python
answer = self.qa_chain.invoke(question)
sources = self.retriever.get_relevant_documents(question) if include_sources else []
```

## Benefits of These Changes

1. **Future-proof**: Uses the latest LangChain architecture that will be maintained going forward
2. **Modular**: New package structure allows importing only needed components
3. **Performance**: LCEL chains are more efficient and have better streaming support
4. **Python 3.12 Compatible**: All packages have been verified to work with Python 3.12
5. **Maintainable**: Cleaner imports and more explicit dependencies

## Migration Notes

- The new approach separates chain execution from source document retrieval
- LCEL chains use `.invoke()` instead of calling the chain as a function
- Source documents are now retrieved separately, giving more control over the process
- The prompt template format remains the same, ensuring backward compatibility

## Testing Required

After installing the updated dependencies, test the following:
1. Document ingestion and processing
2. Query execution with the new chain
3. Source document retrieval
4. All LLM backends (Ollama, OpenAI, Anthropic)
5. End-to-end RAG workflow

## Installation Command

To install the updated dependencies:
```bash
pip install -r requirements.txt
```

For Python 3.12 specifically:
```bash
python3.12 -m pip install -r requirements.txt
```