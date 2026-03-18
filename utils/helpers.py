"""
Utility functions for common operations.
"""

import re
import requests
from typing import Optional, List, Dict
from utils.logger import log

def safe_request(url: str, method: str = "GET", timeout: int = 10, **kwargs) -> Optional[requests.Response]:
    """
    Safely make HTTP requests with error handling.
    
    Args:
        url: URL to request
        method: HTTP method (GET, POST, etc.)
        timeout: Request timeout in seconds
        **kwargs: Additional arguments for requests
    
    Returns:
        Response object or None if failed
    """
    try:
        response = requests.request(method, url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        log.error(f"Request failed for {url}: {str(e)}")
        return None

def extract_numbers(text: str) -> List[float]:
    """
    Extract all numbers from text.
    
    Args:
        text: Input text
    
    Returns:
        List of extracted numbers
    """
    if not text:
        return []
    numbers = re.findall(r'[\d,]+\.?\d*', text)
    return [float(num.replace(',', '')) for num in numbers if num]

def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from text.
    
    Args:
        text: Input text
    
    Returns:
        List of extracted emails
    """
    if not text:
        return []
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)

def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text.
    
    Args:
        text: Input text
    
    Returns:
        List of extracted URLs
    """
    if not text:
        return []
    pattern = r'https?://[^\s]+'
    return re.findall(pattern, text)

def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Input text
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\(\)]', '', text)
    
    return text.strip()

def normalize_company_name(name: str) -> str:
    """
    Normalize company name for comparison.
    
    Args:
        name: Company name
    
    Returns:
        Normalized name
    """
    if not name:
        return ""
    
    name = name.lower().strip()
    # Remove common suffixes
    name = re.sub(r'\s(inc|ltd|llc|corp|co|inc\.)$', '', name)
    return name

def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate simple string similarity (Jaccard similarity).
    
    Args:
        str1: First string
        str2: Second string
    
    Returns:
        Similarity score 0-1
    """
    str1 = set(str1.lower().split())
    str2 = set(str2.lower().split())
    
    if not str1 or not str2:
        return 0.0
    
    intersection = len(str1 & str2)
    union = len(str1 | str2)
    
    return intersection / union if union > 0 else 0.0