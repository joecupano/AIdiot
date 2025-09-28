#!/usr/bin/env python3
"""
Test script to verify multi-backend LLM setup is working correctly
"""

import os
import sys
from pathlib import Path
import tempfile

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_llm_factory():
    """Test the LLM factory functionality"""
    print("🧪 Testing LLM Factory...")
    
    try:
        from llm_factory import LLMFactory, load_llm_config
        
        # Check available backends
        available = LLMFactory.get_available_backends()
        print(f"Available backends: {available}")
        
        # Test configuration loading
        backend_type, config = load_llm_config()
        print(f"Current backend: {backend_type}")
        print(f"Configuration: {config}")
        
        # Try to create a backend
        if available.get(backend_type, False):
            try:
                backend = LLMFactory.create_backend(backend_type, config)
                print(f"✅ Successfully created {backend_type} backend")
                
                # Test health check
                health = backend.health_check()
                print(f"Health check: {health}")
                
                if health:
                    # Test simple query
                    try:
                        response = backend.query("What is 2+2?")
                        print(f"✅ Query test successful: {response[:100]}...")
                        return True
                    except Exception as e:
                        print(f"⚠️  Query failed: {e}")
                        return False
                else:
                    print("⚠️  Backend not healthy")
                    return False
                    
            except Exception as e:
                print(f"❌ Failed to create backend: {e}")
                return False
        else:
            print(f"⚠️  Backend {backend_type} not available")
            return False
            
    except Exception as e:
        print(f"❌ LLM Factory test failed: {e}")
        return False

def test_rag_system():
    """Test the RAG system with multi-backend support"""
    print("\n🧪 Testing RAG System...")
    
    try:
        from rag_system import DomainRAG
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set temporary vector DB location
            os.environ['VECTOR_DB_DIR'] = temp_dir
            
            try:
                rag = DomainRAG()
                print("✅ RAG system initialized")
                
                # Test health check
                status = rag.health_check()
                print(f"RAG Health Status: {status}")
                
                # Check if core components are working
                embeddings_ok = status.get('embeddings', False)
                vectorstore_ok = status.get('vectorstore', False)
                llm_ok = status.get('llm', False)
                
                if embeddings_ok and vectorstore_ok:
                    print("✅ RAG core components working")
                    
                    if llm_ok:
                        print("✅ LLM integration working")
                        return True
                    else:
                        print("⚠️  LLM not working, but core RAG components OK")
                        return False
                else:
                    print("❌ RAG core components failed")
                    return False
                    
            except Exception as e:
                print(f"❌ RAG initialization failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ RAG system test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading and validation"""
    print("\n🧪 Testing Configuration...")
    
    try:
        from config import (
            VECTOR_DB_DIR, EMBEDDING_MODEL, OLLAMA_MODEL, 
            OLLAMA_BASE_URL, VECTOR_DB_COLLECTION
        )
        
        print(f"Vector DB Directory: {VECTOR_DB_DIR}")
        print(f"Embedding Model: {EMBEDDING_MODEL}")
        print(f"Ollama Model: {OLLAMA_MODEL}")
        print(f"Ollama Base URL: {OLLAMA_BASE_URL}")
        print(f"Collection Name: {VECTOR_DB_COLLECTION}")
        
        # Check if paths are valid
        if Path(VECTOR_DB_DIR).parent.exists():
            print("✅ Configuration paths are valid")
            return True
        else:
            print("❌ Configuration paths invalid")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are available"""
    print("\n🧪 Testing Dependencies...")
    
    required_packages = [
        ("langchain", "LangChain framework"),
        ("chromadb", "Vector database"),
        ("sentence_transformers", "Embeddings"),
        ("PyMuPDF", "PDF processing"),
        ("PIL", "Image processing"),
        ("cv2", "OpenCV"),
        ("requests", "HTTP requests"),
        ("fastapi", "Web API"),
        ("rich", "CLI formatting"),
        ("typer", "CLI framework")
    ]
    
    optional_packages = [
        ("ollama", "Ollama client"),
        ("openai", "OpenAI client"),
        ("anthropic", "Anthropic client"),
        ("pytesseract", "OCR support")
    ]
    
    all_good = True
    
    print("Required packages:")
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package} - {description}")
        except ImportError:
            print(f"  ❌ {package} - {description} (REQUIRED)")
            all_good = False
    
    print("Optional packages:")
    for package, description in optional_packages:
        try:
            __import__(package)
            print(f"  ✅ {package} - {description}")
        except ImportError:
            print(f"  ⚠️  {package} - {description} (optional)")
    
    return all_good

def main():
    """Run all tests"""
    print("🚀 Multi-Backend AI Assistant Test Suite\n")
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_configuration), 
        ("LLM Factory", test_llm_factory),
        ("RAG System", test_rag_system)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Test Results Summary:")
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return 0
    elif passed >= total - 1:
        print("⚠️  Most tests passed. System should work with minor limitations.")
        return 0
    else:
        print("❌ Multiple test failures. Please check your setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())