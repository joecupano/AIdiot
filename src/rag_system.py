import logging
from typing import List, Optional, Any, Dict
from pathlib import Path
import chromadb
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from .config import (
    VECTOR_DB_DIR, EMBEDDING_MODEL, OLLAMA_MODEL, 
    OLLAMA_BASE_URL, VECTOR_DB_COLLECTION
)
from .llm_factory import LLMFactory, HybridLLM, load_llm_config

logger = logging.getLogger(__name__)


class DomainRAG:
    """RAG system for technical documentation and analysis."""
    
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize RAG components."""
        try:
            # Initialize embeddings
            logger.info("Initializing embeddings model...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'}
            )
            
            # Initialize ChromaDB client
            chroma_client = chromadb.PersistentClient(
                path=str(VECTOR_DB_DIR),
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Initialize vector store
            self.vectorstore = Chroma(
                client=chroma_client,
                collection_name=VECTOR_DB_COLLECTION,
                embedding_function=self.embeddings
            )
            
            # Initialize LLM with factory pattern
            logger.info("Initializing LLM backend...")
            backend_type, backend_config = load_llm_config()
            
            # Create primary backend
            primary_backend = LLMFactory.create_backend(backend_type, backend_config)
            
            # Try to create fallback backend (Ollama if not primary)
            fallback_backend = None
            if backend_type != 'ollama':
                try:
                    fallback_config = {
                        'model': OLLAMA_MODEL,
                        'base_url': OLLAMA_BASE_URL,
                        'temperature': 0.1
                    }
                    fallback_backend = LLMFactory.create_backend('ollama', fallback_config)
                    logger.info("Fallback Ollama backend configured")
                except Exception as e:
                    logger.warning(f"Could not create Ollama fallback: {e}")
            
            # Create hybrid LLM with fallback
            self.hybrid_llm = HybridLLM(primary_backend, fallback_backend)
            
            # For compatibility with existing LangChain code, wrap the backend
            class LangChainWrapper:
                def __init__(self, backend):
                    self.backend = backend
                
                def __call__(self, prompt):
                    return self.backend.query(prompt)
            
            self.llm = LangChainWrapper(primary_backend)
            
            # Create specialized prompt template
            prompt_template = self._create_domain_prompt()
            
            # Initialize QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_type="mmr",  # Maximal Marginal Relevance
                    search_kwargs={"k": 5, "fetch_k": 10}
                ),
                chain_type_kwargs={"prompt": prompt_template},
                return_source_documents=True
            )
            
            logger.info("RAG system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG system: {str(e)}")
            raise
    
    def _create_domain_prompt(self) -> PromptTemplate:
        """Create specialized prompt template for domain applications."""
        template = """
You are an expert technical advisor with deep knowledge of:

- RF circuit design and analysis
- Antenna theory and design
- Transmission line theory and impedance matching
- Smith Chart calculations
- Filter design (low-pass, high-pass, band-pass, notch)
- Amplifier design (Class A, B, AB, C, D, E, F)
- Oscillator circuits and frequency synthesis
- Modulation and demodulation techniques
- Microwave and millimeter-wave techniques
- EMC/EMI considerations
- Technical regulations and standards
- Low power techniques
- System design and optimization

Use the following context from technical documentation to answer the question. Be precise, technical, and include relevant formulas, component values, and design considerations when applicable.

Context: {context}

Question: {question}

Provide a comprehensive technical answer that includes:
1. Direct answer to the question
2. Relevant formulas or calculations if applicable
3. Practical design considerations
4. Component recommendations when appropriate
5. References to standards or common practices
6. Safety considerations if relevant

Answer:"""

        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to the vector store."""
        try:
            if not documents:
                logger.warning("No documents to add")
                return False
            
            logger.info(f"Adding {len(documents)} documents to vector store...")
            
            # Filter for domain relevant content
            relevant_docs = [
                doc for doc in documents 
                if doc.metadata.get('domain_relevant', False)
            ]
            
            if not relevant_docs:
                logger.warning("No domain relevant documents found")
                # Add all documents anyway, but with lower relevance
                relevant_docs = documents
            
            # Add documents to vector store
            self.vectorstore.add_documents(relevant_docs)
            
            logger.info(f"Successfully added {len(relevant_docs)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add documents: {str(e)}")
            return False
    
    def query(self, question: str, include_sources: bool = True) -> Dict[str, Any]:
        """Query the RAG system."""
        try:
            if not self.qa_chain:
                raise ValueError("RAG system not properly initialized")
            
            logger.info(f"Processing query: {question}")
            
            # Query the chain
            result = self.qa_chain({"query": question})
            
            response = {
                "answer": result["result"],
                "question": question,
                "sources": []
            }
            
            if include_sources and "source_documents" in result:
                for doc in result["source_documents"]:
                    source_info = {
                        "content": doc.page_content[:200] + "...",  # First 200 chars
                        "metadata": doc.metadata
                    }
                    response["sources"].append(source_info)
            
            return response
            
        except Exception as e:
            logger.error(f"Query failed: {str(e)}")
            return {
                "answer": f"Error processing query: {str(e)}",
                "question": question,
                "sources": []
            }
    
    def get_similar_documents(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve similar documents without LLM processing."""
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return docs
        except Exception as e:
            logger.error(f"Similarity search failed: {str(e)}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the document collection."""
        try:
            collection = self.vectorstore._collection
            count = collection.count()
            
            # Get sample documents to analyze metadata
            if count > 0:
                sample_docs = self.vectorstore.similarity_search("antenna", k=min(100, count))
                
                # Analyze document types
                doc_types = {}
                sources = set()
                
                for doc in sample_docs:
                    doc_type = doc.metadata.get('type', 'unknown')
                    doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
                    
                    source = doc.metadata.get('source', 'unknown')
                    sources.add(source)
                
                return {
                    "total_documents": count,
                    "document_types": doc_types,
                    "unique_sources": len(sources),
                    "sample_sources": list(sources)[:10]  # First 10 sources
                }
            else:
                return {"total_documents": 0}
                
        except Exception as e:
            logger.error(f"Failed to get collection stats: {str(e)}")
            return {"error": str(e)}
    
    def delete_collection(self) -> bool:
        """Delete the entire document collection."""
        try:
            self.vectorstore._collection.delete()
            logger.info("Document collection deleted")
            return True
        except Exception as e:
            logger.error(f"Failed to delete collection: {str(e)}")
            return False
    
    def health_check(self) -> Dict[str, bool]:
        """Check the health of all RAG components."""
        status = {
            "embeddings": False,
            "vectorstore": False,
            "llm": False,
            "qa_chain": False
        }
        
        try:
            # Test embeddings
            if self.embeddings:
                test_embedding = self.embeddings.embed_query("test")
                status["embeddings"] = len(test_embedding) > 0
            
            # Test vector store
            if self.vectorstore:
                count = self.vectorstore._collection.count()
                status["vectorstore"] = count >= 0
            
            # Test LLM (both primary and fallback if available)
            if hasattr(self, 'hybrid_llm'):
                llm_health = self.hybrid_llm.health_check()
                status["llm"] = llm_health.get('primary', False)
                if llm_health.get('fallback') is not None:
                    status["llm_fallback"] = llm_health['fallback']
            elif self.llm:
                test_response = self.llm("Say 'OK'")
                status["llm"] = "OK" in test_response or "ok" in test_response.lower()
            
            # Test QA chain
            if self.qa_chain and status["vectorstore"] and status["llm"]:
                status["qa_chain"] = True
                
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
        
        return status