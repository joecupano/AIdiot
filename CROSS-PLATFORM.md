# Cross-Platform Compatibility Guide

AIdiot AI Assistant is fully cross-platform and runs natively on Windows 11, Ubuntu 24.04, and other operating systems.

## ✅ **Confirmed Compatibility**

### Operating Systems
- **Windows 10/11** - Full native support
- **Ubuntu 20.04/22.04/24.04** - Full native support  
- **Other Linux distributions** - Debian-based recommended
- **macOS** - Intel and Apple Silicon support

### Installation Methods

| Platform | Setup Method | Command | Backend Setup |
|----------|-------------|---------|---------------|
| **Windows 11** | PowerShell Script | `.\setup.ps1` | `python setup_backends.py` |
| **Ubuntu 24.04** | Bash Script | `./setup.sh` | `python setup_backends.py` |
| **macOS** | Manual/Homebrew | See INSTALL.md | `python setup_backends.py` |
| **Other Linux** | Manual | See INSTALL.md | `python setup_backends.py` |

## 🔧 **Platform-Specific Features**

### File Paths
- **Automatic Detection**: Uses `pathlib` for cross-platform path handling
- **Tesseract OCR**: Auto-detects installation path on all platforms
- **Data Directories**: Consistent structure across platforms

### LLM Backend Support
- **Local Backends**: Ollama, LocalAI, text-generation-webui (all platforms)
- **Cloud Backends**: OpenAI, Anthropic (platform-agnostic APIs)
- **Auto-Configuration**: Platform-specific setup scripts handle dependencies

### Dependencies
All core dependencies are cross-platform:
- **Python 3.8+**: Available on all platforms
- **Ollama**: Native installers for Windows, Linux, macOS
- **LangChain**: Pure Python, platform-agnostic
- **ChromaDB**: Cross-platform vector database
- **FastAPI**: Web framework works everywhere

### Command Examples

#### Windows 11
```powershell
# Setup
.\setup.ps1

# Virtual environment
python -m venv venv
venv\Scripts\activate

# Run application
python main.py setup
python main.py interactive
python main.py serve
```

#### Ubuntu 24.04
```bash
# Setup
chmod +x setup.sh
./setup.sh

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Run application
python main.py setup
python main.py interactive
python main.py serve
```

## 📋 **Installation Checklist**

### Windows 11
- [ ] Python 3.8+ installed
- [ ] PowerShell execution policy allows scripts
- [ ] Ollama downloaded and installed
- [ ] Tesseract OCR (optional)
- [ ] Run `.\setup.ps1`

### Ubuntu 24.04
- [ ] System packages updated (`sudo apt update`)
- [ ] Python 3.8+ and pip installed
- [ ] Build tools installed (`build-essential`)
- [ ] Ollama installed via script
- [ ] Tesseract OCR (optional)
- [ ] Run `./setup.sh`

## 🐛 **Platform-Specific Troubleshooting**

### Windows 11 Issues
```powershell
# PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Path issues
where python
where ollama

# Virtual environment issues
Remove-Item -Recurse -Force venv
python -m venv venv
```

### Ubuntu 24.04 Issues
```bash
# Missing packages
sudo apt update
sudo apt install python3-dev build-essential curl

# Permission issues
chmod +x setup.sh
sudo chown -R $USER:$USER ./

# Python path issues
which python3
which pip3
```

### Common Cross-Platform Issues
```bash
# Ollama not found
# Windows: Reinstall from ollama.ai
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Virtual environment activation
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Port conflicts (API server)
# Change port in .env file: API_PORT=8001
```

## 🚀 **Performance Comparison**

| Aspect | Windows 11 | Ubuntu 24.04 | Notes |
|--------|-----------|--------------|-------|
| **Installation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Both excellent |
| **Performance** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Linux slight edge |
| **Memory Usage** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Linux more efficient |
| **Compatibility** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Equal support |
| **Ease of Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Windows script polished |

## 🔄 **Migration Between Platforms**

### Data Portability
Your AIdiot data is fully portable between platforms:

```bash
# Backup your data (works on both platforms)
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