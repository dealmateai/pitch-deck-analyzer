"""
NLP Pipeline - FIXED VERSION
Analyzes pitch deck text with proper error handling
"""

import re
from typing import Dict, List, Optional
import spacy
from sentence_transformers import SentenceTransformer
from utils.logger import log

class NLPPipeline:
    """NLP analysis pipeline with proper error handling."""
    
    def __init__(self):
        """Initialize NLP pipeline."""
        log.info("Initializing NLP pipeline...")
        
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            log.info("✓ Loaded spaCy model: en_core_web_sm")
        except Exception as e:
            log.error(f"Failed to load spaCy: {str(e)}")
            raise
        
        try:
            # Load sentence transformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            log.info("✓ Loaded Sentence Transformer: all-MiniLM-L6-v2")
        except Exception as e:
            log.error(f"Failed to load transformer: {str(e)}")
            raise
    
    def analyze_text(self, text: str) -> Optional[Dict]:
        """
        Analyze text with NLP.
        
        Args:
            text: Input text to analyze
        
        Returns:
            Dictionary with analysis results
        """
        
        if not text or not text.strip():
            log.error("Empty text provided")
            return None
        
        try:
            log.info(f"Analyzing text ({len(text)} chars)...")
            
            # Process with spaCy
            doc = self.nlp(text[:1000000])  # Limit to 1M chars to avoid memory issues
            
            # Extract entities
            entities = self._extract_entities(doc)
            
            # Extract keywords
            keywords = self._extract_keywords(text)
            
            # Extract sections
            sections = self._extract_sections(text)
            
            # Generate embeddings
            try:
                embedding = self.model.encode(text[:1000]).tolist()  # First 1000 chars
            except:
                embedding = None
            
            result = {
                "entities": entities,
                "keywords": keywords,
                "sections": sections,
                "embedding": embedding,
                "text_length": len(text),
            }
            
            log.info(f"✓ Analysis complete: {len(entities)} entities, {len(keywords)} keywords")
            
            return result
        
        except Exception as e:
            log.error(f"Text analysis failed: {str(e)}", exc_info=True)
            return None
    
    def _extract_entities(self, doc) -> Dict[str, List[str]]:
        """Extract named entities."""
        entities = {
            "PERSON": [],
            "ORG": [],
            "GPE": [],
            "MONEY": [],
            "PERCENT": [],
            "DATE": [],
        }
        
        try:
            for ent in doc.ents:
                if ent.label_ in entities:
                    if ent.text not in entities[ent.label_]:
                        entities[ent.label_].append(ent.text)
        except Exception as e:
            log.warning(f"Entity extraction failed: {str(e)}")
        
        return entities
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        keywords = []
        
        try:
            # Common pitch deck keywords
            pitch_keywords = [
                "problem", "solution", "market", "traction", "team",
                "revenue", "users", "growth", "funding", "vision",
                "mission", "product", "business model", "competitive",
                "advantage", "technology", "innovation", "disrupt",
                "platform", "saas", "enterprise", "founder", "ceo",
            ]
            
            text_lower = text.lower()
            
            for keyword in pitch_keywords:
                if keyword in text_lower:
                    keywords.append(keyword)
            
            # Remove duplicates
            keywords = list(set(keywords))
            
        except Exception as e:
            log.warning(f"Keyword extraction failed: {str(e)}")
        
        return keywords
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract major sections from pitch deck."""
        sections = {
            "industry": None,
            "problem": None,
            "solution": None,
        }
        
        try:
            text_lower = text.lower()
            
            # Industry
            industry_keywords = [
                "fintech", "ai/ml", "saas", "ecommerce", "healthtech",
                "edtech", "logistics", "travel", "real estate"
            ]
            
            for ind in industry_keywords:
                if ind in text_lower:
                    sections["industry"] = ind.upper()
                    break
            
            # Problem section
            problem_match = re.search(
                r'(?:problem|challenge|pain point)\s*:?\s*(.{50,300}?)(?=solution|approach|how|$)',
                text,
                re.IGNORECASE | re.DOTALL
            )
            if problem_match:
                sections["problem"] = problem_match.group(1).strip()[:100]
            
            # Solution section
            solution_match = re.search(
                r'(?:solution|approach|how we)\s*:?\s*(.{50,300}?)(?=market|business|team|$)',
                text,
                re.IGNORECASE | re.DOTALL
            )
            if solution_match:
                sections["solution"] = solution_match.group(1).strip()[:100]
            
        except Exception as e:
            log.warning(f"Section extraction failed: {str(e)}")
        
        return sections