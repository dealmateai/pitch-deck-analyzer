"""
PDF Text Extraction Module (FIXED VERSION - PDFPLUMBER ONLY)
Handles extraction of text from pitch deck PDFs.
No PyMuPDF - only pdfplumber
"""

import re
from typing import Dict, Optional, List
from pathlib import Path
import pdfplumber
from utils.logger import log

class PDFExtractor:
    """Extract text and metadata from PDF files using pdfplumber only."""
    
    def __init__(self, max_pages: int = 100):
        """
        Initialize PDF extractor.
        
        Args:
            max_pages: Maximum pages to extract
        """
        self.max_pages = max_pages
        log.info("✓ PDFExtractor initialized (pdfplumber only)")
    
    def extract(self, pdf_path: str) -> Optional[Dict]:
        """
        Extract text from PDF using pdfplumber.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Dictionary with extracted data or None if failed
        """
        
        # Validate file exists
        if not Path(pdf_path).exists():
            log.error(f"PDF file not found: {pdf_path}")
            return None
        
        try:
            log.info(f"Extracting text from PDF: {pdf_path}")
            
            # Open PDF
            with pdfplumber.open(pdf_path) as pdf:
                
                # Check if empty
                if len(pdf.pages) == 0:
                    log.error(f"PDF is empty: {pdf_path}")
                    return None
                
                # Limit pages
                num_pages = min(len(pdf.pages), self.max_pages)
                
                log.info(f"PDF has {len(pdf.pages)} pages, extracting {num_pages}")
                
                # Extract text
                full_text = []
                text_by_page = []
                
                for page_num in range(num_pages):
                    try:
                        page = pdf.pages[page_num]
                        text = page.extract_text()
                        
                        if text is None:
                            text = ""
                        
                        full_text.append(text)
                        text_by_page.append(text)
                        
                        log.info(f"  Page {page_num + 1}: {len(text)} characters")
                        
                    except Exception as e:
                        log.warning(f"  Page {page_num + 1} extraction failed: {str(e)[:50]}")
                        text_by_page.append("")
                        continue
                
                # Combine all text
                combined_text = "\n".join(full_text)
                
                if not combined_text.strip():
                    log.error("No text extracted from PDF")
                    return None
                
                # Clean text
                cleaned_text = self._clean_text(combined_text)
                
                # Extract numbers
                numbers = self._extract_numbers(combined_text)
                
                # Extract URLs
                urls = self._extract_urls(combined_text)
                
                # Extract emails
                emails = self._extract_emails(combined_text)
                
                result = {
                    "full_text": combined_text,
                    "full_text_cleaned": cleaned_text,
                    "text_by_page": text_by_page,
                    "num_pages": num_pages,
                    "word_count": len(cleaned_text.split()),
                    "char_count": len(combined_text),
                    "numbers": numbers,
                    "urls": urls,
                    "emails": emails,
                }
                
                log.info(f"✓ Successfully extracted {result['num_pages']} pages")
                log.info(f"  Total words: {result['word_count']}")
                log.info(f"  Total characters: {result['char_count']}")
                
                return result
        
        except Exception as e:
            log.error(f"PDF extraction failed: {str(e)}", exc_info=True)
            return None
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text.
        
        Args:
            text: Raw text
        
        Returns:
            Cleaned text
        """
        try:
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Remove special characters but keep alphanumeric and basic punctuation
            text = re.sub(r'[^\w\s\-.,!?():\'"@]', '', text)
            
            # Remove URLs
            text = re.sub(r'http\S+|www\S+', '', text)
            
            # Strip leading/trailing whitespace
            text = text.strip()
            
            return text
        
        except Exception as e:
            log.warning(f"Text cleaning failed: {str(e)}")
            return text
    
    def _extract_numbers(self, text: str) -> Dict[str, List[str]]:
        """Extract numerical data from text."""
        numbers = {
            "revenue": [],
            "users": [],
            "growth_rate": [],
            "funding": [],
        }
        
        try:
            # Revenue patterns
            revenue_patterns = [
                r'\$\s*(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:M|B|K|million|billion|thousand)',
                r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:MRR|ARR)',
            ]
            
            for pattern in revenue_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                numbers["revenue"].extend(matches)
            
            # User/customer patterns
            user_patterns = [
                r'(\d+(?:,\d{3})*)\s+(?:users?|customers?|active)',
                r'(?:over|more than|nearly)\s+(\d+(?:,\d{3})*)\s+(?:users?|customers?)',
            ]
            
            for pattern in user_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                numbers["users"].extend(matches)
            
            # Growth rate patterns
            growth_patterns = [
                r'(\d+)%\s+(?:growth|increase|month|annually)',
                r'growing\s+(?:at\s+)?(\d+)%',
            ]
            
            for pattern in growth_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                numbers["growth_rate"].extend(matches)
            
            # Funding patterns
            funding_patterns = [
                r'seeking\s+\$\s*(\d+(?:,\d{3})*\s*(?:M|B))',
                r'raised\s+\$\s*(\d+(?:,\d{3})*\s*(?:M|B))',
            ]
            
            for pattern in funding_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                numbers["funding"].extend(matches)
            
            return numbers
        
        except Exception as e:
            log.warning(f"Number extraction failed: {str(e)}")
            return numbers
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text."""
        try:
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            return list(set(urls))  # Remove duplicates
        except:
            return []
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract emails from text."""
        try:
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            return list(set(emails))  # Remove duplicates
        except:
            return []