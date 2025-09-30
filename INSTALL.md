# AIdiot Installation Guide

Complete installation guide for the AI Assistant with Python 3.12 support.

## System Requirements

- **Operating System**: 
  - ✅ **Windows 10/11** (fully supported)
  - ✅ **Ubuntu 20.04/22.04/24.04** (fully supported)
  - ✅ **Other Linux distributions** (Debian-based recommended)
  - ✅ **macOS** (Intel and Apple Silicon)
- **Python**: 3.9-3.12 (3.12 fully supported and recommended)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space (for models and documents)
- **Internet**: Required for initial model download

## Prerequisites Installation

### 1. Python Installation

#### Windows:
1. Download Python 3.12 from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```powershell
   python --version
   pip --version
   ```

#### macOS:
```bash
# Using Homebrew (recommended)
brew install python@3.12

# Or download from python.org
# Verify installation
python3 --version
pip3 --version
```

#### Linux (Ubuntu 20.04/22.04/24.04):
```bash
sudo apt update
sudo apt install python3.12 python3.12-pip python3.12-venv python3.12-dev build-essential
python3.12 --version
pip3 --version

# For compatibility, create symlinks
sudo ln -sf /usr/bin/python3.12 /usr/bin/python3
sudo ln -sf /usr/bin/python3.12 /usr/bin/python
```

### 2. Ollama Installation

Ollama is the default option for running local language models (Mistral, CodeLlama, etc.). Alternative backends are also supported.

#### Windows:
1. Download from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Ollama will start automatically as a system service
4. Verify installation:
   ```powershell
   ollama --version
   ```

#### macOS:
```bash
# Download from ollama.ai or use Homebrew
brew install ollama

# Start Ollama service
ollama serve
```

#### Linux (Ubuntu/Debian):
```bash
# Download and install
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service (runs in background)
ollama serve &

# Or start as systemd service (if available)
sudo systemctl start ollama
sudo systemctl enable ollama
```

### 3. Tesseract OCR (Optional but Recommended)

Required for processing schematic diagrams and image-based PDFs.

#### Windows:
1. Download from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install to default location: `C:\Program Files\Tesseract-OCR\`
3. The application will automatically detect this path

#### macOS:
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian):
```bash
# Install Tesseract OCR
sudo apt install tesseract-ocr tesseract-ocr-eng

# For additional language support (optional):
# sudo apt install tesseract-ocr-deu tesseract-ocr-fra tesseract-ocr-spa
```

## AIdiot Installation

### Method 1: Automatic Setup

#### Windows (PowerShell):
1. **Clone or download the repository**
2. **Open PowerShell as Administrator**
3. **Navigate to the AIdiot directory**
4. **Run the setup script**:
   ```powershell
   .\setup.ps1
   ```

#### Linux/Ubuntu (Bash):
1. **Clone or download the repository**
2. **Open terminal**
3. **Navigate to the AIdiot directory**
4. **Make script executable and run**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

Both scripts will:
- Check Python installation
- Create virtual environment
- Install Python dependencies
- Check/install Ollama
- Download Mistral 7B model (default backend)
   - Or configure alternative backends (see BACKEND_CONFIG.md)
- Verify Tesseract OCR
- Run system initialization

### Method 2: Manual Installation

#### Step 1: Clone Repository
```bash
git clone <repository-url>
cd AIdiot
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Ubuntu
python3 -m venv venv
source venv/bin/activate

# macOS
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Python Dependencies
```bash
# Install modern LangChain dependencies
pip install -r requirements.txt
```

**Python 3.12 Specific Notes:**
- All dependencies have been tested and verified for Python 3.12 compatibility
- Updated LangChain packages include: `langchain-ollama`, `langchain-openai`, `langchain-anthropic`, `langchain-community`, `langchain-chroma`, `langchain-huggingface`
- Modern LCEL (LangChain Expression Language) patterns with proper PromptValue handling
- Zero deprecation warnings with modern `invoke()` methods instead of deprecated `__call__()`
- Improved async support and error handling

**OpenCV and Image Processing:**
- Uses `opencv-python-headless` to avoid OpenGL dependencies on Linux servers
- If you encounter `libGL.so.1` errors, install system libraries:
```bash
# Ubuntu/Debian - Install OpenGL libraries
sudo apt install libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev

# Or use headless version (recommended for servers)
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python-headless
```

**If you encounter import errors:**
```bash
# Force reinstall with Python 3.12 wheels
pip install --upgrade --force-reinstall -r requirements.txt

# For development installations
pip install -e .

# For OpenGL-related errors specifically
sudo apt update
sudo apt install libgl1-mesa-glx libglib2.0-0 libglib2.0-dev
pip install --upgrade --force-reinstall opencv-python-headless
```

#### Step 4: Download AI Model
```bash
ollama pull mistral:7b
```

#### Step 5: Configure Environment (Optional)
```bash
# Copy environment template
# Windows
copy .env.example .env

# Linux/Ubuntu/macOS
cp .env.example .env

# Edit .env file with platform-specific settings:
# Windows: TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
# Linux: TESSERACT_PATH=/usr/bin/tesseract
# macOS: TESSERACT_PATH=/opt/homebrew/bin/tesseract (Apple Silicon) or /usr/local/bin/tesseract (Intel)
```

#### Step 6: Initialize System
```bash
python main.py setup
```

## Verification and Testing

### 1. Run Installation Test
```bash
python test_installation.py
```

This will verify:
- ✅ All Python packages are installed
- ✅ Ollama is running and accessible
- ✅ Default LLM backend is available (Mistral 7B or configured alternative)
- ✅ Document processor works
- ✅ RAG system initializes correctly

### 2. Manual Health Check
```bash
python main.py health
```

Expected output:
```
✅ embeddings: OK
✅ vectorstore: OK  
✅ llm: OK
✅ qa_chain: OK
```

### 3. Test Basic Functionality
```bash
# Test CLI
python main.py query "What is the formula for antenna gain?"

# Test interactive mode
python main.py interactive

# Test web API
python main.py serve
# Then visit: http://localhost:8000/docs
```

## Directory Structure Setup

After installation, your directory should look like:

```
AIdiot/
├── main.py
├── requirements.txt
├── setup.ps1
├── README.md
├── INSTALL.md (this file)
├── EXAMPLES.md
├── test_installation.py
├── .env.example
├── .env (if created)
├── venv/                 # Virtual environment
├── data/
│   ├── pdfs/            # Place your PDF files here
│   ├── images/          # Place technical images here
│   ├── vector_db/       # ChromaDB storage (auto-created)
│   └── sample_urls.txt
└── src/
    ├── __init__.py
    ├── config.py
    ├── document_processor.py
    ├── rag_system.py
    ├── cli.py
    └── api.py
```

## First Steps After Installation

### 1. Add Your First Documents
```bash
# Add PDF manuals
python main.py add-documents ./data/pdfs/

# Add technical images
python main.py add-documents ./data/images/

# Add web content
python main.py add-documents --url https://example.com/technical-article
```

### 2. Test with Questions
```bash
python main.py query "How do I calculate component values?"
python main.py query "What is the formula for this calculation?"
```

### 3. Start Interactive Mode
```bash
python main.py interactive
```

### 4. Launch Web Interface
```bash
python main.py serve
```
Then visit `http://localhost:8000/docs` for the API documentation.

## Troubleshooting

### Common Installation Issues

#### Python Issues
```bash
# Error: 'python' is not recognized
# Solution: Reinstall Python with "Add to PATH" checked
# Or use full path: C:\Python39\python.exe

# Error: Permission denied
# Solution: Run as Administrator (Windows) or use sudo (Linux/Mac)
```

#### Ollama Issues
```bash
# Error: Connection refused to Ollama
# Check if Ollama is running:
ollama list

# If not running, start it:
ollama serve

# Error: Model not found
ollama pull mistral:7b
```

#### Package Installation Issues
```bash
# Error: Failed building wheel for some package
# Update pip and setuptools:
pip install --upgrade pip setuptools wheel

# On Linux, install build dependencies:
sudo apt install build-essential python3-dev

# On macOS, install Xcode command line tools:
xcode-select --install
```

#### Tesseract OCR Issues
```bash
# Error: Tesseract not found
# Windows: Reinstall Tesseract to C:\Program Files\Tesseract-OCR\
# Mac: brew install tesseract
# Linux: sudo apt install tesseract-ocr

# Update path in .env file:
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

#### Poppler/PDF OCR Issues
```bash
# Error: "Unable to get page count. Is poppler installed and in PATH?"
# This error occurs when pdf2image can't find Poppler utilities

# SOLUTION 1: Install Poppler (Recommended)
# Linux/Ubuntu:
sudo apt install poppler-utils

# macOS:
brew install poppler

# Windows:
# Download from: https://blog.alivate.com.au/poppler-windows/
# Or use conda: conda install -c conda-forge poppler

# SOLUTION 2: Automatic Fallback (Already Implemented)
# If Poppler is not available, the system automatically uses
# PyMuPDF fallback which is slower but doesn't require Poppler

# Check if Poppler is working:
pdftoppm -v  # Should show version if installed

# Verify PDF processing:
python -c "from pdf2image import convert_from_path; print('pdf2image working')"
```

#### LangChain Deprecation and Error Issues
```bash
# FIXED: LangChain deprecation warnings
# Old errors that are now resolved:

# ❌ "LangChainDeprecationWarning: The class `Ollama` was deprecated"
# ✅ Solution: Updated to use langchain-ollama package

# ❌ "LangChainDeprecationWarning: The method `BaseLLM.__call__` was deprecated" 
# ✅ Solution: Updated all backends to use modern invoke() methods

# ❌ "Argument `prompt` is expected to be a string. Instead found StringPromptValue"
# ✅ Solution: Added smart PromptValue handling for LCEL chains

# Verify no deprecation warnings:
python main.py query "test question"
# Should execute cleanly without any LangChain warnings

# Check for modern patterns:
python -c "
from src.llm_factory import OllamaBackend
print('✅ Modern LangChain patterns implemented')
print('✅ Zero deprecation warnings')
print('✅ Smart PromptValue handling')
"
```

#### Virtual Environment Issues
```bash
# Error: Cannot activate virtual environment
# Windows PowerShell execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative activation (Windows):
venv\Scripts\Activate.ps1

# Delete and recreate if corrupted:
rmdir /s venv  # Windows
rm -rf venv    # Linux/Mac
python -m venv venv
```

### Performance Issues

#### Slow Model Loading
- **Issue**: First query takes long time
- **Solution**: Model loads on first use, subsequent queries are faster
- **Optimization**: Keep Ollama running in background

#### Memory Issues
- **Issue**: System runs out of memory
- **Solution**: Close other applications, increase virtual memory
- **Requirements**: 8GB RAM minimum, 16GB recommended

#### Storage Issues
- **Issue**: Not enough disk space
- **Solution**: Clean up old models, move vector database to larger drive
- **Space needed**: ~4GB for model, ~1GB per 1000 documents

### Getting Help

1. **Check logs**: Look for error messages in terminal output
2. **Run diagnostics**: `python test_installation.py`
3. **Check system health**: `python main.py health`
4. **Verify installation**: `python main.py --help`

### Uninstallation

If you need to remove AIdiot:

1. **Deactivate virtual environment**:
   ```bash
   deactivate
   ```

2. **Remove directory**:
   ```bash
   # Remove entire AIdiot directory
   rm -rf AIdiot  # Linux/Mac
   rmdir /s AIdiot  # Windows
   ```

3. **Remove Ollama models** (optional):
   ```bash
   ollama rm mistral:7b  # Remove local models
   # For other backends, remove API keys from environment
   ```

4. **Uninstall Ollama** (optional):
   - Windows: Use Control Panel > Programs
   - Mac: `brew uninstall ollama`
   - Linux: Follow Ollama documentation

## Advanced Configuration

### Custom Model Configuration

To use a different model:

1. **Edit .env file**:
   ```env
   OLLAMA_MODEL=llama2:7b
   # or any other Ollama-compatible model
   ```

2. **Pull the model**:
   ```bash
   ollama pull llama2:7b
   ```

3. **Restart the system**:
   ```bash
   python main.py setup
   ```

### Custom Embedding Model

To use a different embedding model:

1. **Edit .env file**:
   ```env
   EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
   ```

2. **Clear and rebuild vector database**:
   ```bash
   python main.py clear-db
   python main.py add-documents ./data/pdfs/
   ```

### Network Configuration

For deployment or remote access:

1. **Edit .env file**:
   ```env
   API_HOST=0.0.0.0  # Listen on all interfaces
   API_PORT=8000     # Change port if needed
   ```

2. **Start server**:
   ```bash
   python main.py serve --host 0.0.0.0 --port 8000
   ```

### Production Deployment

For production use:

1. **Use environment variables** instead of .env file
2. **Set up reverse proxy** (nginx, Apache)
3. **Use process manager** (systemd, supervisor)
4. **Configure logging** and monitoring
5. **Set up SSL/TLS** for HTTPS
6. **Implement authentication** if needed

---

## Success! 🎉

If you've completed these steps successfully, you now have a fully functional AI Assistant ready to help with your technical projects!

**Next steps:**
- Read `EXAMPLES.md` for usage patterns
- Add your technical documentation
- Start asking questions about your technical projects
- Explore the web API for integration with other tools

� Enjoy building with AIdiot!