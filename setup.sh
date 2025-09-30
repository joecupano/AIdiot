#!/bin/bash

# AIdiot Setup Script for Ubuntu/Linux
# Run this script to set up the AI Assistant

echo "🚀 Setting up AIdiot - AI Assistant"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ This script should not be run as root${NC}"
   exit 1
fi

# Check Ubuntu version
echo -e "${YELLOW}Checking Ubuntu version...${NC}"
ubuntu_version=$(lsb_release -rs 2>/dev/null || echo "Unknown")
echo -e "${GREEN}✅ Ubuntu version: $ubuntu_version${NC}"

# Update package lists
echo -e "${YELLOW}Updating package lists...${NC}"
sudo apt update

# Check Python installation
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo -e "${GREEN}✅ Python found: $python_version${NC}"
else
    echo -e "${YELLOW}📥 Installing Python...${NC}"
    sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Python installed successfully${NC}"
    else
        echo -e "${RED}❌ Failed to install Python${NC}"
        exit 1
    fi
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 found${NC}"
else
    echo -e "${YELLOW}📥 Installing pip...${NC}"
    sudo apt install -y python3-pip
fi

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${RED}❌ Failed to create virtual environment${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip in virtual environment
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install system libraries for OpenCV (headless)
echo -e "${YELLOW}Installing system libraries for image processing...${NC}"
sudo apt install -y libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libglib2.0-dev

# Note: We use opencv-python-headless to avoid OpenGL dependencies
echo -e "${CYAN}📝 Note: Using OpenCV headless version to avoid OpenGL dependencies${NC}"

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
    echo -e "${GREEN}✅ OpenCV headless version installed (no GUI dependencies)${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    echo -e "${YELLOW}💡 If you encounter OpenGL errors, try:${NC}"
    echo -e "${YELLOW}   sudo apt install libgl1-mesa-glx libglib2.0-0${NC}"
    exit 1
fi

# Check for Ollama
echo -e "${YELLOW}Checking Ollama installation...${NC}"
if command -v ollama &> /dev/null; then
    ollama_version=$(ollama --version 2>&1)
    echo -e "${GREEN}✅ Ollama found: $ollama_version${NC}"
    
    # Check if Ollama service is running
    if pgrep -x "ollama" > /dev/null; then
        echo -e "${GREEN}✅ Ollama service is running${NC}"
    else
        echo -e "${YELLOW}⚠️  Starting Ollama service...${NC}"
        ollama serve &
        sleep 5
    fi
    
    # Check for Mistral model
    echo -e "${YELLOW}Checking for Mistral 7B model...${NC}"
    if ollama list 2>&1 | grep -q "mistral:7b"; then
        echo -e "${GREEN}✅ Mistral 7B model found${NC}"
    else
        echo -e "${YELLOW}📥 Downloading Mistral 7B model...${NC}"
        ollama pull mistral:7b
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Mistral 7B model downloaded${NC}"
        else
            echo -e "${RED}❌ Failed to download model${NC}"
        fi
    fi
else
    echo -e "${RED}❌ Ollama not found${NC}"
    echo -e "${YELLOW}📥 Installing Ollama...${NC}"
    curl -fsSL https://ollama.ai/install.sh | sh
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Ollama installed${NC}"
        echo -e "${YELLOW}Starting Ollama service...${NC}"
        ollama serve &
        sleep 5
        echo -e "${YELLOW}Downloading Mistral 7B model...${NC}"
        ollama pull mistral:7b
    else
        echo -e "${RED}❌ Failed to install Ollama${NC}"
        echo -e "${YELLOW}Please install manually from: https://ollama.ai${NC}"
    fi
fi

# Check for Tesseract (optional)
echo -e "${YELLOW}Checking Tesseract OCR...${NC}"
if command -v tesseract &> /dev/null; then
    tesseract_version=$(tesseract --version 2>&1 | head -1)
    echo -e "${GREEN}✅ Tesseract OCR found: $tesseract_version${NC}"
else
    echo -e "${YELLOW}⚠️  Tesseract OCR not found (optional for image processing)${NC}"
    echo -e "${YELLOW}Install with: sudo apt install tesseract-ocr${NC}"
    read -p "Install Tesseract now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt install -y tesseract-ocr
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Tesseract installed${NC}"
        else
            echo -e "${RED}❌ Failed to install Tesseract${NC}"
        fi
    fi
fi

# Check for additional useful packages
echo -e "${YELLOW}Installing additional system dependencies...${NC}"
sudo apt install -y curl wget git

# Create .env file from example
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo -e "${YELLOW}Creating .env file...${NC}"
        cp .env.example .env
        # Update Tesseract path for Linux
        sed -i 's|TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe|TESSERACT_PATH=/usr/bin/tesseract|' .env
        echo -e "${GREEN}✅ .env file created${NC}"
    fi
fi

# Run system setup
echo -e "${YELLOW}Running system setup...${NC}"
python main.py setup

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo -e "${NC}1. Activate virtual environment: ${YELLOW}source venv/bin/activate${NC}"
echo -e "${NC}2. Add some documents: ${YELLOW}python main.py add-documents ./data/pdfs/${NC}"
echo -e "${NC}3. Start interactive mode: ${YELLOW}python main.py interactive${NC}"
echo -e "${NC}4. Or start web API: ${YELLOW}python main.py serve${NC}"
echo ""
echo -e "${NC}For examples: ${YELLOW}python main.py examples${NC}"
echo -e "${NC}For help: ${YELLOW}python main.py --help${NC}"
echo ""
echo -e "${GREEN}🚀 Enjoy building with AIdiot!${NC}"