#!/usr/bin/env python3
"""
Quick setup script for multi-backend LLM support
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def install_optional_packages():
    """Install optional packages for different backends"""
    packages = {
        "openai": "OpenAI GPT support",
        "anthropic": "Anthropic Claude support", 
        "ollama": "Ollama local LLM support",
        "easyocr": "Enhanced OCR support"
    }
    
    print("Installing optional packages for multi-backend support...")
    
    for package, description in packages.items():
        success = run_command(f"pip install {package}", f"Installing {package} ({description})")
        if not success:
            print(f"⚠️  Optional package {package} failed to install - {description} won't be available")

def create_env_template():
    """Create environment template file"""
    env_content = """# AI Assistant Multi-Backend Configuration
# Choose one primary backend and configure its settings

# Primary backend (ollama, openai, anthropic, textgen, localai)
LLM_BACKEND=ollama

# Ollama Configuration (default/fallback)
OLLAMA_MODEL=mistral:7b
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TEMPERATURE=0.1

# OpenAI Configuration (uncomment if using)
# OPENAI_API_KEY=your_openai_key_here
# OPENAI_MODEL=gpt-3.5-turbo
# OPENAI_TEMPERATURE=0.1
# OPENAI_MAX_TOKENS=2000

# Anthropic Configuration (uncomment if using)
# ANTHROPIC_API_KEY=your_anthropic_key_here
# ANTHROPIC_MODEL=claude-3-haiku-20240307
# ANTHROPIC_TEMPERATURE=0.1
# ANTHROPIC_MAX_TOKENS=2000

# text-generation-webui Configuration (uncomment if using)
# TEXTGEN_BASE_URL=http://localhost:5000
# TEXTGEN_MODEL=your_model_name
# TEXTGEN_TEMPERATURE=0.1
# TEXTGEN_MAX_TOKENS=2000

# LocalAI Configuration (uncomment if using)
# LOCALAI_BASE_URL=http://localhost:8080
# LOCALAI_MODEL=gpt-3.5-turbo
# LOCALAI_TEMPERATURE=0.1

# Domain Configuration
DOMAIN_FOCUS=technical
VECTOR_DB_COLLECTION=technical_docs

# Other settings
DEBUG=false
LOG_LEVEL=INFO
"""
    
    env_file = Path(".env.example")
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created {env_file} - copy to .env and customize")

def check_backends():
    """Check which backends are available"""
    print("\n🔍 Checking backend availability...")
    
    try:
        from src.llm_factory import LLMFactory
        available = LLMFactory.get_available_backends()
        
        print("Backend Availability:")
        for backend, is_available in available.items():
            status = "✅ Available" if is_available else "❌ Not available"
            print(f"  {backend}: {status}")
            
        return available
    except Exception as e:
        print(f"❌ Could not check backends: {e}")
        return {}

def test_ollama_connection():
    """Test if Ollama is running"""
    print("\n🔗 Testing Ollama connection...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama is running")
            print(f"Available models: {[model['name'] for model in models.get('models', [])]}")
            return True
        else:
            print("❌ Ollama is running but returned error")
            return False
    except Exception as e:
        print("❌ Ollama is not running or not accessible")
        print("💡 Start Ollama with: ollama serve")
        print("💡 Install a model with: ollama pull mistral:7b")
        return False

def main():
    """Main setup function"""
    print("🚀 AI Assistant Multi-Backend Setup\n")
    
    # Install optional packages
    install_optional_packages()
    
    # Create environment template
    create_env_template()
    
    # Check backend availability
    available = check_backends()
    
    # Test Ollama (default backend)
    ollama_running = test_ollama_connection()
    
    # Provide next steps
    print("\n📋 Next Steps:")
    
    if not ollama_running:
        print("1. Install and start Ollama:")
        print("   - Download from: https://ollama.ai/")
        print("   - Run: ollama serve")
        print("   - Install model: ollama pull mistral:7b")
    
    print("2. Configure your backend:")
    print("   - Copy .env.example to .env")
    print("   - Set LLM_BACKEND to your preferred option")
    print("   - Add API keys if using cloud services")
    
    print("3. Test the system:")
    print("   - python main.py query \"What is a resistor?\"")
    print("   - python main.py serve --port 8000")
    
    print("\n📚 For detailed configuration instructions, see:")
    print("   - BACKEND_CONFIG.md")
    print("   - AI_MODEL_ALTERNATIVES.md")
    
    # Show recommended configuration based on availability
    print("\n💡 Recommended configuration based on your system:")
    
    if available.get('ollama', False) and ollama_running:
        print("✅ Ollama is ready - good for privacy and local development")
    elif available.get('openai', False):
        print("🌐 OpenAI is available - good for performance (requires API key)")
    elif available.get('anthropic', False):
        print("🌐 Anthropic is available - good for complex reasoning (requires API key)")
    else:
        print("⚠️  No backends are currently ready - check installation and configuration")

if __name__ == "__main__":
    main()