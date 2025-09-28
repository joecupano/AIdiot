import os
import platform
import shutil
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PDF_DIR = DATA_DIR / "pdfs"
IMAGES_DIR = DATA_DIR / "images"
VECTOR_DB_DIR = DATA_DIR / "vector_db"

# Ensure directories exist
PDF_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

# LLM Configuration
OLLAMA_MODEL = "mistral:7b"
OLLAMA_BASE_URL = "http://localhost:11434"

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_DB_COLLECTION = "amateur_radio_docs"

# OCR Configuration (for image-based PDFs and images)
# Auto-detect Tesseract path based on platform

# Try to find Tesseract automatically
TESSERACT_PATH = shutil.which("tesseract")

# Platform-specific fallback paths
if not TESSERACT_PATH:
    system = platform.system().lower()
    if system == "windows":
        TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    elif system == "linux":
        TESSERACT_PATH = "/usr/bin/tesseract"
    elif system == "darwin":  # macOS
        # Try common Homebrew paths
        for path in ["/opt/homebrew/bin/tesseract", "/usr/local/bin/tesseract"]:
            if os.path.exists(path):
                TESSERACT_PATH = path
                break
        else:
            TESSERACT_PATH = "/usr/local/bin/tesseract"  # Default fallback

DPI = 300  # For PDF to image conversion

# Web scraping configuration
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3

# API Configuration
API_HOST = "127.0.0.1"
API_PORT = 8000

# Topic-specific configurations (configurable for different domains)
DOMAIN_TOPICS = [
    "antenna design", "RF circuits", "amplifiers", "oscillators",
    "filters", "transmission lines", "impedance matching",
    "smith charts", "propagation", "modulation", "demodulation",
    "mixers", "transceivers", "repeaters", "microwave",
    "VHF", "UHF", "HF", "baluns", "transformers"
]

# Supported file formats
SUPPORTED_PDF_EXTENSIONS = [".pdf"]
SUPPORTED_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"