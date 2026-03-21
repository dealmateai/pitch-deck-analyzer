"""
Founder Extractor
Extracts founder information from pitch deck text
Enhanced with previous company extraction
"""

import re
from typing import Dict, List, Optional
from utils.logger import log

class FounderExtractor:
    """Extract founder information from text."""
    
    def __init__(self):
        """Initialize founder extractor."""
        log.info("✓ FounderExtractor initialized")
        
        # Common job titles to look for
        self.job_titles = [
            'CEO', 'CTO', 'COO', 'CFO', 'Founder', 'Co-founder', 'Co-Founder',
            'President', 'VP', 'Vice President', 'Director', 'Manager',
            'Engineer', 'Developer', 'Product Manager', 'Designer'
        ]
        
        # Top companies to look for (FAANG, unicorns, etc)
        self.known_companies = [
            'Google', 'Amazon', 'Facebook', 'Apple', 'Microsoft', 'Meta',
            'Tesla', 'Netflix', 'Airbnb', 'Uber', 'Stripe', 'Dropbox',
            'Figma', 'Slack', 'Twilio', 'Palantir', 'Coursera', 'Notion',
            'OpenAI', 'LinkedIn', 'Instagram', 'WhatsApp', 'Spotify',
            'Snapchat', 'Pinterest', 'Robinhood', 'Brex', 'Canva',
            'McKinsey', 'Goldman Sachs', 'BCG', 'Bain', 'Morgan Stanley'
        ]
        
        # Top universities to look for
        self.top_universities = [
            'Stanford', 'MIT', 'Harvard', 'Berkeley', 'Carnegie Mellon',
            'Yale', 'Princeton', 'Penn', 'Cornell', 'Caltech',
            'Cambridge', 'Oxford', 'Polytechnique', 'ETH Zurich',
            'University of Toronto', 'IIT', 'NUS', 'Tsinghua', 'Peking'
        ]
    
    def extract_founder_info(self, text: str, entities: Dict) -> Optional[Dict]:
        """
        Extract founder information from text.
        
        Args:
            text: Pitch deck text
            entities: NER entities from NLP pipeline
        
        Returns:
            Dictionary with founder information including previous companies
        """
        log.info("Extracting founder information...")
        
        info = {
            "names": [],
            "count": 0,
            "experience_level": "Unknown",
            "education": {"top_school": None, "degree": None, "field": None},
            "technical_background": False,
            "previous_companies": [],  # NEW
            "previous_startups": {"is_serial": False, "previous_exits": 0},
            "startup_experience": False,
            "domain_expertise": "General",
        }
        
        # Extract names from entities
        if entities.get("PERSON"):
            info["names"] = entities["PERSON"][:3]  # Limit to 3 founders
            info["count"] = len(info["names"])
        
        # Extract previous companies from text
        info["previous_companies"] = self._extract_previous_companies(text)
        
        # Determine experience level based on previous companies
        info["experience_level"] = self._determine_experience_level(
            info["previous_companies"],
            text
        )
        
        # Extract education
        info["education"] = self._extract_education(text)
        
        # Detect technical background
        info["technical_background"] = self._detect_technical_background(text)
        
        # Detect startup experience
        info["startup_experience"] = bool(
            re.search(r'founder|co-founder|startup|entrepreneur', text, re.IGNORECASE)
        )

        # Keep backward-compatible shape expected by fit calculator.
        info["previous_startups"] = {
            "is_serial": info["startup_experience"] or len(info["previous_companies"]) > 0,
            "previous_exits": 0,
        }
        
        # Determine domain expertise
        info["domain_expertise"] = self._determine_domain_expertise(text)
        
        log.info(f"✓ Extracted {info['count']} founders")
        log.info(f"  Experience: {info['experience_level']}")
        log.info(f"  Previous companies: {len(info['previous_companies'])}")
        log.info(f"  Technical: {info['technical_background']}")
        
        return info
    
    def _extract_previous_companies(self, text: str) -> List[Dict]:
        """
        Extract previous companies from text.
        
        Args:
            text: Input text
        
        Returns:
            List of previous companies with positions
        """
        previous_companies = []
        
        # Look for known companies in text
        for company in self.known_companies:
            if company.lower() in text.lower():
                # Try to find associated job title
                position = "Employee"
                
                # Look for patterns like "CEO at Google", "Google Engineer", etc.
                for title in self.job_titles:
                    pattern = rf'{title}\s+(?:at\s+)?{company}|{company}\s+{title}'
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        position = title
                        break
                
                # Avoid duplicates
                if not any(c['name'].lower() == company.lower() for c in previous_companies):
                    previous_companies.append({
                        "name": company,
                        "position": position
                    })
        
        return previous_companies
    
    def _determine_experience_level(self, previous_companies: List[Dict], text: str) -> str:
        """
        Determine experience level from previous companies.
        
        Args:
            previous_companies: List of previous companies
            text: Input text
        
        Returns:
            Experience level string
        """
        experience_score = 0
        
        # Score based on number of previous companies
        experience_score += len(previous_companies)
        
        # Look for seniority indicators
        if re.search(r'CEO|CTO|COO|VP|President|Director', text, re.IGNORECASE):
            experience_score += 2
        
        # Look for big tech company experience
        for company in ['Google', 'Amazon', 'Facebook', 'Apple', 'Microsoft']:
            if company.lower() in text.lower():
                experience_score += 1.5
        
        # Categorize
        if experience_score >= 4:
            return "Highly Experienced"
        elif experience_score >= 2:
            return "Moderately Experienced"
        elif experience_score >= 1:
            return "Some Experience"
        else:
            return "Early Career"
    
    def _extract_education(self, text: str) -> Dict:
        """Extract education information."""
        education = {
            "top_school": None,
            "degree": None,
            "field": None
        }
        
        # Look for top universities
        for university in self.top_universities:
            if university.lower() in text.lower():
                education["top_school"] = university.upper()
                break
        
        # Look for degree
        degree_patterns = [
            (r'PhD|Ph\.D', 'PhD'),
            (r'Master|M\.S|MS', 'Master'),
            (r'Bachelor|B\.S|BS', 'Bachelor'),
            (r'MBA', 'MBA'),
        ]
        
        for pattern, degree in degree_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                education["degree"] = degree
                break
        
        # Look for field of study
        field_patterns = [
            (r'Computer Science|CS|Software', 'Computer Science'),
            (r'Engineering|Electrical', 'Engineering'),
            (r'Business|Commerce|Economics', 'Business'),
            (r'Mathematics|Physics|Science', 'Science'),
            (r'Design|Art', 'Design'),
        ]
        
        for pattern, field in field_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                education["field"] = field
                break
        
        return education
    
    def _detect_technical_background(self, text: str) -> bool:
        """Detect if founder has technical background."""
        technical_keywords = [
            'engineer', 'developer', 'programmer', 'software', 'code',
            'cto', 'technical', 'algorithm', 'database', 'infrastructure',
            'computer science', 'machine learning', 'ai', 'ml', 'data'
        ]
        
        text_lower = text.lower()
        count = sum(1 for keyword in technical_keywords if keyword in text_lower)
        
        return count >= 2
    
    def _determine_domain_expertise(self, text: str) -> str:
        """Determine domain expertise from text."""
        expertise_keywords = {
            'Technology': ['tech', 'software', 'platform', 'ai', 'ml'],
            'Finance': ['fintech', 'payment', 'banking', 'investment', 'trading'],
            'Healthcare': ['health', 'medical', 'biotech', 'pharma'],
            'E-commerce': ['retail', 'ecommerce', 'marketplace', 'shopping'],
            'Education': ['education', 'learning', 'training', 'course'],
            'Manufacturing': ['manufacturing', 'hardware', 'industrial'],
        }
        
        text_lower = text.lower()
        
        # Count matches for each domain
        domain_scores = {}
        for domain, keywords in expertise_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                domain_scores[domain] = score
        
        # Return highest scoring domain
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        else:
            return "General"