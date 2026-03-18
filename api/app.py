"""
FastAPI Application - Pitch Deck Analyzer
Input: PDF pitch deck
Output: Company Fit % & Founder Fit %
"""

import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import log
from config import API_CONFIG
from api.models import AnalysisResponse, HealthResponse
from api.scoring_pipeline import ScoringPipeline

# Initialize FastAPI
app = FastAPI(
    title="Pitch Deck Analyzer API",
    description="Analyze pitch decks and calculate Company Fit % & Founder Fit %",
    version="2.0.0",
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global scoring pipeline
scoring_pipeline = None

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    global scoring_pipeline
    
    try:
        log.info("Starting Pitch Deck Analyzer API...")
        scoring_pipeline = ScoringPipeline()
        log.info("✓ API initialized successfully")
    except Exception as e:
        log.error(f"Failed to initialize API: {str(e)}")
        raise

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        models_loaded=scoring_pipeline is not None,
        version="2.0.0",
    )

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_pitch_deck(file: UploadFile = File(...)):
    """
    Analyze pitch deck PDF.
    
    Input: PDF file
    Output: Company Fit % & Founder Fit %
    
    Returns:
        AnalysisResponse with fit scores and extracted details
    """
    
    # Validate file
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    if getattr(file, "size", None):
        if file.size > API_CONFIG["max_file_size"]:
            raise HTTPException(
                status_code=400,
                detail=f"File too large (max {API_CONFIG['max_file_size'] / 1024 / 1024:.0f}MB)"
            )
    
    temp_file = None
    try:
        # Save upload to temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            temp_file = tmp.name
            content = await file.read()
            if not content:
                raise HTTPException(
                    status_code=400,
                    detail="Empty file uploaded"
                )
            if len(content) > API_CONFIG["max_file_size"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large (max {API_CONFIG['max_file_size'] / 1024 / 1024:.0f}MB)"
                )
            tmp.write(content)
        
        log.info(f"Processing: {file.filename}")
        
        # Check pipeline
        if scoring_pipeline is None:
            raise HTTPException(
                status_code=500,
                detail="Pipeline not initialized"
            )
        
        # Analyze
        result = scoring_pipeline.analyze_pitch_deck(temp_file)
        
        if result is None:
            raise HTTPException(
                status_code=400,
                detail="Failed to analyze pitch deck"
            )
        
        log.info(f"✓ Analysis complete: Company {result.company_fit:.1f}% | Founder {result.founder_fit:.1f}%")
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal error"
        )
    
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Pitch Deck Analyzer API",
        "version": "2.0.0",
        "description": "Analyze pitch decks - Get Company Fit % & Founder Fit %",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze (POST)",
            "docs": "/docs",
        },
    }