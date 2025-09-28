# Multi-Backend LLM Configuration Examples

This guide shows how to configure the AI Assistant to use different LLM backends instead of the default Ollama setup.

## Configuration Methods

### 1. Environment Variables

The easiest way to switch backends is using environment variables:

```bash
# Use OpenAI GPT
export LLM_BACKEND=openai
export OPENAI_API_KEY=your_api_key_here
export OPENAI_MODEL=gpt-4

# Use Anthropic Claude
export LLM_BACKEND=anthropic
export ANTHROPIC_API_KEY=your_api_key_here
export ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Use text-generation-webui
export LLM_BACKEND=textgen
export TEXTGEN_BASE_URL=http://localhost:5000

# Use LocalAI
export LLM_BACKEND=localai
export LOCALAI_BASE_URL=http://localhost:8080
export LOCALAI_MODEL=codellama
```

### 2. .env File Configuration

Create a `.env` file in your project root:

```env
# Primary backend configuration
LLM_BACKEND=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=2000

# Ollama fallback (if primary fails)
OLLAMA_MODEL=mistral:7b
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TEMPERATURE=0.1
```

## Backend-Specific Setup Instructions

### OpenAI Setup

1. Get API key from [OpenAI Platform](https://platform.openai.com/)
2. Set environment variables:
```bash
export LLM_BACKEND=openai
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4
```

3. Install dependencies:
```bash
pip install openai
```

### Anthropic Claude Setup

1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Set environment variables:
```bash
export LLM_BACKEND=anthropic
export ANTHROPIC_API_KEY=your_key_here
export ANTHROPIC_MODEL=claude-3-haiku-20240307
```

3. Install dependencies:
```bash
pip install anthropic
```

### text-generation-webui Setup

1. Install text-generation-webui:
```bash
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui
pip install -r requirements.txt
```

2. Start the server:
```bash
python server.py --api --listen
```

3. Configure the AI Assistant:
```bash
export LLM_BACKEND=textgen
export TEXTGEN_BASE_URL=http://localhost:5000
```

### LocalAI Setup

1. Install LocalAI:
```bash
# Using Docker
docker run -p 8080:8080 --name local-ai -ti localai/localai:latest

# Or download binary from GitHub releases
```

2. Configure model:
```bash
# Download a model (example)
curl -o model.bin https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/pytorch_model.bin
```

3. Configure the AI Assistant:
```bash
export LLM_BACKEND=localai
export LOCALAI_BASE_URL=http://localhost:8080
export LOCALAI_MODEL=your-model-name
```

### LM Studio Setup

While not directly integrated, you can use LM Studio's OpenAI-compatible API:

1. Install LM Studio from [https://lmstudio.ai/](https://lmstudio.ai/)
2. Download a model in LM Studio
3. Start the local server (OpenAI compatible)
4. Configure as OpenAI backend:
```bash
export LLM_BACKEND=openai
export OPENAI_API_KEY=not-needed
export OPENAI_BASE_URL=http://localhost:1234/v1
export OPENAI_MODEL=your-model-name
```

## Testing Your Configuration

Use the built-in health check:

```python
from src.rag_system import DomainRAG

# Initialize system
rag = DomainRAG()

# Check health of all components
status = rag.health_check()
print("System Status:", status)

# Test a simple query
response = rag.query("What is a low-pass filter?")
print("Response:", response)
```

Or use the CLI:

```bash
python main.py query "Test query" --health-check
```

## Performance Considerations

### Local vs Cloud Backends

**Local Backends (Ollama, text-generation-webui, LocalAI):**
- ✅ Privacy (no data sent to cloud)
- ✅ No API costs
- ✅ Offline operation
- ❌ Slower inference
- ❌ Limited model quality
- ❌ Requires powerful hardware

**Cloud Backends (OpenAI, Anthropic):**
- ✅ Fast inference
- ✅ High-quality responses
- ✅ No local hardware requirements
- ❌ API costs
- ❌ Data privacy concerns
- ❌ Requires internet connection

### Recommended Configurations

**For Development/Testing:**
```env
LLM_BACKEND=openai
OPENAI_MODEL=gpt-3.5-turbo
```

**For Production (Privacy-First):**
```env
LLM_BACKEND=ollama
OLLAMA_MODEL=mistral:7b
# Runs completely offline, no data sent to cloud
```

**For Production (Performance-First):**
```env
LLM_BACKEND=anthropic
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

**For Hybrid (Best of Both):**
```env
LLM_BACKEND=anthropic
ANTHROPIC_MODEL=claude-3-haiku-20240307
# Ollama as fallback (configured automatically)
OLLAMA_MODEL=mistral:7b
# Fast cloud primary + reliable local fallback
```

## Troubleshooting

### Common Issues

1. **Import Errors:**
   ```bash
   # Install missing dependencies
   pip install openai anthropic ollama
   ```

2. **API Key Issues:**
   ```bash
   # Check your API key is valid
   echo $OPENAI_API_KEY
   ```

3. **Connection Issues:**
   ```bash
   # Test local server is running
   curl http://localhost:11434/api/tags  # Ollama
   curl http://localhost:5000/api/v1/model  # text-generation-webui
   ```

4. **Model Not Found:**
   - Ensure the model name exactly matches what's available
   - For Ollama: `ollama list`
   - For OpenAI: Check [model documentation](https://platform.openai.com/docs/models)

### Health Check Failed

If the health check fails:

1. Check network connectivity
2. Verify API keys are correct
3. Ensure the backend service is running
4. Check the logs for detailed error messages

### Fallback System

The system automatically falls back to Ollama if the primary backend fails:

```python
# System will try primary backend first
response = rag.query("Your question")

# If primary fails, it switches to Ollama automatically
# You can manually reset to try primary again
rag.hybrid_llm.reset_fallback()
```

## Custom Backend Implementation

To add a new backend, create a class inheriting from `LLMBackend`:

```python
from src.llm_factory import LLMBackend

class CustomBackend(LLMBackend):
    def __init__(self, **kwargs):
        # Initialize your backend
        pass
    
    def query(self, prompt: str, **kwargs) -> str:
        # Implement query logic
        pass
    
    def health_check(self) -> bool:
        # Implement health check
        pass

# Register with factory
LLMFactory.BACKENDS['custom'] = CustomBackend
```

This flexibility allows you to integrate any LLM service or local model that suits your specific needs.