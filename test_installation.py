#!/usr/bin/env python3
"""
Test script to verify AIdiot installation and basic functionality.
Run this after installation to check if everything is working properly.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import langchain
        print("✅ LangChain imported successfully")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    try:
        import chromadb
        print("✅ ChromaDB imported successfully")
    except ImportError as e:
        print(f"❌ ChromaDB import failed: {e}")
        return False
    
    try:
        import sentence_transformers
        print("✅ Sentence Transformers imported successfully")
    except ImportError as e:
        print(f"❌ Sentence Transformers import failed: {e}")
        return False
    
    try:
        from src.config import OLLAMA_MODEL, EMBEDDING_MODEL
        print("✅ Configuration loaded successfully")
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False
    
    return True


def test_ollama_connection():
    """Test Ollama connection and model availability."""
    print("\n🔍 Testing Ollama connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama is running")
            
            # Check for Mistral model
            model_names = [model['name'] for model in models.get('models', [])]
            if 'mistral:7b' in model_names:
                print("✅ Mistral 7B model is available")
                return True
            else:
                print("⚠️  Mistral 7B model not found")
                print("Run: ollama pull mistral:7b")
                return False
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama (is it running?)")
        return False
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False


def test_rag_system():
    """Test RAG system initialization."""
    print("\n🔍 Testing RAG system initialization...")
    
    try:
        from src.rag_system import DomainRAG
        
        rag = DomainRAG()
        print("✅ RAG system initialized")
        
        # Test health check
        health = rag.health_check()
        print(f"📊 Health check results: {health}")
        
        if health.get('embeddings', False):
            print("✅ Embeddings working")
        else:
            print("❌ Embeddings failed")
        
        if health.get('vectorstore', False):
            print("✅ Vector store working")
        else:
            print("❌ Vector store failed")
        
        return all(health.values())
        
    except Exception as e:
        print(f"❌ RAG system test failed: {e}")
        return False


def test_document_processor():
    """Test document processor."""
    print("\n🔍 Testing document processor...")
    
    try:
        from src.document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        print("✅ Document processor initialized")
        
        # Test URL processing (simple test)
        test_url = "https://httpbin.org/html"
        try:
            docs = processor.process_url(test_url)
            print(f"✅ URL processing works (processed {len(docs)} chunks)")
        except Exception as e:
            print(f"⚠️  URL processing test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Document processor test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 AIdiot Installation Test\n")
    
    tests = [
        test_imports,
        test_ollama_connection,
        test_document_processor,
        test_rag_system
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    print("📊 Test Summary:")
    
    test_names = ["Imports", "Ollama", "Document Processor", "RAG System"]
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    total_passed = sum(results)
    total_tests = len(results)
    
    print(f"\nResults: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! AIdiot is ready to use.")
        print("\nNext steps:")
        print("1. Add some documents: python main.py add-documents ./data/pdfs/")
        print("2. Try interactive mode: python main.py interactive")
        print("3. Start the API: python main.py serve")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        print("Common solutions:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Start Ollama: ollama serve")
        print("- Pull model: ollama pull mistral:7b")
    
    return total_passed == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)