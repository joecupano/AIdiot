# AIdiot - AI Assistant

[![Python](https://img.shields.io/badge/python-3.9%2B%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-v0.1%2B-green.svg)](https://python.langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![LLM](https://img.shields.io/badge/LLM-Multi--Backend-blue.svg)](https://github.com/joecupano/AIdiot)

A standalone AI solution for technical design and analysis using modern RAG (Retrieval-Augmented Generation) architecture. Process PDF files, image-based PDFs, technical diagrams, and web content with **Python 3.12 support** and **modern LangChain v0.1+ integration**.

![AIdiot Demo](https://via.placeholder.com/800x400/2196F3/FFFFFF?text=AIdiot+AI+Assistant+%7C+Python+3.12+%7C+LangChain+v0.1%2B)

## 🆕 **What's New**
- ✅ **Python 3.12 Support** - Fully tested and optimized
- ✅ **Modern LangChain** - Uses v0.1+ with LCEL (LangChain Expression Language)
- ✅ **Modular Packages** - `langchain-community`, `langchain-openai`, `langchain-anthropic`
- ✅ **Enhanced Performance** - Improved RAG chains and async support
- ✅ **Better Error Handling** - Robust fallback mechanisms

## 🚀 Quick Start

### Windows (Python 3.12)
```powershell
# Clone repository
git clone https://github.com/yourusername/aidiot.git
cd aidiot

# Automated setup with Python 3.12 support
.\setup.ps1

# Start using the AI assistant
python main.py interactive
```

### Linux/Ubuntu (Python 3.12)
```bash
# Clone repository  
git clone https://github.com/yourusername/aidiot.git
cd aidiot

# Automated setup with modern dependencies
chmod +x setup.sh
./setup.sh

# Start using the AI assistant
python main.py interactive
```

### 🔧 Modern Backend Configuration
```bash
# Default: Local Ollama with modern LangChain integration
export LLM_BACKEND=ollama
export OLLAMA_MODEL=mistral:7b

# OpenAI with langchain-openai package
export LLM_BACKEND=openai
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL=gpt-4-turbo

# Anthropic with langchain-anthropic package  
export LLM_BACKEND=anthropic
export ANTHROPIC_API_KEY=your_key_here
export ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Quick multi-backend setup
python setup_backends.py
```

## ✨ Features

- 🔧 **Multi-format Processing**: PDFs, images, web content with enhanced OCR
- 🤖 **Modern Multi-Backend AI**: Updated integrations for all LLM providers
- 🖼️ **Advanced OCR**: Extract text and component values from technical diagrams  
- 🌐 **Dual Interface**: Enhanced CLI and REST API with Python 3.12 performance
- 📊 **Modern RAG Architecture**: LCEL-based chains for better performance
- 🔄 **Cross-Platform**: Full Python 3.12 support on Windows, Linux, macOS
- ⚡ **Enhanced Performance**: Async improvements and better error handling

## 📖 Documentation

- [Installation Guide](INSTALL.md) - Python 3.12 setup instructions
- [Usage Examples](EXAMPLES.md) - Updated usage patterns and API examples
- [Backend Configuration](BACKEND_CONFIG.md) - Modern LangChain backend setup
- [AI Model Alternatives](AI_MODEL_ALTERNATIVES.md) - 2024 model comparison with LangChain integration
- [Cross-Platform Guide](CROSS-PLATFORM.md) - Python 3.12 platform-specific info
- [LangChain Migration](LANGCHAIN_MIGRATION.md) - Technical details of the modernization
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when server running)

## 🛠️ Requirements

- **Python 3.9-3.12** (3.12 recommended and fully supported)
- **8GB RAM** (16GB recommended)
- **10GB free disk space**
- **[Ollama](https://ollama.ai)** for local AI models (recommended)
- **Modern LangChain packages** (installed automatically)

## 📊 Updated Usage Examples

```bash
# System setup with modern dependencies
python main.py setup

# Add technical documents with enhanced processing
python main.py add-documents ./technical_manuals/

# Ask questions with improved RAG system
python main.py query "How do I calculate component values for this design?"

# Start web server with Python 3.12 performance
python main.py serve --port 8000
```

## 🏗️ Modern Architecture

```
AIdiot (Python 3.12 + LangChain v0.1+)/
├── 📄 Enhanced PDF Processing    → Improved text extraction
├── 🖼️ Advanced Image OCR         → Better technical diagram analysis  
├── 🌐 Smart Web Scraping         → Enhanced content integration
├── 🧠 Modern RAG System          → LCEL-based chains for performance
├── 💻 Updated CLI Interface      → Python 3.12 optimized
├── 🚀 Enhanced REST API          → Async improvements
└── 🔧 Multi-Backend LLM Support  → Modular LangChain packages
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for local AI model hosting
- [OpenAI](https://openai.com) & [Anthropic](https://anthropic.com) for cloud AI services
- [LangChain](https://langchain.com) for RAG framework
- [FastAPI](https://fastapi.tiangolo.com) for web API
- [Rich](https://rich.readthedocs.io) for beautiful CLI output

## 📈 Roadmap

- [x] Multi-backend LLM support (Ollama, OpenAI, Anthropic, LocalAI)
- [x] Domain-agnostic architecture
- [ ] Enhanced OCR for handwritten text
- [ ] Multi-language support
- [ ] Vector database optimization
- [ ] Cloud deployment guides
- [ ] Plugin system for custom processors
- [ ] Model performance benchmarking tools

---

**Star ⭐ this repo if you find it useful!**