import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import cv2
import numpy as np
from pdf2image import convert_from_path
import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .config import (
    TESSERACT_PATH, DPI, CHUNK_SIZE, CHUNK_OVERLAP,
    REQUEST_TIMEOUT, MAX_RETRIES, DOMAIN_TOPICS
)

# Configure Tesseract path
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Processes various document types for AI RAG system."""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def process_pdf(self, file_path: Path) -> List[Document]:
        """Process PDF files, handling both text and image-based PDFs."""
        documents = []
        
        try:
            # Try text extraction first
            doc = fitz.open(str(file_path))
            full_text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                # If page has minimal text, treat as image-based
                if len(text.strip()) < 100:
                    logger.info(f"Page {page_num + 1} appears to be image-based, using OCR")
                    text = self._ocr_pdf_page(file_path, page_num)
                
                full_text += f"\n\n--- Page {page_num + 1} ---\n\n{text}"
            
            doc.close()
            
            # Create document chunks
            chunks = self.text_splitter.split_text(full_text)
            
            for i, chunk in enumerate(chunks):
                metadata = {
                    "source": str(file_path),
                    "type": "pdf",
                    "chunk_id": i,
                    "filename": file_path.name,
                    "domain_relevant": self._is_domain_relevant(chunk)
                }
                documents.append(Document(page_content=chunk, metadata=metadata))
                
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            
        return documents
    
    def _ocr_pdf_page(self, pdf_path: Path, page_num: int) -> str:
        """Extract text from PDF page using OCR."""
        try:
            # Convert PDF page to image
            images = convert_from_path(
                str(pdf_path),
                dpi=DPI,
                first_page=page_num + 1,
                last_page=page_num + 1
            )
            
            if images:
                # Enhance image for better OCR
                img_array = np.array(images[0])
                enhanced_img = self._enhance_image_for_ocr(img_array)
                
                # Perform OCR
                text = pytesseract.image_to_string(enhanced_img, config='--psm 6')
                return text
                
        except Exception as e:
            logger.error(f"OCR failed for page {page_num}: {str(e)}")
            
        return ""
    
    def process_image(self, file_path: Path) -> List[Document]:
        """Process images and extract text using OCR."""
        documents = []
        
        try:
            # Load and enhance image
            img = cv2.imread(str(file_path))
            enhanced_img = self._enhance_image_for_analysis(img)
            
            # Perform OCR with specialized config for technical content
            text = pytesseract.image_to_string(
                enhanced_img,
                config='--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,()[]{}+-=*/:;'
            )
            
            # Extract technical information and labels
            technical_info = self._extract_technical_info(text)
            
            # Combine raw OCR text with extracted technical information
            full_text = f"Image Analysis:\n{text}\n\nTechnical Information:\n{technical_info}"
            
            chunks = self.text_splitter.split_text(full_text)
            
            for i, chunk in enumerate(chunks):
                metadata = {
                    "source": str(file_path),
                    "type": "image",
                    "chunk_id": i,
                    "filename": file_path.name,
                    "domain_relevant": self._is_domain_relevant(full_text)
                }
                documents.append(Document(page_content=chunk, metadata=metadata))
                
        except Exception as e:
            logger.error(f"Error processing schematic {file_path}: {str(e)}")
            
        return documents
    
    def _enhance_image_for_ocr(self, img_array: np.ndarray) -> np.ndarray:
        """Enhance image for better OCR results."""
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
            
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Noise removal
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        return cleaned
    
    def _enhance_image_for_analysis(self, img: np.ndarray) -> np.ndarray:
        """Enhance images for technical content recognition."""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Apply binary threshold
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def _extract_technical_info(self, ocr_text: str) -> str:
        """Extract technical values and identifiers from OCR text."""
        import re
        
        technical_patterns = {
            'resistors': r'R\d+\s*[=:]?\s*(\d+\.?\d*\s*[kKmM]?[Ω]?)',
            'capacitors': r'C\d+\s*[=:]?\s*(\d+\.?\d*\s*[pnumμ]?[F]?)',
            'inductors': r'L\d+\s*[=:]?\s*(\d+\.?\d*\s*[pnumμmH]?[H]?)',
            'frequencies': r'(\d+\.?\d*\s*[kKmMgG]?[Hh][Zz])',
            'voltages': r'(\d+\.?\d*\s*[mμnpkKM]?[Vv])',
            'currents': r'(\d+\.?\d*\s*[mμnpkKM]?[Aa])',
            'power': r'(\d+\.?\d*\s*[mμnpkKM]?[Ww])',
            'impedance': r'(\d+\.?\d*\s*[Ω])'
        }
        
        extracted_values = []
        
        for value_type, pattern in technical_patterns.items():
            matches = re.findall(pattern, ocr_text, re.IGNORECASE)
            if matches:
                extracted_values.append(f"{value_type}: {', '.join(matches)}")
        
        return '\n'.join(extracted_values) if extracted_values else "No technical values detected"
    
    def process_url(self, url: str) -> List[Document]:
        """Process web pages and extract relevant content."""
        documents = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Check if content is domain relevant
            if not self._is_domain_relevant(text):
                logger.warning(f"URL {url} content doesn't appear domain relevant")
            
            chunks = self.text_splitter.split_text(text)
            
            for i, chunk in enumerate(chunks):
                metadata = {
                    "source": url,
                    "type": "web",
                    "chunk_id": i,
                    "title": soup.title.string if soup.title else "Unknown",
                    "domain_relevant": self._is_domain_relevant(chunk)
                }
                documents.append(Document(page_content=chunk, metadata=metadata))
                
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}")
            
        return documents
    
    def _is_domain_relevant(self, text: str) -> bool:
        """Check if text content is relevant to the domain."""
        text_lower = text.lower()
        
        # Count topic matches
        matches = sum(1 for topic in DOMAIN_TOPICS if topic in text_lower)
        
        # Additional domain keywords (configurable)
        domain_keywords = [
            'ham radio', 'amateur radio', 'rf', 'radio frequency',
            'vswr', 'swr', 'qrp', 'qro', 'dx', 'contest',
            'callsign', 'cw', 'ssb', 'fm', 'am', 'psk31',
            'arrl', 'icom', 'yaesu', 'kenwood'
        ]
        
        keyword_matches = sum(1 for keyword in domain_keywords if keyword in text_lower)
        
        return (matches + keyword_matches) >= 2
    
    def process_directory(self, directory_path: Path, file_types: List[str] = None) -> List[Document]:
        """Process all supported files in a directory."""
        if file_types is None:
            file_types = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']
        
        documents = []
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in file_types:
                logger.info(f"Processing {file_path}")
                
                if file_path.suffix.lower() == '.pdf':
                    docs = self.process_pdf(file_path)
                elif file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                    docs = self.process_image(file_path)
                
                documents.extend(docs)
        
        return documents