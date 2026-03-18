"""
Utilities package.
"""

from utils.logger import log
from utils.helpers import (
    safe_request,
    extract_numbers,
    extract_emails,
    extract_urls,
    clean_text,
    normalize_company_name,
    calculate_similarity,
)

__all__ = [
    "log",
    "safe_request",
    "extract_numbers",
    "extract_emails",
    "extract_urls",
    "clean_text",
    "normalize_company_name",
    "calculate_similarity",
]