"""
NLP module for text extraction and analysis.
Uses PDFPLUMBER ONLY (no PyMuPDF).
"""

from importlib import import_module
from typing import Any


def __getattr__(name: str) -> Any:
    if name == "PDFExtractor":
        return import_module("nlp.pdf_extractor").PDFExtractor
    if name == "NLPPipeline":
        return import_module("nlp.nlp_pipeline").NLPPipeline
    raise AttributeError(f"module 'nlp' has no attribute {name!r}")

__all__ = [
    "PDFExtractor",
    "NLPPipeline",
]