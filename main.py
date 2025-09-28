#!/usr/bin/env python3
"""
AIdiot - AI Assistant

A standalone AI solution for technical design using RAG (Retrieval-Augmented Generation)
with support for PDF files, image-based PDFs, technical diagrams, and web content.

Usage:
    python main.py [command] [options]

Commands:
    setup          - Initial setup and system check
    add-docs       - Add documents to knowledge base
    query          - Ask a question
    interactive    - Start interactive mode
    serve          - Start web API server
    stats          - Show knowledge base statistics
    health         - Check system health
    clear-db       - Clear knowledge base

Examples:
    python main.py setup
    python main.py add-docs ./rf_docs/
    python main.py query "How do I design a low-pass filter for 2 meters?"
    python main.py interactive
    python main.py serve
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import logging
import typer
from rich.console import Console

# Import our modules
try:
    from src.cli import app as cli_app
    from src.api import app as fastapi_app
    from src.config import API_HOST, API_PORT, LOG_LEVEL
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)

console = Console()

# Create main Typer app
main_app = typer.Typer(
    name="AIdiot",
    help="AI Assistant - Standalone AI solution for technical design",
    add_completion=False
)

# Add CLI commands from cli module
main_app.add_typer(cli_app, name="", help="CLI commands")


@main_app.command()
def serve(
    host: str = typer.Option(API_HOST, "--host", "-h", help="API server host"),
    port: int = typer.Option(API_PORT, "--port", "-p", help="API server port"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload for development")
):
    """Start the web API server."""
    try:
        import uvicorn
        
        console.print(f"🚀 Starting AIdiot API server on http://{host}:{port}")
        console.print("📖 API documentation available at http://{host}:{port}/docs")
        
        # Configure logging
        logging.basicConfig(level=getattr(logging, LOG_LEVEL))
        
        uvicorn.run(
            "src.api:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
        
    except ImportError:
        console.print("❌ uvicorn not found. Install with: pip install uvicorn")
    except KeyboardInterrupt:
        console.print("\n👋 Server stopped")
    except Exception as e:
        console.print(f"❌ Server error: {str(e)}")


@main_app.command()
def version():
    """Show version information."""
    from src import __version__, __description__
    
    console.print(f"""
AIdiot v{__version__}
{__description__}

Features:
• RAG-based AI assistant for technical domains
• Support for PDFs, images, and web content
• OCR for technical diagrams
• Configurable for different technical topics
• Command line and REST API interfaces
• Powered by Mistral 7B via Ollama
    """)


@main_app.command()
def examples():
    """Show usage examples."""
    console.print("""
🤖 AIdiot Usage Examples:

🔧 Setup:
   python main.py setup

📚 Add Documents:
   python main.py add-documents ./technical_manuals/
   python main.py add-documents reference_book.pdf
   python main.py add-documents diagram.png
   python main.py add-documents --url https://example.com/technical-article

❓ Ask Questions:
   python main.py query "How do I calculate the required component values?"
   python main.py query "What's the formula for this calculation?"
   python main.py query "Design a filter for this application"

💬 Interactive Mode:
   python main.py interactive

🌐 Web API:
   python main.py serve
   # Then use API at http://localhost:8000/docs

📊 System Info:
   python main.py stats
   python main.py health

🧹 Maintenance:
   python main.py clear-db
    """)


def main():
    """Main entry point."""
    try:
        # Check if we're being called with no arguments
        if len(sys.argv) == 1:
            console.print("""
🚀 AIdiot - AI Assistant

Run 'python main.py --help' for commands
Run 'python main.py examples' for usage examples
Run 'python main.py setup' to get started
            """)
            return
        
        main_app()
        
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!")
    except Exception as e:
        console.print(f"❌ Error: {str(e)}")
        logging.exception("Unhandled exception in main")


if __name__ == "__main__":
    main()