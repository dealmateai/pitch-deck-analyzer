"""
Company Details Extractor from Pitch Deck
Extracts:
- Company name
- Industry
- Problem statement
- Market size
- Traction metrics
- Revenue/Users/Growth
"""

import re
from typing import Dict, List, Optional, Tuple
from utils.logger import log
from config import EXTRACTION_CONFIG

class CompanyExtractor:
    """Extract company-specific details from pitch deck text."""
    
    def __init__(self):
        """Initialize company extractor."""
        log.info("✓ CompanyExtractor initialized")
        self.industry_keywords = EXTRACTION_CONFIG["industry_mapping"]
    
    def extract_company_info(self, text: str, entities: Dict) -> Dict:
        """
        Extract comprehensive company information.
        
        Args:
            text: Full pitch deck text
            entities: Named entities from NLP analysis
        
        Returns:
            Dictionary with company details
        """
        company_info = {
            "name": self._extract_company_name(text, entities),
            "industry": self._extract_industry(text),
            "problem": self._extract_problem(text),
            "solution": self._extract_solution(text),
            "market_size": self._extract_market_size(text),
            "traction": self._extract_traction(text),
            "business_model": self._extract_business_model(text),
        }
        
        log.info(f"✓ Extracted company info: {company_info['name']}")
        
        return company_info
    
    def _extract_company_name(self, text: str, entities: Dict) -> str:
        """Extract company name from entities or text."""
        # Try to get from entities first
        if entities.get("ORG"):
            return entities["ORG"][0]  # First organization entity
        
        # Look for common company name patterns
        patterns = [
            r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|are|provides?|offers?)",
            r"(?:Company|Product)\s+name\s*:?\s*([A-Z][^,.\n]+)",
            r"(?:We are|We're|Founded as|Introducing)\s+([A-Z][^,.\n]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return "Unknown Company"
    
    def _extract_industry(self, text: str) -> str:
        """Extract industry/domain."""
        text_lower = text.lower()
        
        # Match against predefined industries
        for industry, keywords in self.industry_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return industry.upper()
        
        # Fallback: look for specific patterns
        patterns = [
            r"(?:industry|sector|domain)\s*:?\s*([A-Za-z\s]+?)(?:\.|,|$)",
            r"(?:we are in|we operate in|we work in)\s+(?:the\s+)?([A-Za-z\s]+)\s+(?:industry|space|sector)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip().upper()
        
        return "Other"
    
    def _extract_problem(self, text: str) -> str:
        """Extract problem statement."""
        # Find problem section
        problem_patterns = [
            r"(?:THE\s+)?PROBLEM\s*:?\s*(.{50,400}?)(?=SOLUTION|HOW|APPROACH|$)",
            r"(?:Problem|Challenge|Pain Point)\s*:?\s*(.{50,400}?)(?:\.|,|SOLUTION|$)",
            r"(?:Today|Currently),?\s+(.{50,300}?)\s+(?:is|are|remains?)\s+(?:inefficient|broken|outdated|expensive|missing|lacking)",
        ]
        
        for pattern in problem_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                problem_text = match.group(1).strip()
                # Clean up the text
                problem_text = re.sub(r'\s+', ' ', problem_text)
                return problem_text[:300]  # Limit to 300 chars
        
        return "Not specified"
    
    def _extract_solution(self, text: str) -> str:
        """Extract solution description."""
        solution_patterns = [
            r"(?:OUR\s+)?SOLUTION\s*:?\s*(.{50,400}?)(?=MARKET|BUSINESS|TRACTION|$)",
            r"(?:Solution|Approach|How We)\s*:?\s*(.{50,400}?)(?:\.|,|MARKET|$)",
            r"(?:We|Our company)\s+(?:build|develop|create|provide|offer)\s+(.{50,300}?)\s+(?:to|that|which|leveraging)",
        ]
        
        for pattern in solution_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                solution_text = match.group(1).strip()
                solution_text = re.sub(r'\s+', ' ', solution_text)
                return solution_text[:300]
        
        return "Not specified"
    
    def _extract_market_size(self, text: str) -> Dict:
        """Extract market size information."""
        market_data = {
            "tam": None,
            "sam": None,
            "som": None,
            "growth_rate": None,
        }
        
        # TAM (Total Addressable Market)
        tam_patterns = [
            r"(?:TAM|Total\s+Addressable\s+Market)\s*:?\s*\$?\s*([\d,\.]+\s*(?:billion|million|trillion|B|M|T))",
            r"(?:market\s+size|market\s+opportunity)\s+(?:is|of|at)\s+\$?\s*([\d,\.]+\s*(?:billion|million|trillion|B|M|T))",
        ]
        
        for pattern in tam_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                market_data["tam"] = match.group(1).strip()
                break
        
        # Growth rate
        growth_patterns = [
            r"(\d+)%\s+(?:growth|increase|CAGR)",
            r"growing\s+(?:at\s+)?(\d+)%\s+(?:annually|yearly|per year)",
        ]
        
        for pattern in growth_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                market_data["growth_rate"] = f"{match.group(1)}%"
                break
        
        return market_data
    
    def _extract_traction(self, text: str) -> Dict:
        """Extract traction metrics."""
        traction = {
            "users": None,
            "revenue": None,
            "monthly_growth": None,
            "customers": None,
        }
        
        # Users/Customers
        user_patterns = [
            r"([\d,]+)\s+(?:users?|customers?|active\s+users?|paying\s+customers?)",
            r"(?:over|more than|nearly)\s+([\d,]+)\s+(?:users?|customers?)",
        ]
        
        for pattern in user_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                users = match.group(1).replace(',', '')
                traction["users"] = int(users) if users.isdigit() else match.group(1)
                break
        
        # Revenue
        revenue_patterns = [
            r"\$\s*([\d,\.]+)\s*(?:M|million|B|billion)?\s+(?:in\s+)?(?:revenue|ARR|MRR)",
            r"(?:revenue|sales)\s+(?:of|at|is)\s+\$\s*([\d,\.]+)\s*(?:M|million|B|billion)?",
        ]
        
        for pattern in revenue_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                traction["revenue"] = match.group(1).strip()
                break
        
        # Monthly growth
        growth_patterns = [
            r"(\d+)%\s+(?:monthly|month-over-month|MoM)\s+growth",
            r"growing\s+(\d+)%\s+(?:month|monthly)",
        ]
        
        for pattern in growth_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                traction["monthly_growth"] = f"{match.group(1)}%"
                break
        
        return traction
    
    def _extract_business_model(self, text: str) -> str:
        """Extract business model."""
        business_models = [
            ("SaaS", ["subscription", "saas", "monthly fee", "annual fee"]),
            ("Marketplace", ["marketplace", "commission", "transaction fee"]),
            ("Freemium", ["freemium", "free with premium"]),
            ("B2B", ["b2b", "business to business", "enterprise"]),
            ("B2C", ["b2c", "business to consumer", "direct to consumer", "d2c"]),
            ("Advertising", ["advertising", "ads", "ad-supported"]),
            ("Licensing", ["licensing", "license"]),
        ]
        
        text_lower = text.lower()
        
        for model, keywords in business_models:
            for keyword in keywords:
                if keyword in text_lower:
                    return model
        
        return "Not specified"