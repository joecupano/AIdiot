# Cross-Platform Compatibility Guide

AIdiot AI Assistant is fully cross-platform with Python 3.12 support and modern LangChain architecture.

## ✅ **Confirmed Compatibility**

### Operating Systems & Python Versions
- **Windows 10/11** - Full native support with Python 3.9-3.12
- **Ubuntu 20.04/22.04/24.04** - Full native support with Python 3.9-3.12
- **Other Linux distributions** - Debian-based recommended
- **macOS** - Intel and Apple Silicon support with Python 3.9-3.12

### Python 3.12 Specific Support ✨
- **LangChain v0.1+**: Full compatibility with modular packages
- **Modern Dependencies**: All packages tested with Python 3.12
- **Async Improvements**: Better async/await support across platforms
- **Performance**: Enhanced performance with Python 3.12 optimizations

### Installation Methods

| Platform | Python 3.12 Setup | Command | Backend Setup |
|----------|-------------------|---------|---------------|
| **Windows 11** | `python --version` | `.\setup.ps1` | `python setup_backends.py` |
| **Ubuntu 24.04** | `python3.12 --version` | `./setup.sh` | `python setup_backends.py` |
| **macOS** | `brew install python@3.12` | See INSTALL.md | `python setup_backends.py` |
| **Other Linux** | Package manager | See INSTALL.md | `python setup_backends.py` |

## 🔧 **Platform-Specific Features**

### Modern LangChain Integration
- **Modular Packages**: `langchain-community`, `langchain-openai`, `langchain-anthropic`
- **LCEL Chains**: LangChain Expression Language works on all platforms
- **Backend Flexibility**: Easy switching between local and cloud LLMs
- **Error Handling**: Improved cross-platform error handling and fallbacks

### File Paths & Configuration
- **Automatic Detection**: Uses `pathlib` for cross-platform path handling
- **Tesseract OCR**: Auto-detects installation path on all platforms
- **Data Directories**: Consistent structure across platforms
- **Environment Variables**: `.env` file support for easy configuration

### LLM Backend Support by Platform
- **Local Backends**: Ollama, LocalAI, text-generation-webui (all platforms)
- **Cloud Backends**: OpenAI, Anthropic (platform-agnostic APIs)
- **Docker Support**: LocalAI and custom backends via Docker
- **Auto-Configuration**: Platform-specific setup scripts handle dependencies

### Command Examples

#### Windows 11 with Python 3.12
```powershell
# Check Python version
python --version  # Should show 3.12.x

# Setup with modern LangChain
.\setup.ps1

# Virtual environment
python -m venv venv
venv\Scripts\activate

# Install modern LangChain packages
pip install -r requirements.txt

# Run with updated architecture
python main.py setup
python main.py interactive
python main.py serve
```

#### Ubuntu 24.04 with Python 3.12
```bash
# Install Python 3.12 if needed
sudo apt update
sudo apt install python3.12 python3.12-pip python3.12-venv

# Setup with modern dependencies
chmod +x setup.sh
./setup.sh

# Virtual environment with Python 3.12
python3.12 -m venv venv
source venv/bin/activate

# Run application
python main.py setup
python main.py interactive  
python main.py serve
```

#### macOS with Python 3.12
```bash
# Install Python 3.12 via Homebrew
brew install python@3.12

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py setup
```

## 📋 **Installation Checklist**

### Windows 11 + Python 3.12
- [ ] Python 3.12 installed from python.org
- [ ] PowerShell execution policy allows scripts
- [ ] Ollama downloaded and installed
- [ ] Tesseract OCR (optional for diagram processing)
- [ ] Run `.\setup.ps1` for automatic setup
- [ ] Verify: `python -c "import langchain_community; print('OK')"`

### Ubuntu 24.04 + Python 3.12
- [ ] System packages updated (`sudo apt update`)
- [ ] Python 3.12 and pip installed
- [ ] Build tools installed (`build-essential`)
- [ ] Ollama installed via script
- [ ] Tesseract OCR (optional)
- [ ] Run `./setup.sh` for automatic setup
- [ ] Verify: `python -c "import langchain_community; print('OK')"`

### macOS + Python 3.12
- [ ] Homebrew installed
- [ ] Python 3.12 via Homebrew
- [ ] Xcode command line tools
- [ ] Ollama for macOS installed
- [ ] Tesseract via Homebrew (optional)
- [ ] Manual setup following INSTALL.md

## 🐛 **Platform-Specific Troubleshooting**

### Windows 11 + Python 3.12 Issues
```powershell
# PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Python 3.12 path issues
where python
python --version

# LangChain import issues
pip install --upgrade --force-reinstall langchain-community
pip install --upgrade --force-reinstall langchain-core
where ollama

# Virtual environment issues with Python 3.12
Remove-Item -Recurse -Force venv
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip setuptools wheel

# LangChain compatibility issues
pip install --upgrade langchain>=0.1.0
pip install --upgrade langchain-community>=0.0.25
```

### Ubuntu 24.04 + Python 3.12 Issues
```bash
# Missing Python 3.12 packages
sudo apt update
sudo apt install python3.12-dev python3.12-venv build-essential curl

# Install specific Python 3.12 packages
sudo apt install python3.12-distutils python3.12-lib2to3

# Permission issues
chmod +x setup.sh
sudo chown -R $USER:$USER ./

# Python 3.12 path issues
which python3.12
python3.12 --version
which pip3

# LangChain import errors with Python 3.12
python3.12 -m pip install --upgrade pip
python3.12 -m pip install --force-reinstall langchain-community
```

### macOS + Python 3.12 Issues
```bash
# Homebrew Python 3.12 issues
brew update
brew install python@3.12
brew link --force python@3.12

# Path issues
export PATH="/opt/homebrew/bin:$PATH"  # Apple Silicon
export PATH="/usr/local/bin:$PATH"     # Intel Mac

# LangChain compilation issues
xcode-select --install
pip install --upgrade setuptools wheel
```

### Common Cross-Platform Issues (Python 3.12)
```bash
# Modern Ollama installation
# Windows: Download latest from ollama.ai
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
# macOS: brew install ollama

# Virtual environment with Python 3.12
# Windows: python -m venv venv && venv\Scripts\activate
# Linux/Mac: python3.12 -m venv venv && source venv/bin/activate

# Port conflicts (API server)
# Change port in .env file: API_PORT=8001
# Or: python main.py serve --port 8001

# LangChain module resolution
python -c "import sys; print(sys.path)"
pip list | grep langchain

# OpenCV/OpenGL dependency issues (Linux)
# Error: libGL.so.1: cannot open shared object file
# Solution: Install OpenGL libraries OR use headless OpenCV
sudo apt install libgl1-mesa-glx libglib2.0-0
# Alternative: Already fixed with opencv-python-headless package
```

## 🚀 **Performance Comparison (Python 3.12)**

| Aspect | Windows 11 | Ubuntu 24.04 | macOS | Notes |
|--------|-----------|--------------|-------|-------|
| **Installation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Scripts handle complexity |
| **Python 3.12 Performance** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Linux/Mac native advantage |
| **LangChain Performance** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | LCEL chains optimized |
| **Memory Usage** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Unix systems more efficient |
| **Ollama Integration** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Equal support |
| **Development Experience** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Windows tooling improved |

## 🔄 **Migration Between Platforms**

### Data Portability with Modern Stack
Your AIdiot data is fully portable between platforms with the updated architecture:

```bash
# Backup your data (Python 3.12 compatible)
python main.py export --format json --output ./backup/
# Or: tar -czf aidiot-backup.tar.gz data/ .env

# Restore on new platform
python main.py import --source ./backup/
# Or: tar -xzf aidiot-backup.tar.gz

# Verify modern LangChain compatibility
python main.py health --verbose
tar -czf aidiot-backup.tar.gz data/

# Restore on new platform
tar -xzf aidiot-backup.tar.gz

# Rebuild virtual environment
python -m venv venv  # Windows
python3 -m venv venv  # Linux
```

### Configuration Transfer
```bash
# Copy your .env file between platforms
# Adjust paths as needed:

# Windows to Linux
TESSERACT_PATH=/usr/bin/tesseract

# Linux to Windows  
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

## 📊 **Testing Status**

### Automated Tests
- ✅ Installation test (`python test_installation.py`)
- ✅ Health check (`python main.py health`)
- ✅ Document processing tests
- ✅ API endpoint tests

### Manual Verification
- ✅ Windows 11 Pro - Full functionality confirmed
- ✅ Ubuntu 24.04 LTS - Full functionality confirmed
- ✅ PDF processing works on both
- ✅ Image OCR works on both
- ✅ Web API accessible on both
- ✅ CLI interface identical on both

## 🎯 **Recommended Platform**

**For Development:**
- **Ubuntu 24.04** - Slightly better performance, easier dependency management

**For Production:**
- **Ubuntu 24.04** - More stable, better resource efficiency

**For Desktop Use:**
- **Windows 11** - Familiar environment, excellent tools

**For Servers:**
- **Ubuntu 24.04** - Industry standard, reliable, cost-effective

## 💡 **Best Practices**

### Cross-Platform Development
1. **Always use virtual environments**
2. **Test on both platforms before deployment**
3. **Use relative paths in code**
4. **Document platform-specific requirements**
5. **Provide setup scripts for both platforms**

### Deployment Recommendations
```bash
# Development
git clone <repository>
cd AIdiot

# Windows
.\setup.ps1

# Linux
./setup.sh

# Both platforms
python main.py setup
python main.py add-documents ./data/pdfs/
python main.py interactive
```

---

**Conclusion:** AIdiot provides identical functionality and user experience across Windows 11 and Ubuntu 24.04, making it truly cross-platform ready! 🚀