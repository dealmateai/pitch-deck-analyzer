"""
API Models - Request/Response Validation
Updated for Company & Founder Fit Analysis
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class CompanyExtracted(BaseModel):
    """Extracted company details."""
    name: Optional[str] = Field(None, description="Company name")
    industry: Optional[str] = Field(None, description="Industry/Domain")
    problem: Optional[str] = Field(None, description="Problem statement")
    solution: Optional[str] = Field(None, description="Solution description")
    market_size: Optional[Dict] = Field(None, description="Market size data")
    traction: Optional[Dict] = Field(None, description="Traction metrics")
    business_model: Optional[str] = Field(None, description="Business model type")

class FounderExtracted(BaseModel):
    """Extracted founder details."""
    names: Optional[List[str]] = Field(None, description="Founder names")
    count: Optional[int] = Field(None, description="Number of founders")
    experience_level: Optional[str] = Field(None, description="Experience level")
    education: Optional[Dict] = Field(None, description="Education details")
    technical_background: Optional[bool] = Field(None, description="Has technical background")
    previous_companies: Optional[List[Dict]] = Field(None, description="Previous company experience")
    startup_experience: Optional[bool] = Field(None, description="Whether founder has startup experience")
    previous_startups: Optional[Dict] = Field(None, description="Previous startup experience")
    domain_expertise: Optional[str] = Field(None, description="Domain expertise")

class AnalysisResponse(BaseModel):
    """API response for pitch deck analysis."""
    
    company_fit: float = Field(..., description="Company/Idea Fit Score (0-100%)", ge=0, le=100)
    founder_fit: float = Field(..., description="Founder Fit Score (0-100%)", ge=0, le=100)
    overall_score: float = Field(..., description="Combined Score (0-100%)", ge=0, le=100)
    
    company_extracted: CompanyExtracted = Field(..., description="Extracted company details")
    founder_extracted: FounderExtracted = Field(..., description="Extracted founder details")
    
    analysis: Optional[Dict] = Field(None, description="Detailed analysis breakdown")
    recommendations: Optional[List[str]] = Field(None, description="Recommendations for improvement")

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="API status")
    models_loaded: bool = Field(..., description="Whether models are loaded")
    version: str = Field(..., description="API version")