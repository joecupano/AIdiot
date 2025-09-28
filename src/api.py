from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from pathlib import Path
import tempfile
import shutil
import json
from datetime import datetime

from .document_processor import DocumentProcessor
from .rag_system import DomainRAG
from .config import API_HOST, API_PORT, LOG_LEVEL

# Setup logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AIdiot API",
    description="AI Assistant - RESTful API for technical design and analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
doc_processor = DocumentProcessor()
rag_system = None


def get_rag_system() -> DomainRAG:
    """Get or initialize the RAG system."""
    global rag_system
    if rag_system is None:
        rag_system = DomainRAG()
    return rag_system


# Pydantic models
class QueryRequest(BaseModel):
    question: str
    include_sources: bool = True


class QueryResponse(BaseModel):
    answer: str
    question: str
    sources: List[Dict[str, Any]] = []
    timestamp: str


class URLRequest(BaseModel):
    url: str


class DocumentStats(BaseModel):
    total_documents: int
    document_types: Dict[str, int]
    unique_sources: int
    sample_sources: List[str]


class HealthStatus(BaseModel):
    embeddings: bool
    vectorstore: bool
    llm: bool
    qa_chain: bool
    overall_healthy: bool


class DocumentUploadResponse(BaseModel):
    success: bool
    message: str
    documents_added: int


# API Routes

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AIdiot API",
        "description": "AI Assistant",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "query": "POST /query - Ask questions",
            "upload_file": "POST /documents/upload - Upload documents",
            "add_url": "POST /documents/url - Add URL content",
            "stats": "GET /stats - Knowledge base statistics",
            "health": "GET /health - System health check",
            "docs": "GET /docs - API documentation"
        }
    }


@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """Query the technical knowledge base."""
    try:
        rag = get_rag_system()
        
        logger.info(f"Processing query: {request.question}")
        response = rag.query(request.question, include_sources=request.include_sources)
        
        return QueryResponse(
            answer=response["answer"],
            question=response["question"],
            sources=response["sources"],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document (PDF or image)."""
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = Path(tmp_file.name)
        
        try:
            # Process document
            logger.info(f"Processing uploaded file: {file.filename}")
            
            if file_extension == '.pdf':
                documents = doc_processor.process_pdf(tmp_path)
            else:
                documents = doc_processor.process_image(tmp_path)
            
            if not documents:
                return DocumentUploadResponse(
                    success=False,
                    message="No content could be extracted from the file",
                    documents_added=0
                )
            
            # Add to knowledge base
            rag = get_rag_system()
            success = rag.add_documents(documents)
            
            if success:
                return DocumentUploadResponse(
                    success=True,
                    message=f"Successfully processed {file.filename}",
                    documents_added=len(documents)
                )
            else:
                return DocumentUploadResponse(
                    success=False,
                    message="Failed to add documents to knowledge base",
                    documents_added=0
                )
                
        finally:
            # Clean up temporary file
            tmp_path.unlink(missing_ok=True)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")


@app.post("/documents/url", response_model=DocumentUploadResponse)
async def add_url_content(request: URLRequest):
    """Process and add content from a URL."""
    try:
        logger.info(f"Processing URL: {request.url}")
        
        # Process URL
        documents = doc_processor.process_url(request.url)
        
        if not documents:
            return DocumentUploadResponse(
                success=False,
                message="No content could be extracted from the URL",
                documents_added=0
            )
        
        # Add to knowledge base
        rag = get_rag_system()
        success = rag.add_documents(documents)
        
        if success:
            return DocumentUploadResponse(
                success=True,
                message=f"Successfully processed content from {request.url}",
                documents_added=len(documents)
            )
        else:
            return DocumentUploadResponse(
                success=False,
                message="Failed to add documents to knowledge base",
                documents_added=0
            )
            
    except Exception as e:
        logger.error(f"URL processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"URL processing failed: {str(e)}")


@app.get("/stats", response_model=DocumentStats)
async def get_knowledge_base_stats():
    """Get statistics about the knowledge base."""
    try:
        rag = get_rag_system()
        stats = rag.get_collection_stats()
        
        if "error" in stats:
            raise HTTPException(status_code=500, detail=stats["error"])
        
        return DocumentStats(
            total_documents=stats.get("total_documents", 0),
            document_types=stats.get("document_types", {}),
            unique_sources=stats.get("unique_sources", 0),
            sample_sources=stats.get("sample_sources", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Stats retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")


@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Check the health of all system components."""
    try:
        rag = get_rag_system()
        health = rag.health_check()
        
        return HealthStatus(
            embeddings=health.get("embeddings", False),
            vectorstore=health.get("vectorstore", False),
            llm=health.get("llm", False),
            qa_chain=health.get("qa_chain", False),
            overall_healthy=all(health.values())
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthStatus(
            embeddings=False,
            vectorstore=False,
            llm=False,
            qa_chain=False,
            overall_healthy=False
        )


@app.get("/similar/{query}")
async def get_similar_documents(query: str, limit: int = 5):
    """Get similar documents without LLM processing."""
    try:
        rag = get_rag_system()
        documents = rag.get_similar_documents(query, k=limit)
        
        return {
            "query": query,
            "documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in documents
            ]
        }
        
    except Exception as e:
        logger.error(f"Similarity search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Similarity search failed: {str(e)}")


@app.delete("/documents")
async def clear_knowledge_base():
    """Clear all documents from the knowledge base."""
    try:
        rag = get_rag_system()
        success = rag.delete_collection()
        
        if success:
            return {"success": True, "message": "Knowledge base cleared successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear knowledge base")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Clear operation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Clear operation failed: {str(e)}")


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "detail": "The requested endpoint does not exist"}


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "detail": "An unexpected error occurred"}


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    logger.info("Starting AIdiot API server...")
    
    try:
        # Initialize RAG system
        get_rag_system()
        logger.info("RAG system initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {str(e)}")
        # Continue startup even if RAG system fails - it can be retried later


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )