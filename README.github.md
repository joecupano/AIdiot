# AIdiot - AI Assistant

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Ollama](https://img.shields.io/badge/Ollama-Mistral%207B-orange.svg)](https://ollama.ai)

A standalone AI solution for technical design and analysis using RAG (Retrieval-Augmented Generation). Process PDF files, image-based PDFs, technical diagrams, and web content to provide intelligent assistance for technical projects.

![AIdiot Demo](https://via.placeholder.com/800x400/2196F3/FFFFFF?text=AIdiot+AI+Assistant+Demo)

## 🚀 Quick Start

### Windows
```powershell
git clone https://github.com/yourusername/aidiot.git
cd aidiot
.\setup.ps1
python main.py interactive
```

### Linux/Ubuntu
```bash
git clone https://github.com/yourusername/aidiot.git
cd aidiot
chmod +x setup.sh
./setup.sh
python main.py interactive
```

## ✨ Features

- 🔧 **Multi-format Processing**: PDFs, images, web content
- 🤖 **Local AI**: Mistral 7B via Ollama (no cloud required)
- 🖼️ **OCR Technology**: Extract text from technical diagrams
- 🌐 **Dual Interface**: Command-line and REST API
- 📊 **RAG Architecture**: Accurate, source-attributed answers
- 🔄 **Cross-Platform**: Windows, Linux, macOS support

## 📖 Documentation

- [Installation Guide](INSTALL.md) - Complete setup instructions
- [Usage Examples](EXAMPLES.md) - Practical usage patterns
- [Cross-Platform Guide](CROSS-PLATFORM.md) - Platform-specific info
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when server running)

## 🛠️ Requirements

- Python 3.8+
- 8GB RAM (16GB recommended)
- 10GB free disk space
- [Ollama](https://ollama.ai) for AI model

## 📊 Usage Examples

```bash
# Add technical documents
python main.py add-documents ./technical_manuals/

# Ask questions
python main.py query "How do I calculate component values for this design?"

# Start web server
python main.py serve
```

## 🏗️ Architecture

```
AIdiot/
├── 📄 PDF Processing      → Extract text and metadata
├── 🖼️ Image OCR           → Technical diagram analysis  
├── 🌐 Web Scraping        → Online content integration
├── 🧠 RAG System          → Intelligent Q&A with sources
├── 💻 CLI Interface       → Interactive command-line tool
└── 🚀 REST API           → Web application integration
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
- [LangChain](https://langchain.com) for RAG framework
- [FastAPI](https://fastapi.tiangolo.com) for web API
- [Rich](https://rich.readthedocs.io) for beautiful CLI output

## 📈 Roadmap

- [ ] Additional AI models support
- [ ] Enhanced OCR for handwritten text
- [ ] Multi-language support
- [ ] Vector database optimization
- [ ] Cloud deployment guides
- [ ] Plugin system for custom processors

---

**Star ⭐ this repo if you find it useful!**