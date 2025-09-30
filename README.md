# AIdiot - AI Assistant

A standalone AI solution for technical design and analysis using RAG (Retrieval-Augmented Generation). This system can process PDF files, image-based PDFs, technical diagrams, and web content to provide intelligent assistance for technical projects.

## Features

🚀 **Core Capabilities:**
- **Multi-format Document Processing**: PDF files, image-based PDFs, technical diagrams (PNG, JPG, TIFF)
- **Smart OCR Technology**: Extract text and component values from technical diagrams with automatic fallbacks
- **Robust PDF Processing**: Automatic Poppler fallback using PyMuPDF when Poppler unavailable
- **Headless-Ready**: OpenCV-free operation for containerized/server deployments
- **Web Content Integration**: Process technical articles and documentation from URLs
- **Configurable Domain Knowledge**: Optimized for technical terminology and concepts (customizable)
- **Dual Interface**: Command-line tool and REST API for web applications

🧠 **AI-Powered Analysis:**
- **Multi-Backend LLM Support**: Choose from local (Ollama via langchain-ollama, LocalAI) or cloud (OpenAI, Anthropic) models
- **Modern Architecture**: Built with LangChain v0.1+ using LCEL and modular packages (langchain-community, langchain-openai, langchain-anthropic, langchain-ollama)
- **Automatic Fallback**: Seamlessly switches between primary and backup LLM services
- **Error Recovery**: Graceful handling of missing dependencies with functional fallbacks
- **Technical Focus**: Specialized prompts for technical design and analysis (configurable)
- **Source Attribution**: Shows which documents contributed to each answer

🔧 **Technical Specialization (Configurable):**
- Circuit design and analysis
- Component calculations and filter design
- Technical calculations and theory
- Component value extraction from diagrams
- Standards, regulations, and best practices
- Specialized techniques and methodologies

## Requirements

- **Python 3.9-3.12** - [Download from python.org](https://python.org)
- **Ollama** (for local LLM) - [Install from ollama.ai](https://ollama.ai)
- **Tesseract OCR** (optional) - [Download for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- **Poppler utilities** (optional, recommended) - Improves PDF OCR performance

### Dependency Management ✅
All dependencies have graceful fallbacks:
- **OpenCV**: Uses headless version (opencv-python-headless) to avoid GUI dependencies
- **Poppler**: Automatic PyMuPDF fallback when Poppler unavailable
- **Tesseract**: Graceful degradation when OCR unavailable
- **LangChain**: Modern modular architecture with langchain-ollama, langchain-openai, etc.

### Python 3.12 Support ✅
This application has been fully tested and optimized for Python 3.12, including updated LangChain dependencies and modern async patterns.

## Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AIdiot
   ```

2. **Run setup script:**
   ```powershell
   # Windows PowerShell
   .\setup.ps1
   ```
   ```bash
   # Linux/Mac
   ./setup.sh
   ```

3. **Or install manually:**
   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   
   # Activate virtual environment
   venv\Scripts\activate     # Windows
   source venv/bin/activate  # Linux/Mac
   
   # Install dependencies (includes modern LangChain packages)
   pip install -r requirements.txt
   
   # Install and start Ollama
   ollama pull mistral:7b
   
   # Initialize system
   python main.py setup
   ```

### LangChain Modernization 🆕
This version uses the latest LangChain architecture with:
- **Modular packages**: `langchain-community`, `langchain-openai`, `langchain-anthropic`, `langchain-ollama`, `langchain-chroma`, `langchain-huggingface`
- **LangChain Expression Language (LCEL)**: Efficient chain composition and execution with proper prompt handling
- **Modern invoke() methods**: Updated from deprecated `__call__()` to modern `invoke()` across all backends
- **PromptValue compatibility**: Smart handling of LCEL StringPromptValue objects
- **Deprecation-free**: Zero deprecation warnings with latest LangChain patterns
- **Full Python 3.12 compatibility**: Tested and optimized for latest Python

See [BACKEND_CONFIG.md](BACKEND_CONFIG.md) for detailed backend configuration.

### Backend Configuration

Choose your preferred LLM backend by setting environment variables or creating a `.env` file:

**Option 1: Local (Privacy-focused)**
```bash
# Default - Ollama with Mistral
export LLM_BACKEND=ollama
export OLLAMA_MODEL=mistral:7b
```

**Option 2: Cloud (Performance-focused)**
```bash
# OpenAI GPT
export LLM_BACKEND=openai
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL=gpt-4

# Or Anthropic Claude
export LLM_BACKEND=anthropic
export ANTHROPIC_API_KEY=your_key_here
export ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

**Option 3: Quick Setup**
```bash
# Run the multi-backend setup script
python setup_backends.py
```

See [BACKEND_CONFIG.md](BACKEND_CONFIG.md) for detailed configuration options and [AI_MODEL_ALTERNATIVES.md](AI_MODEL_ALTERNATIVES.md) for comparison of different models.

## Usage

### Command Line Interface

```bash
# System setup and health check
python main.py setup
python main.py health

# Add documents to knowledge base
python main.py add-documents ./technical_manuals/
python main.py add-documents reference_handbook.pdf
python main.py add-documents technical_diagram.png
python main.py add-documents --url https://example.com/technical-article

# Ask questions
python main.py query "How do I design a filter for this application?"
python main.py query "What's the calculation for this component?"
python main.py query "Calculate the required parameters for this design"

# Interactive chat mode
python main.py interactive

# Knowledge base management
python main.py stats      # Show statistics
python main.py clear-db   # Clear all documents

# Start web API server
python main.py serve
```

### Web API

Start the API server:
```bash
python main.py serve
```

The API will be available at `http://localhost:8000` with interactive documentation at `/docs`.

#### API Endpoints

- **POST /query** - Ask questions
- **POST /documents/upload** - Upload PDF or image files
- **POST /documents/url** - Add content from URLs
- **GET /stats** - Knowledge base statistics
- **GET /health** - System health check
- **GET /similar/{query}** - Find similar documents

#### Example API Usage

```python
import requests

# Ask a question
response = requests.post("http://localhost:8000/query", json={
    "question": "How do I calculate the required component values?",
    "include_sources": True
})

answer = response.json()
print(f"Answer: {answer['answer']}")
```

```javascript
// JavaScript example
fetch('http://localhost:8000/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        question: "What is the formula for this calculation?",
        include_sources: true
    })
})
.then(response => response.json())
.then(data => console.log(data.answer));
```

## Document Types Supported

### PDFs
- **Text PDFs**: Direct text extraction
- **Image-based PDFs**: OCR processing with enhancement
- **Technical manuals**, equipment documentation, research papers

### Technical Diagrams and Images
- **Formats**: PNG, JPG, JPEG, TIFF, BMP
- **Component Recognition**: Extracts technical component values and labels
- **Technical Annotations**: Measurements, specifications, ratings, parameters
- **Enhancement**: Automatic image processing for better OCR

### Web Content
- **Technical Articles**: Industry publications, technical websites
- **Documentation**: Equipment manuals, application notes
- **Forums**: Stack Exchange, technical discussions, Q&A sites

## Example Questions

AIdiot can help with questions like:

**Design Calculations:**
- "Calculate the required component values for this application"
- "How do I design a system for these specifications?"
- "What's the optimal configuration for this design?"

**Circuit Analysis:**
- "Design a filter for this frequency range"
- "How do I calculate matching networks?"
- "What's the formula for this resonant circuit?"

**Practical Applications:**
- "How do I optimize performance in this system?"
- "What components do I need for this design?"
- "How do I implement this technical solution?"

**Technical Analysis:**
- "Analyze this technical diagram" (with image upload)
- "What are the component values in this circuit?"
- "Explain the operation of this system"

## Configuration

Copy `.env.example` to `.env` and customize:

```env
# LLM Configuration
OLLAMA_MODEL=mistral:7b
OLLAMA_BASE_URL=http://localhost:11434

# RAG Configuration  
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=all-MiniLM-L6-v2

# OCR Configuration
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
DPI=300

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
```

## Project Structure

```
AIdiot/
├── main.py              # Main entry point
├── requirements.txt     # Python dependencies
├── setup.ps1           # Windows setup script
├── .env.example        # Configuration template
├── data/               # Data directory
│   ├── pdfs/          # Place PDF files here
│   ├── images/        # Place technical images here
│   ├── vector_db/     # ChromaDB storage
│   └── sample_urls.txt # Example URLs
└── src/               # Source code
    ├── __init__.py
    ├── config.py      # Configuration management
    ├── document_processor.py # Document processing
    ├── rag_system.py  # RAG implementation
    ├── cli.py         # Command line interface
    └── api.py         # Web API
```

## Technical Details

### RAG Architecture
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB for persistent storage
- **Retrieval**: Maximal Marginal Relevance (MMR) for diverse results
- **LLM Backends**: Multi-backend support with automatic fallback
  - **Local**: Ollama (Mistral, CodeLlama), LocalAI, text-generation-webui
  - **Cloud**: OpenAI GPT, Anthropic Claude, Google PaLM
  - **Hybrid**: Primary + fallback configuration for reliability
- **Chunking**: Recursive character splitting with overlap

### Document Processing Pipeline
1. **PDF Processing**: PyMuPDF for text extraction, OCR fallback for images
2. **Image Enhancement**: OpenCV preprocessing for better OCR accuracy
3. **Component Extraction**: Regex patterns for electronic component values
4. **Relevance Filtering**: Domain-configurable topic classification
5. **Chunking and Embedding**: Optimized for technical content retrieval

### Specialized Features
- **Domain-Configurable Prompts**: Tailored for specific technical domains
- **Component Recognition**: Extracts technical values from diagrams
- **Technical Accuracy**: Low temperature setting for precise calculations
- **Source Attribution**: Tracks document sources for verification

## Troubleshooting

### Common Issues

**Ollama Connection Failed:**
- Ensure Ollama is installed and running
- Check if `ollama serve` is active
- Verify model is pulled: `ollama pull mistral:7b`

**OCR Not Working:**
- Install Tesseract OCR for Windows
- Update `TESSERACT_PATH` in config
- Check image quality and format

**Import Errors:**
- Activate virtual environment
- Install all requirements: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

**No Documents Found:**
- Check file formats (PDF, PNG, JPG supported)
- Verify files are in correct directories
- Check file permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[License details to be added]

## Acknowledgments

- **Ollama Team** for the excellent local LLM platform
- **LangChain** for RAG framework
- **Open Source Community** for technical resources and knowledge sharing
- **Technical Communities** for continuous learning and collaboration

---

� Happy building with AIdiot - Your AI companion for technical design and analysis!
