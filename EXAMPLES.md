# AIdiot Usage Examples

Practical examples of using the AI Assistant with the modern LangChain architecture, Python 3.12, and robust error handling with automatic fallbacks.

## 🚀 **Getting Started**

```bash
# Initial setup with Python 3.12 and dependency checking
python main.py setup

# Add your first document (PDF manual) - with automatic OCR fallback
python main.py add-documents "ARRL_Antenna_Book.pdf"

# Ask your first question using modern LCEL chains
python main.py query "What is the formula for dipole antenna length?"

# Check system status and dependency availability
python main.py health
python main.py stats
```

## 📚 **Building a Knowledge Base**

### Adding Various Document Types

```bash
# Add multiple PDFs from a directory
python main.py add-documents ./rf_manuals/

# Add schematic diagrams (with OCR processing)
python main.py add-documents filter_schematic.png
python main.py add-documents amplifier_circuit.jpg

# Add web content
python main.py add-documents --url https://www.arrl.org/antenna-basics
python main.py add-documents --url https://ham.stackexchange.com/questions/tagged/antenna-design

# Batch processing with multiple URLs
python main.py add-documents \
    --url https://www.electronics-tutorials.ws/filter/filter_2.html \
    --url https://www.allaboutcircuits.com/textbook/alternating-current/chpt-8/
```

### Advanced Document Processing

```bash
# Process directory with specific file types
python main.py add-documents ./documents/ --filter "*.pdf,*.png,*.jpg"

# Add documents with custom metadata
python main.py add-documents technical_manual.pdf --metadata '{"category": "manual", "domain": "rf"}'

# Process with specific OCR settings for technical diagrams
# Note: Automatically uses PyMuPDF fallback if Poppler unavailable
python main.py add-documents circuit_diagram.png --ocr-mode advanced

# Process image-heavy PDF with fallback handling
# System will try pdf2image first, then PyMuPDF if Poppler missing
python main.py add-documents schematic_collection.pdf --force-ocr
```

### Dependency Fallback Examples

```bash
# Check what dependencies are available
python -c "from src.document_processor import CV2_AVAILABLE, PDF2IMAGE_AVAILABLE; print(f'OpenCV: {CV2_AVAILABLE}, pdf2image: {PDF2IMAGE_AVAILABLE}')"

# Process documents without OpenCV (headless mode)
# System automatically uses PIL-based processing
export CV2_DISABLE=1
python main.py add-documents technical_diagram.png

# Process PDFs without Poppler
# System automatically uses PyMuPDF fallback for OCR
python main.py add-documents --force-ocr manual_scan.pdf
```

## 💬 **Interactive Mode Examples**

```bash
# Start interactive mode with modern LangChain backend
python main.py interactive

# Example conversation with updated RAG system:
📡 Your question: How do I calculate the resonant frequency of an LC circuit?

🤖 Answer: The resonant frequency of an LC circuit is calculated using the formula:

f = 1 / (2π√(LC))

Where:
- f = resonant frequency in Hz
- L = inductance in henries (H)  
- C = capacitance in farads (F)

For example, with L = 10µH and C = 100pF:
f = 1 / (2π√(10×10⁻⁶ × 100×10⁻¹²))
f = 1 / (2π√(10⁻¹⁵))
f ≈ 15.92 MHz

📚 Sources: RF_Handbook.pdf (p.45), LC_Circuits.pdf (p.12)

📡 Your question: What's the bandwidth of this circuit?

🤖 Answer: The bandwidth of an LC resonant circuit depends on its Q factor:

BW = f₀ / Q

Where Q (quality factor) = ωL / R = (1/R)√(L/C)

For the previous example with Q = 100:
BW = 15.92 MHz / 100 = 159.2 kHz

The 3dB bandwidth extends from f₀ - BW/2 to f₀ + BW/2.

📡 Your question: /stats

📊 Knowledge Base Stats: {
  "total_documents": 157,
  "document_chunks": 1847,
  "document_types": {
    "pdf": 89,
    "web": 45, 
    "images": 23
  },
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "vector_store": "chromadb",
  "llm_backend": "ollama:mistral:7b"
}

📡 Your question: /help

Available commands:
- /stats - Show knowledge base statistics
- /health - Check system health
- /switch-backend openai - Switch to different LLM backend
- /clear - Clear conversation history
- /exit - Exit interactive mode
```

## 🌐 **Web API Examples**

### Starting the API Server

```bash
# Start with default settings (Python 3.12 compatible)
python main.py serve

# Start with custom configuration
python main.py serve --host 0.0.0.0 --port 8080 --reload

# Start with specific backend
LLM_BACKEND=openai python main.py serve
```

### Python Client Examples

```python
import requests
import json

# Base URL for the API
base_url = "http://localhost:8000"

# Start the API server first
# python main.py serve

# 1. Ask a question
def ask_question(question):
    response = requests.post(f"{base_url}/query", json={
# Query the API
def ask_question(question):
    response = requests.post(f"{base_url}/query", json={
        "question": question,
        "include_sources": True,
        "backend": "auto"  # Let system choose best backend
    })
    return response.json()

# Example questions with modern backend support
answer = ask_question("How do I design a Yagi antenna for 2 meters?")
print(f"Answer: {answer['answer']}")
print(f"Sources: {len(answer['sources'])} documents")
print(f"Backend used: {answer.get('backend_used', 'default')}")

# Upload documents with metadata
def upload_document(file_path, metadata=None):
    with open(file_path, 'rb') as f:
        files = {"file": f}
        data = {"metadata": json.dumps(metadata)} if metadata else {}
        response = requests.post(f"{base_url}/documents/upload", 
                               files=files, data=data)
    return response.json()

result = upload_document("antenna_manual.pdf", {
    "category": "antenna", 
    "difficulty": "intermediate",
    "tags": ["yagi", "2m", "vhf"]
})
print(f"Upload result: {result['message']}")

# Add URL content with processing options  
def add_url(url, options=None):
    payload = {"url": url}
    if options:
        payload.update(options)
    response = requests.post(f"{base_url}/documents/url", json=payload)
    return response.json()

result = add_url("https://www.arrl.org/impedance-matching", {
    "extract_images": True,
    "follow_links": False,
    "max_depth": 1
})
print(f"URL processing: {result['message']}")

# Get enhanced statistics
def get_stats():
    response = requests.get(f"{base_url}/stats")
    return response.json()

stats = get_stats()
print(f"Total documents: {stats['total_documents']}")
print(f"Total chunks: {stats['document_chunks']}")
print(f"Document types: {stats['document_types']}")
print(f"Embedding model: {stats['embedding_model']}")
print(f"Current LLM backend: {stats['llm_backend']}")

# Enhanced health check
def health_check():
    response = requests.get(f"{base_url}/health")
    return response.json()

health = health_check()
print(f"System healthy: {health['overall_healthy']}")
print(f"Components: {health['components']}")
print(f"Backend status: {health['backend_status']}")

# Backend switching
def switch_backend(backend_name, config=None):
    payload = {"backend": backend_name}
    if config:
        payload["config"] = config
    response = requests.post(f"{base_url}/backend/switch", json=payload)
    return response.json()

# Switch to OpenAI for complex queries
result = switch_backend("openai", {
    "model": "gpt-4-turbo",
    "temperature": 0.1
})
print(f"Backend switch: {result['message']}")
```

### Modern JavaScript/TypeScript Client

```typescript
// Modern TypeScript client with async/await
interface QueryRequest {
    question: string;
    include_sources?: boolean;
    backend?: string;
    max_tokens?: number;
}

interface QueryResponse {
    answer: string;
    sources: Array<{
        content: string;
        metadata: Record<string, any>;
    }>;
    backend_used?: string;
    processing_time?: number;
}

class AIdiotClient {
    constructor(private baseUrl: string = 'http://localhost:8000') {}

    async query(request: QueryRequest): Promise<QueryResponse> {
        const response = await fetch(`${this.baseUrl}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request)
        });
        return response.json();
    }

    async uploadDocument(file: File, metadata?: Record<string, any>) {
        const formData = new FormData();
        formData.append('file', file);
        if (metadata) {
            formData.append('metadata', JSON.stringify(metadata));
        }
        
        const response = await fetch(`${this.baseUrl}/documents/upload`, {
            method: 'POST',
            body: formData
        });
        return response.json();
    }

    async getStats() {
        const response = await fetch(`${this.baseUrl}/stats`);
        return response.json();
    }
}

// Usage example
const client = new AIdiotClient();

(async () => {
    try {
        const result = await client.query({
            question: "Explain impedance matching in antenna systems",
            include_sources: true,
            backend: "auto"
        });
        
        console.log(`Answer: ${result.answer}`);
        console.log(`Sources: ${result.sources.length}`);
        console.log(`Backend: ${result.backend_used}`);
    } catch (error) {
        console.error('Query failed:', error);
    }
})();
```

### HTML Web Interface

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>AIdiot Web Interface</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .chat-container { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin: 10px 0; }
        .message { margin: 10px 0; }
        .user { color: blue; }
        .ai { color: green; }
        input[type="text"] { width: 70%; padding: 5px; }
        button { padding: 5px 10px; }
    </style>
</head>
<body>
    <h1>🚀 AIdiot - Technical AI Assistant</h1>
    
    <div class="chat-container" id="chatContainer"></div>
    
    <div>
        <input type="text" id="questionInput" placeholder="Ask your technical question...">
        <button onclick="askQuestion()">Ask</button>
    </div>
    
    <div style="margin-top: 20px;">
        <input type="file" id="fileInput" accept=".pdf,.png,.jpg,.jpeg">
        <button onclick="uploadFile()">Upload Document</button>
    </div>

    <script>
        const API_BASE = 'http://localhost:8000';
        
        async function askQuestion() {
            const question = document.getElementById('questionInput').value;
            if (!question) return;
            
            addMessage(`You: ${question}`, 'user');
            document.getElementById('questionInput').value = '';
            
            try {
                const response = await fetch(`${API_BASE}/query`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        question: question,
                        include_sources: true 
                    })
                });
                
                const data = await response.json();
                addMessage(`AI: ${data.answer}`, 'ai');
                
                if (data.sources && data.sources.length > 0) {
                    const sources = data.sources.map(s => s.metadata.filename || 'web').join(', ');
                    addMessage(`Sources: ${sources}`, 'sources');
                }
            } catch (error) {
                addMessage(`Error: ${error.message}`, 'error');
            }
        }
        
        async function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            if (!file) return;
            
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch(`${API_BASE}/documents/upload`, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                addMessage(`Upload: ${data.message}`, 'system');
                fileInput.value = '';
            } catch (error) {
                addMessage(`Upload Error: ${error.message}`, 'error');
            }
        }
        
        function addMessage(text, className) {
            const container = document.getElementById('chatContainer');
            const message = document.createElement('div');
            message.className = `message ${className}`;
            message.textContent = text;
            container.appendChild(message);
            container.scrollTop = container.scrollHeight;
        }
        
        // Allow Enter key to ask questions
        document.getElementById('questionInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askQuestion();
            }
        });
        
        // Check system health on load
        fetch(`${API_BASE}/health`)
            .then(response => response.json())
            .then(data => {
                const status = data.overall_healthy ? 'System ready!' : 'System issues detected';
                addMessage(`🚀 ${status}`, 'system');
            })
            .catch(error => {
                addMessage('❌ Cannot connect to API server. Start with: python main.py serve', 'error');
            });
    </script>
</body>
</html>
```

## 5. Advanced Usage Patterns

### Batch Processing Documents

```bash
# Process all PDFs in multiple directories
python main.py add-documents ./manuals/arrl/
python main.py add-documents ./manuals/manufacturers/
python main.py add-documents ./research_papers/

# Process images from various sources
python main.py add-documents ./data/images/diagrams/
python main.py add-documents ./data/images/circuits/
python main.py add-documents ./data/images/references/

# Add multiple URLs (create a script)
# add_urls.sh:
python main.py add-documents --url "https://www.arrl.org/antenna-basics"
python main.py add-documents --url "https://www.arrl.org/impedance-matching"
python main.py add-documents --url "https://www.arrl.org/smith-chart"
python main.py add-documents --url "https://www.arrl.org/rf-design"
```

### Specialized Question Examples

```bash
# Antenna Design Questions
python main.py query "Calculate the dimensions for a 3-element Yagi antenna for 146 MHz"
python main.py query "What is the radiation resistance of a quarter-wave monopole?"
python main.py query "How do I design a log-periodic dipole array for 2-30 MHz?"

# Filter Design Questions  
python main.py query "Design a 7th order Chebyshev low-pass filter for 30 MHz with 1dB ripple"
python main.py query "What component values do I need for a pi-network impedance matcher?"
python main.py query "How do I calculate insertion loss of a bandpass filter?"

# Circuit Analysis Questions
python main.py query "Analyze the stability of this RF amplifier circuit" # (with image upload)
python main.py query "What is the gain and noise figure of a cascode amplifier?"
python main.py query "How do I calculate the conversion gain of a mixer circuit?"

# Practical Questions
python main.py query "My SWR is 3:1 on 20 meters. What could be wrong?"
python main.py query "How do I reduce harmonic distortion in a Class C amplifier?"
python main.py query "What transmission line should I use for 1296 MHz?"
```

### Knowledge Base Management

```bash
# Regular maintenance
python main.py stats          # Check current status
python main.py health        # Verify system health

# Backup and restore (manual process)
# The vector database is stored in ./data/vector_db/
# Back up this directory to preserve your knowledge base

# Clear and rebuild
python main.py clear-db      # Clear all documents
python main.py add-documents ./backup_docs/  # Rebuild from backup

# Performance monitoring
python main.py query "test query" --no-sources  # Fast query without sources
```

## 6. Integration Examples

### Flask Web Application

```python
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
AIDIOT_API = "http://localhost:8000"

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    response = requests.post(f"{AIDIOT_API}/query", json={
        "question": question,
        "include_sources": True
    })
    return jsonify(response.json())

@app.route('/api/upload', methods=['POST'])
def upload():
    file = request.files['file']
    files = {'file': (file.filename, file.stream, file.content_type)}
    response = requests.post(f"{AIDIOT_API}/documents/upload", files=files)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Discord Bot Integration

```python
import discord
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
AIDIOT_API = "http://localhost:8000"

@bot.command(name='ham')
async def ham_question(ctx, *, question):
    """Ask the technical AI assistant a question."""
    try:
        response = requests.post(f"{AIDIOT_API}/query", json={
            "question": question,
            "include_sources": False
        })
        data = response.json()
        
        # Discord has a 2000 character limit
        answer = data['answer']
        if len(answer) > 1900:
            answer = answer[:1900] + "... (truncated)"
        
        await ctx.send(f"🤖 **Answer:** {answer}")
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='hamstats')
async def ham_stats(ctx):
    """Get knowledge base statistics."""
    try:
        response = requests.get(f"{AIDIOT_API}/stats")
        data = response.json()
        
        embed = discord.Embed(title="📊 AIdiot Knowledge Base Stats", color=0x00ff00)
        embed.add_field(name="Total Documents", value=data['total_documents'])
        embed.add_field(name="Unique Sources", value=data['unique_sources'])
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

bot.run('YOUR_DISCORD_BOT_TOKEN')
```

## 7. Performance Tips

### Optimizing Query Performance

```bash
# Use specific technical terms for better results
python main.py query "Smith chart impedance transformation 50 ohm to 75 ohm"
# Better than: "how to match impedances"

# Include frequency information when relevant
python main.py query "VHF antenna design 144-148 MHz"
# Better than: "VHF antenna design"

# Be specific about component types
python main.py query "ceramic capacitor temperature coefficient C0G 1nF 50V"
# Better than: "capacitor specifications"
```

### System Performance

```bash
# Monitor system health regularly
python main.py health

# Check for optimal chunk count (aim for 100-10000 documents)
python main.py stats

# Restart if memory usage becomes high
# Stop: Ctrl+C
# Restart: python main.py serve
```

## 🔧 **Error Handling and Troubleshooting Examples**

### Dependency Fallback Scenarios

```bash
# Scenario 1: Missing Poppler utilities
# Error: "Unable to get page count. Is poppler installed and in PATH?"
# Solution: System automatically uses PyMuPDF fallback

python main.py add-documents scanned_manual.pdf
# Output: "WARNING: pdf2image not available - using PyMuPDF fallback for PDF OCR"
# Result: Document processed successfully with slower but functional OCR

# Scenario 2: Missing OpenCV in headless environment  
# Error: libGL.so.1 errors in Docker/containers
# Solution: System uses opencv-python-headless and PIL fallback

python main.py add-documents circuit_diagram.png
# Output: "WARNING: OpenCV not available. Using basic PIL processing"
# Result: Image processed with PIL-based enhancement

# Scenario 3: LangChain deprecation warnings (FIXED!)
# Old errors: 
# - "LangChainDeprecationWarning: The class `Ollama` was deprecated"
# - "LangChainDeprecationWarning: The method `BaseLLM.__call__` was deprecated" 
# - "Argument `prompt` is expected to be a string. Instead found StringPromptValue"

# Solutions implemented:
# ✅ Updated to use langchain-ollama package 
# ✅ Replaced deprecated __call__() with modern invoke() methods
# ✅ Added smart PromptValue handling for LCEL chains

python main.py query "antenna theory"
# Output: Clean execution with ZERO deprecation warnings
# Result: Proper LCEL compatibility with modern LangChain patterns
```

### Testing Fallback Functionality

```bash
# Test PDF processing without Poppler
# Temporarily rename pdf2image to simulate missing Poppler
pip uninstall pdf2image
python main.py add-documents test_manual.pdf
# Should work with PyMuPDF fallback
pip install pdf2image  # Restore when done

# Test headless operation  
# Simulate headless environment
export DISPLAY=""
python main.py add-documents technical_diagram.png
# Should work with PIL-based processing

# Test LLM backend failover
LLM_BACKEND=invalid_backend python main.py query "test question"
# Should gracefully fall back to default backend
```

### Modern LangChain Usage Patterns

```bash
# Verify modern LangChain implementation
python -c "
# Test that all backends use modern invoke() methods
from src.llm_factory import OllamaBackend, OpenAIBackend, AnthropicBackend
print('✅ All backends support modern invoke() patterns')
print('✅ Smart PromptValue handling implemented')
print('✅ Zero deprecation warnings')
"

# Test LCEL chain compatibility
python main.py query "How does LCEL improve performance?"
# Should execute without any LangChain warnings or errors

# Check for deprecated patterns (should find none)
grep -r "__call__" src/ || echo "✅ No deprecated __call__ patterns found"
grep -r "LangChainDeprecationWarning" src/ || echo "✅ No deprecation warnings in code"
```

### Performance Optimization Examples

```bash
# Check what processing methods are available
python -c "
from src.document_processor import CV2_AVAILABLE, PDF2IMAGE_AVAILABLE
print(f'OpenCV available: {CV2_AVAILABLE}')
print(f'pdf2image available: {PDF2IMAGE_AVAILABLE}')
print('Optimal setup:' if (CV2_AVAILABLE and PDF2IMAGE_AVAILABLE) else 'Fallback mode:')
"

# Optimize for batch processing
# Process multiple documents efficiently
python main.py add-documents ./large_document_set/ --batch-size 10

# Monitor processing performance
time python main.py add-documents complex_schematic.pdf
# Compare performance with/without optimal dependencies
```

This comprehensive set of examples should help users get the most out of the AIdiot Technical AI Assistant!