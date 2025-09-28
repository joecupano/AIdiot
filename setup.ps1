#!/bin/bash

# AIdiot Setup Script for Windows (PowerShell)
# Run this script to set up the Amateur Radio AI Assistant

Write-Host "🚀 Setting up AIdiot - AI Assistant" -ForegroundColor Green

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check for Ollama
Write-Host "Checking Ollama installation..." -ForegroundColor Yellow
$ollamaVersion = ollama --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Ollama found: $ollamaVersion" -ForegroundColor Green
    
    # Check for Mistral model
    Write-Host "Checking for Mistral 7B model..." -ForegroundColor Yellow
    $ollamaList = ollama list 2>&1
    if ($ollamaList -match "mistral:7b") {
        Write-Host "✅ Mistral 7B model found" -ForegroundColor Green
    } else {
        Write-Host "📥 Downloading Mistral 7B model..." -ForegroundColor Yellow
        ollama pull mistral:7b
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Mistral 7B model downloaded" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to download model" -ForegroundColor Red
        }
    }
} else {
    Write-Host "❌ Ollama not found" -ForegroundColor Red
    Write-Host "Please install Ollama from: https://ollama.ai" -ForegroundColor Yellow
    Write-Host "Then run: ollama pull mistral:7b" -ForegroundColor Yellow
}

# Check for Tesseract (optional)
Write-Host "Checking Tesseract OCR..." -ForegroundColor Yellow
$tesseractPath = "C:\Program Files\Tesseract-OCR\tesseract.exe"
if (Test-Path $tesseractPath) {
    Write-Host "✅ Tesseract OCR found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Tesseract OCR not found (optional for image processing)" -ForegroundColor Yellow
    Write-Host "Download from: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
}

# Run setup
Write-Host "Running system setup..." -ForegroundColor Yellow
python main.py setup

# Setup multi-backend support
Write-Host "Setting up multi-backend LLM support..." -ForegroundColor Yellow
python setup_backends.py

# Test the installation
Write-Host "Testing installation..." -ForegroundColor Yellow
python test_multibackend.py

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Backend Configuration:" -ForegroundColor Cyan
Write-Host "• Default: Ollama with Mistral 7B (local, private)" -ForegroundColor White
Write-Host "• Cloud Options: OpenAI GPT, Anthropic Claude (requires API keys)" -ForegroundColor White
Write-Host "• Configure in .env file or see BACKEND_CONFIG.md" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Add some documents: python main.py add-documents ./data/pdfs/" -ForegroundColor White
Write-Host "2. Start interactive mode: python main.py interactive" -ForegroundColor White
Write-Host "3. Or start web API: python main.py serve" -ForegroundColor White
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "• Examples: python main.py examples" -ForegroundColor White
Write-Host "• Help: python main.py --help" -ForegroundColor White
Write-Host "• Backend Config: BACKEND_CONFIG.md" -ForegroundColor White
Write-Host "• Model Alternatives: AI_MODEL_ALTERNATIVES.md" -ForegroundColor White