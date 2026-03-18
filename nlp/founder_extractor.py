"""
Founder Details Extractor from Pitch Deck
Extracts:
- Founder names
- Experience level
- Education/Background
- Technical expertise
- Previous startup experience
- Domain expertise
"""

import re
from typing import Dict, List, Optional
from utils.logger import log

class FounderExtractor:
    """Extract founder-specific details from pitch deck text."""
    
    # Top tier schools (Stanford, MIT, etc.)
    TOP_SCHOOLS = [
        "stanford", "mit", "harvard", "caltech", "berkeley", "oxford", "cambridge",
        "carnegie mellon", "yale", "princeton", "uc berkeley", "cmu"
    ]
    
    # Experience keywords
    EXPERIENCE_KEYWORDS = [
        "ceo", "cto", "founder", "co-founder", "cofounder",
        "executive", "director", "manager", "lead", "engineer",
        "product manager", "former", "previously"
    ]
    
    # Technical keywords
    TECHNICAL_KEYWORDS = [
        "engineer", "developer", "programmer", "software", "coding",
        "machine learning", "ai", "data science", "full stack",
        "frontend", "backend", "devops", "architect"
    ]
    
    # Startup keywords
    STARTUP_KEYWORDS = [
        "serial entrepreneur", "serial founder", "startup", "founded",
        "exit", "acquired", "exited", "bootstrap", "venture"
    ]
    
    def __init__(self):
        """Initialize founder extractor."""
        log.info("✓ FounderExtractor initialized")
    
    def extract_founder_info(self, text: str, entities: Dict) -> Dict:
        """
        Extract comprehensive founder information.
        
        Args:
            text: Full pitch deck text
            entities: Named entities from NLP analysis
        
        Returns:
            Dictionary with founder details
        """
        founder_info = {
            "names": self._extract_founder_names(text, entities),
            "count": 0,
            "experience_level": self._calculate_experience_level(text),
            "education": self._extract_education(text),
            "technical_background": self._extract_technical_background(text),
            "previous_startups": self._extract_startup_history(text),
            "domain_expertise": self._extract_domain_expertise(text),
        }
        
        founder_info["count"] = len(founder_info["names"])
        
        log.info(f"✓ Extracted {founder_info['count']} founders")
        
        return founder_info
    
    def _extract_founder_names(self, text: str, entities: Dict) -> List[str]:
        """Extract founder names."""
        names = []
        
        # Get from named entities
        if entities.get("PERSON"):
            names.extend(entities["PERSON"][:3])  # Top 3 persons
        
        # Look for specific patterns
        patterns = [
            r"(?:Founder|Co-founder|Cofounder)s?\s*:?\s*([A-Za-z\s]+?)(?:,|and|$)",
            r"(?:Founded by|Created by)\s+([A-Za-z\s]+?)(?:,|and|in|$)",
            r"(?:Team|Leadership)\s*:?\s*(?:.*?)([A-Z][a-z]+\s+[A-Z][a-z]+)(?:\s*-|,|$)",
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                name = match.group(1).strip()
                # Filter out common non-names
                if name and len(name.split()) >= 2 and name not in names:
                    names.append(name)
        
        return list(dict.fromkeys(names))[:5]  # Unique, max 5 names
    
    def _calculate_experience_level(self, text: str) -> str:
        """Calculate overall experience level."""
        text_lower = text.lower()
        
        # Count experience indicators
        experience_count = 0
        
        # Check for C-level positions
        if any(x in text_lower for x in ["ceo", "cto", "cfo", "chief"]):
            experience_count += 2
        
        # Check for director/manager positions
        if any(x in text_lower for x in ["director", "manager", "lead", "head"]):
            experience_count += 1
        
        # Check for senior/experience indicators
        if any(x in text_lower for x in ["senior", "principal", "staff", "experience", "years"]):
            experience_count += 1
        
        # Check for big company background
        big_companies = ["google", "facebook", "meta", "amazon", "apple", "microsoft", 
                        "stripe", "uber", "airbnb", "netflix"]
        if any(x in text_lower for x in big_companies):
            experience_count += 2
        
        # Determine level
        if experience_count >= 4:
            return "Highly Experienced"
        elif experience_count >= 2:
            return "Moderately Experienced"
        elif experience_count >= 1:
            return "Some Experience"
        else:
            return "Early Career"
    
    def _extract_education(self, text: str) -> Dict:
        """Extract education details."""
        education = {
            "top_school": None,
            "degree": None,
            "field_of_study": None,
        }
        
        text_lower = text.lower()
        
        # Check for top schools
        for school in self.TOP_SCHOOLS:
            if school in text_lower:
                education["top_school"] = school.upper()
                break
        
        # Degree patterns
        degree_patterns = [
            r"(?:B\.?S\.?|B\.?A\.?|Bachelor's?)\s+(?:in|of)?\s+([A-Za-z\s]+?)(?:,|\.|from|$)",
            r"(?:M\.?S\.?|M\.?A\.?|Master's?)\s+(?:in|of)?\s+([A-Za-z\s]+?)(?:,|\.|from|$)",
            r"(?:Ph\.?D\.?|Doctorate)\s+(?:in|of)?\s+([A-Za-z\s]+?)(?:,|\.|from|$)",
        ]
        
        for pattern in degree_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                education["degree"] = pattern.split()[0]  # B.S., M.S., etc.
                education["field_of_study"] = match.group(1).strip()
                break
        
        return education
    
    def _extract_technical_background(self, text: str) -> bool:
        """Check if founder has technical background."""
        text_lower = text.lower()
        
        technical_count = 0
        
        for keyword in self.TECHNICAL_KEYWORDS:
            if keyword in text_lower:
                technical_count += 1
        
        return technical_count >= 2
    
    def _extract_startup_history(self, text: str) -> Dict:
        """Extract previous startup experience."""
        history = {
            "is_serial": False,
            "previous_exits": 0,
            "previous_startups": None,
        }
        
        text_lower = text.lower()
        
        # Check for serial entrepreneur
        if "serial" in text_lower and ("founder" in text_lower or "entrepreneur" in text_lower):
            history["is_serial"] = True
        
        # Count exits/acquisitions
        exit_keywords = ["exit", "acquired", "exited", "sold"]
        for keyword in exit_keywords:
            history["previous_exits"] += text_lower.count(keyword)
        
        # Extract previous startup names
        startup_patterns = [
            r"(?:founded|started|created)\s+([A-Za-z0-9\s]+?)(?:\s+in\s+\d+|,|$)",
            r"(?:at|from)\s+([A-Za-z0-9\s]+?)\s+(?:where|as a|i was)",
        ]
        
        previous_startups = []
        for pattern in startup_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                startup = match.group(1).strip()
                if startup and len(startup) < 50:  # Reasonable startup name length
                    previous_startups.append(startup)
        
        if previous_startups:
            history["previous_startups"] = ", ".join(list(dict.fromkeys(previous_startups)))
        
        return history
    
    def _extract_domain_expertise(self, text: str) -> str:
        """Extract domain/industry expertise."""
        domains = [
            ("Finance", ["fintech", "banking", "payment", "trading", "insurance"]),
            ("Technology", ["ai", "ml", "software", "devops", "blockchain"]),
            ("E-commerce", ["ecommerce", "retail", "marketplace", "shopping"]),
            ("Healthcare", ["healthcare", "health", "biotech", "medical", "pharma"]),
            ("Education", ["education", "edtech", "learning", "training"]),
            ("Transportation", ["transportation", "logistics", "delivery", "mobility"]),
            ("Real Estate", ["real estate", "property", "realestate"]),
            ("Energy", ["energy", "renewable", "solar", "wind"]),
        ]
        
        text_lower = text.lower()
        
        for domain, keywords in domains:
            for keyword in keywords:
                if keyword in text_lower:
                    return domain
        
        return "General"