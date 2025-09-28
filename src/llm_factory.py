import os
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

# Import various LLM libraries conditionally
try:
    from langchain.llms import Ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from langchain.chat_models import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from langchain.chat_models import ChatAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

logger = logging.getLogger(__name__)

class LLMBackend(ABC):
    """Abstract base class for LLM backends"""
    
    @abstractmethod
    def query(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        pass

class OllamaBackend(LLMBackend):
    """Ollama backend implementation"""
    
    def __init__(self, model: str = "mistral:7b", base_url: str = "http://localhost:11434", **kwargs):
        if not OLLAMA_AVAILABLE:
            raise ImportError("Ollama not available. Install with: pip install langchain")
        
        self.llm = Ollama(
            model=model,
            base_url=base_url,
            temperature=kwargs.get('temperature', 0.1)
        )
        self.model = model
        self.base_url = base_url
    
    def query(self, prompt: str, **kwargs) -> str:
        try:
            return self.llm(prompt)
        except Exception as e:
            logger.error(f"Ollama query failed: {e}")
            raise
    
    def health_check(self) -> bool:
        try:
            if not REQUESTS_AVAILABLE:
                return False
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

class OpenAIBackend(LLMBackend):
    """OpenAI backend implementation"""
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None, **kwargs):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI not available. Install with: pip install openai langchain")
        
        self.llm = ChatOpenAI(
            model=model,
            openai_api_key=api_key or os.getenv('OPENAI_API_KEY'),
            temperature=kwargs.get('temperature', 0.1),
            max_tokens=kwargs.get('max_tokens', 2000)
        )
        self.model = model
    
    def query(self, prompt: str, **kwargs) -> str:
        try:
            from langchain.schema import HumanMessage
            messages = [HumanMessage(content=prompt)]
            response = self.llm(messages)
            return response.content
        except Exception as e:
            logger.error(f"OpenAI query failed: {e}")
            raise
    
    def health_check(self) -> bool:
        try:
            # Simple test query
            test_response = self.query("Test", max_tokens=5)
            return len(test_response) > 0
        except Exception:
            return False

class AnthropicBackend(LLMBackend):
    """Anthropic Claude backend implementation"""
    
    def __init__(self, model: str = "claude-3-haiku-20240307", api_key: Optional[str] = None, **kwargs):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic not available. Install with: pip install anthropic langchain")
        
        self.llm = ChatAnthropic(
            model=model,
            anthropic_api_key=api_key or os.getenv('ANTHROPIC_API_KEY'),
            temperature=kwargs.get('temperature', 0.1),
            max_tokens=kwargs.get('max_tokens', 2000)
        )
        self.model = model
    
    def query(self, prompt: str, **kwargs) -> str:
        try:
            from langchain.schema import HumanMessage
            messages = [HumanMessage(content=prompt)]
            response = self.llm(messages)
            return response.content
        except Exception as e:
            logger.error(f"Anthropic query failed: {e}")
            raise
    
    def health_check(self) -> bool:
        try:
            # Simple test query
            test_response = self.query("Test", max_tokens=5)
            return len(test_response) > 0
        except Exception:
            return False

class TextGenWebUIBackend(LLMBackend):
    """text-generation-webui backend implementation"""
    
    def __init__(self, base_url: str = "http://localhost:5000", model: str = None, **kwargs):
        if not REQUESTS_AVAILABLE:
            raise ImportError("Requests not available. Install with: pip install requests")
        
        self.base_url = base_url
        self.model = model
        self.temperature = kwargs.get('temperature', 0.1)
        self.max_tokens = kwargs.get('max_tokens', 2000)
    
    def query(self, prompt: str, **kwargs) -> str:
        try:
            payload = {
                "prompt": prompt,
                "max_new_tokens": kwargs.get('max_tokens', self.max_tokens),
                "temperature": kwargs.get('temperature', self.temperature),
                "do_sample": True,
                "top_p": 0.9,
                "top_k": 20,
                "repetition_penalty": 1.1
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/generate",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result['results'][0]['text']
        except Exception as e:
            logger.error(f"TextGen WebUI query failed: {e}")
            raise
    
    def health_check(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/v1/model", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

class LocalAIBackend(LLMBackend):
    """LocalAI backend implementation"""
    
    def __init__(self, base_url: str = "http://localhost:8080", model: str = "gpt-3.5-turbo", **kwargs):
        if not REQUESTS_AVAILABLE:
            raise ImportError("Requests not available. Install with: pip install requests")
        
        self.base_url = base_url
        self.model = model
        self.temperature = kwargs.get('temperature', 0.1)
        self.max_tokens = kwargs.get('max_tokens', 2000)
    
    def query(self, prompt: str, **kwargs) -> str:
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": kwargs.get('temperature', self.temperature),
                "max_tokens": kwargs.get('max_tokens', self.max_tokens)
            }
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                timeout=60,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"LocalAI query failed: {e}")
            raise
    
    def health_check(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

class LLMFactory:
    """Factory class for creating LLM backend instances"""
    
    BACKENDS = {
        'ollama': OllamaBackend,
        'openai': OpenAIBackend,
        'anthropic': AnthropicBackend,
        'textgen': TextGenWebUIBackend,
        'localai': LocalAIBackend
    }
    
    @classmethod
    def create_backend(cls, backend_type: str, config: Dict[str, Any]) -> LLMBackend:
        """Create an LLM backend instance"""
        
        if backend_type not in cls.BACKENDS:
            raise ValueError(f"Unknown backend type: {backend_type}. Available: {list(cls.BACKENDS.keys())}")
        
        backend_class = cls.BACKENDS[backend_type]
        
        try:
            return backend_class(**config)
        except Exception as e:
            logger.error(f"Failed to create {backend_type} backend: {e}")
            raise
    
    @classmethod
    def get_available_backends(cls) -> Dict[str, bool]:
        """Check which backends are available based on installed dependencies"""
        availability = {}
        
        # Test each backend
        test_configs = {
            'ollama': {'model': 'test'},
            'openai': {'model': 'gpt-3.5-turbo', 'api_key': 'test'},
            'anthropic': {'model': 'claude-3-haiku-20240307', 'api_key': 'test'},
            'textgen': {'base_url': 'http://localhost:5000'},
            'localai': {'base_url': 'http://localhost:8080'}
        }
        
        for backend_name, backend_class in cls.BACKENDS.items():
            try:
                # Try to instantiate (will fail if dependencies missing)
                backend_class(**test_configs[backend_name])
                availability[backend_name] = True
            except ImportError:
                availability[backend_name] = False
            except Exception:
                # Other errors (like missing API keys) still mean backend is available
                availability[backend_name] = True
        
        return availability

class HybridLLM:
    """Hybrid LLM that can route queries to different backends based on configuration"""
    
    def __init__(self, primary_backend: LLMBackend, fallback_backend: Optional[LLMBackend] = None):
        self.primary_backend = primary_backend
        self.fallback_backend = fallback_backend
        self.use_fallback = False
    
    def query(self, prompt: str, **kwargs) -> str:
        """Query with automatic fallback"""
        try:
            if not self.use_fallback:
                return self.primary_backend.query(prompt, **kwargs)
            elif self.fallback_backend:
                return self.fallback_backend.query(prompt, **kwargs)
            else:
                raise Exception("Primary backend failed and no fallback available")
        except Exception as e:
            logger.warning(f"Primary backend failed: {e}")
            
            if self.fallback_backend and not self.use_fallback:
                logger.info("Switching to fallback backend")
                self.use_fallback = True
                return self.fallback_backend.query(prompt, **kwargs)
            else:
                raise
    
    def health_check(self) -> Dict[str, bool]:
        """Check health of both backends"""
        return {
            'primary': self.primary_backend.health_check(),
            'fallback': self.fallback_backend.health_check() if self.fallback_backend else None
        }
    
    def reset_fallback(self):
        """Reset to use primary backend"""
        self.use_fallback = False

# Configuration helper
def load_llm_config() -> Dict[str, Any]:
    """Load LLM configuration from environment variables"""
    backend_type = os.getenv('LLM_BACKEND', 'ollama').lower()
    
    configs = {
        'ollama': {
            'model': os.getenv('OLLAMA_MODEL', 'mistral:7b'),
            'base_url': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
            'temperature': float(os.getenv('OLLAMA_TEMPERATURE', '0.1'))
        },
        'openai': {
            'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            'api_key': os.getenv('OPENAI_API_KEY'),
            'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.1')),
            'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
        },
        'anthropic': {
            'model': os.getenv('ANTHROPIC_MODEL', 'claude-3-haiku-20240307'),
            'api_key': os.getenv('ANTHROPIC_API_KEY'),
            'temperature': float(os.getenv('ANTHROPIC_TEMPERATURE', '0.1')),
            'max_tokens': int(os.getenv('ANTHROPIC_MAX_TOKENS', '2000'))
        },
        'textgen': {
            'base_url': os.getenv('TEXTGEN_BASE_URL', 'http://localhost:5000'),
            'model': os.getenv('TEXTGEN_MODEL'),
            'temperature': float(os.getenv('TEXTGEN_TEMPERATURE', '0.1')),
            'max_tokens': int(os.getenv('TEXTGEN_MAX_TOKENS', '2000'))
        },
        'localai': {
            'base_url': os.getenv('LOCALAI_BASE_URL', 'http://localhost:8080'),
            'model': os.getenv('LOCALAI_MODEL', 'gpt-3.5-turbo'),
            'temperature': float(os.getenv('LOCALAI_TEMPERATURE', '0.1'))
        }
    }
    
    return backend_type, configs.get(backend_type, {})

# Example usage
if __name__ == "__main__":
    # Check available backends
    available = LLMFactory.get_available_backends()
    print("Available backends:", available)
    
    # Load configuration
    backend_type, config = load_llm_config()
    print(f"Using backend: {backend_type}")
    
    # Create backend
    try:
        backend = LLMFactory.create_backend(backend_type, config)
        print(f"Backend created successfully: {backend}")
        
        # Test health check
        health = backend.health_check()
        print(f"Health check: {health}")
        
        # Test query
        if health:
            response = backend.query("What is 2+2?")
            print(f"Test response: {response}")
        
    except Exception as e:
        print(f"Failed to create backend: {e}")