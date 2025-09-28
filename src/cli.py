#!/usr/bin/env python3

import logging
import sys
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
import json

from .document_processor import DocumentProcessor
from .rag_system import DomainRAG
from .config import PDF_DIR, IMAGES_DIR, LOG_LEVEL, LOG_FORMAT

# Setup logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Initialize Rich console
console = Console()

# Initialize Typer app
app = typer.Typer(
    name="AIdiot",
    help="AI Assistant - RAG system for technical design and analysis",
    add_completion=False
)

# Global instances
doc_processor = DocumentProcessor()
rag_system = None


def get_rag_system() -> DomainRAG:
    """Get or initialize the RAG system."""
    global rag_system
    if rag_system is None:
        with console.status("[bold green]Initializing RAG system..."):
            rag_system = DomainRAG()
    return rag_system


@app.command()
def setup():
    """Initial setup and system check."""
    console.print(Panel.fit("🚀 AIdiot - AI Assistant Setup"))
    
    # Check Ollama installation
    console.print("Checking Ollama installation...")
    import subprocess
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            console.print("✅ Ollama is installed and running")
            
            # Check if mistral:7b is available
            if "mistral:7b" in result.stdout:
                console.print("✅ Mistral 7B model is available")
            else:
                console.print("⚠️  Mistral 7B model not found")
                if Confirm.ask("Download Mistral 7B model?"):
                    console.print("Downloading model...")
                    download_result = subprocess.run(["ollama", "pull", "mistral:7b"])
                    if download_result.returncode == 0:
                        console.print("✅ Model downloaded successfully")
                    else:
                        console.print("❌ Failed to download model")
        else:
            console.print("❌ Ollama not found or not running")
            console.print("Please install Ollama from: https://ollama.ai")
            return
            
    except FileNotFoundError:
        console.print("❌ Ollama not found in PATH")
        console.print("Please install Ollama from: https://ollama.ai")
        return
    
    # Check data directories
    console.print("\nChecking data directories...")
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    console.print(f"📁 PDF directory: {PDF_DIR}")
    console.print(f"📁 Images directory: {IMAGES_DIR}")
    
    # Initialize RAG system
    console.print("\nInitializing RAG system...")
    try:
        rag = get_rag_system()
        health = rag.health_check()
        
        for component, status in health.items():
            status_icon = "✅" if status else "❌"
            console.print(f"{status_icon} {component}: {'OK' if status else 'Failed'}")
        
        if all(health.values()):
            console.print("\n🎉 Setup complete! System is ready to use.")
        else:
            console.print("\n⚠️  Some components failed. Check logs for details.")
            
    except Exception as e:
        console.print(f"❌ Setup failed: {str(e)}")


@app.command()
def add_documents(
    path: str = typer.Argument(..., help="Path to PDF file, image file, or directory"),
    url: Optional[str] = typer.Option(None, "--url", "-u", help="URL to process")
):
    """Add documents to the knowledge base."""
    rag = get_rag_system()
    
    if url:
        console.print(f"Processing URL: {url}")
        with console.status("[bold green]Processing URL..."):
            documents = doc_processor.process_url(url)
        
        if documents:
            with console.status("[bold green]Adding to knowledge base..."):
                success = rag.add_documents(documents)
            
            if success:
                console.print(f"✅ Added {len(documents)} document chunks from URL")
            else:
                console.print("❌ Failed to add documents")
        else:
            console.print("❌ No content extracted from URL")
        return
    
    path_obj = Path(path)
    
    if not path_obj.exists():
        console.print(f"❌ Path does not exist: {path}")
        return
    
    console.print(f"Processing: {path}")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Processing documents...", total=None)
        
        if path_obj.is_file():
            if path_obj.suffix.lower() == '.pdf':
                documents = doc_processor.process_pdf(path_obj)
            elif path_obj.suffix.lower() in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                documents = doc_processor.process_image(path_obj)
            else:
                console.print("❌ Unsupported file type")
                return
        else:
            documents = doc_processor.process_directory(path_obj)
        
        progress.update(task, description="Adding to knowledge base...")
        
        if documents:
            success = rag.add_documents(documents)
            
            if success:
                progress.update(task, description=f"✅ Added {len(documents)} document chunks")
            else:
                progress.update(task, description="❌ Failed to add documents")
        else:
            progress.update(task, description="❌ No documents processed")


@app.command()
def query(
    question: str = typer.Argument(..., help="Your technical question"),
    sources: bool = typer.Option(True, "--sources/--no-sources", help="Include source information")
):
    """Query the technical knowledge base."""
    rag = get_rag_system()
    
    with console.status("[bold green]Thinking..."):
        response = rag.query(question, include_sources=sources)
    
    # Display answer
    console.print(Panel(
        response["answer"],
        title="🤖 Answer",
        border_style="green"
    ))
    
    # Display sources if requested
    if sources and response["sources"]:
        console.print("\n📚 Sources:")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Source", style="dim")
        table.add_column("Type", style="cyan")
        table.add_column("Content Preview", style="white")
        
        for source in response["sources"][:5]:  # Show top 5 sources
            metadata = source["metadata"]
            source_name = metadata.get("filename", metadata.get("source", "Unknown"))
            doc_type = metadata.get("type", "Unknown")
            content_preview = source["content"]
            
            table.add_row(source_name, doc_type, content_preview)
        
        console.print(table)


@app.command()
def interactive():
    """Start interactive chat mode."""
    rag = get_rag_system()
    
    console.print(Panel.fit("🎯 Interactive AI Assistant"))
    console.print("Type 'exit', 'quit', or press Ctrl+C to exit")
    console.print("Type 'help' for available commands\n")
    
    try:
        while True:
            question = Prompt.ask("🤖 Your question")
            
            if question.lower() in ['exit', 'quit', 'bye']:
                break
            elif question.lower() == 'help':
                console.print("""
Available commands:
- Ask any technical question
- 'stats' - Show knowledge base statistics  
- 'health' - Check system health
- 'clear' - Clear screen
- 'exit' or 'quit' - Exit interactive mode
                """)
                continue
            elif question.lower() == 'stats':
                stats = rag.get_collection_stats()
                console.print(f"📊 Knowledge Base Stats: {json.dumps(stats, indent=2)}")
                continue
            elif question.lower() == 'health':
                health = rag.health_check()
                for component, status in health.items():
                    status_icon = "✅" if status else "❌"
                    console.print(f"{status_icon} {component}")
                continue
            elif question.lower() == 'clear':
                console.clear()
                continue
            
            with console.status("[bold green]Analyzing..."):
                response = rag.query(question, include_sources=True)
            
            # Display answer with formatting
            console.print(Panel(
                response["answer"],
                title="🤖 Answer",
                border_style="green"
            ))
            
            # Show sources briefly
            if response["sources"]:
                sources_text = ", ".join([
                    s["metadata"].get("filename", "web") 
                    for s in response["sources"][:3]
                ])
                console.print(f"📚 Sources: {sources_text}")
            
            console.print()  # Add spacing
            
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!")


@app.command()
def stats():
    """Show knowledge base statistics."""
    rag = get_rag_system()
    
    stats = rag.get_collection_stats()
    
    if "error" in stats:
        console.print(f"❌ Error getting stats: {stats['error']}")
        return
    
    # Create stats panel
    stats_text = f"""
Total Documents: {stats.get('total_documents', 0)}
Document Types: {json.dumps(stats.get('document_types', {}), indent=2)}
Unique Sources: {stats.get('unique_sources', 0)}
    """
    
    console.print(Panel(stats_text, title="📊 Knowledge Base Statistics"))
    
    if stats.get('sample_sources'):
        console.print("\n📚 Sample Sources:")
        for source in stats['sample_sources'][:10]:
            console.print(f"  • {source}")


@app.command()
def health():
    """Check system health."""
    rag = get_rag_system()
    
    health_status = rag.health_check()
    
    table = Table(title="System Health Check")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="bold")
    
    for component, status in health_status.items():
        status_text = "✅ OK" if status else "❌ Failed"
        table.add_row(component.title(), status_text)
    
    console.print(table)


@app.command()
def clear_db():
    """Clear all documents from the knowledge base."""
    if Confirm.ask("⚠️  This will delete all documents from the knowledge base. Continue?"):
        rag = get_rag_system()
        
        with console.status("[bold red]Clearing database..."):
            success = rag.delete_collection()
        
        if success:
            console.print("✅ Knowledge base cleared")
        else:
            console.print("❌ Failed to clear knowledge base")


def main():
    """Main entry point."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!")
    except Exception as e:
        console.print(f"❌ Error: {str(e)}")
        logger.exception("Unhandled exception")


if __name__ == "__main__":
    main()