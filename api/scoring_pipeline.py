"""
Scoring Pipeline - REWRITTEN for Company & Founder Fit Analysis
Extracts details from pitch deck PDF and calculates fit scores.
"""

from typing import Dict, Optional, Tuple
import pandas as pd
from utils.logger import log
from nlp.pdf_extractor import PDFExtractor
from nlp.nlp_pipeline import NLPPipeline
from nlp.company_extractor import CompanyExtractor
from nlp.founder_extractor import FounderExtractor
from nlp.fit_calculator import FitCalculator
from api.models import AnalysisResponse, CompanyExtracted, FounderExtracted

class ScoringPipeline:
    """
    Complete pipeline for analyzing pitch decks.
    
    Flow:
    1. Extract PDF text
    2. Analyze text with NLP
    3. Extract company details
    4. Extract founder details
    5. Calculate company fit score
    6. Calculate founder fit score
    7. Return results
    """
    
    def __init__(self, kaggle_companies: Optional[list] = None):
        """
        Initialize scoring pipeline.
        
        Args:
            kaggle_companies: List of known successful companies from Kaggle
        """
        log.info("Initializing scoring pipeline...")
        
        self.pdf_extractor = PDFExtractor()
        log.info("✓ PDF extractor initialized")
        
        self.nlp_pipeline = NLPPipeline()
        log.info("✓ NLP pipeline initialized")
        
        self.company_extractor = CompanyExtractor()
        log.info("✓ Company extractor initialized")
        
        self.founder_extractor = FounderExtractor()
        log.info("✓ Founder extractor initialized")
        
        self.fit_calculator = FitCalculator()
        log.info("✓ Fit calculator initialized")
        
        self.kaggle_companies = kaggle_companies or []
        
        log.info("✓ Scoring pipeline fully initialized")
    
    
    def analyze_pitch_deck(self, pdf_path: str) -> Optional[AnalysisResponse]:
        """
        Complete analysis of pitch deck.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            AnalysisResponse with scores and extracted data
        """
        try:
            log.info("=" * 80)
            log.info(f"Starting analysis of: {pdf_path}")
            log.info("=" * 80)
            
            # STEP 1: Extract PDF text
            log.info("\n[STEP 1] Extracting PDF text...")
            pdf_data = self._extract_pdf(pdf_path)
            if pdf_data is None:
                return None
            
            # STEP 2: Analyze text with NLP
            log.info("\n[STEP 2] Analyzing text with NLP...")
            nlp_analysis = self._analyze_text(pdf_data)
            if nlp_analysis is None:
                return None
            
            # STEP 3: Extract company details
            log.info("\n[STEP 3] Extracting company details...")
            company_info = self.company_extractor.extract_company_info(
                pdf_data["full_text_cleaned"],
                nlp_analysis.get("entities", {})
            )
            
            # STEP 4: Extract founder details
            log.info("\n[STEP 4] Extracting founder details...")
            founder_info = self.founder_extractor.extract_founder_info(
                pdf_data["full_text_cleaned"],
                nlp_analysis.get("entities", {})
            )
            
            # STEP 5: Calculate company fit
            log.info("\n[STEP 5] Calculating company fit score...")
            company_fit = self.fit_calculator.calculate_company_fit(
                company_info,
                self.kaggle_companies
            )
            
            # STEP 6: Calculate founder fit
            log.info("\n[STEP 6] Calculating founder fit score...")
            founder_fit = self.fit_calculator.calculate_founder_fit(founder_info)
            
            # STEP 7: Calculate overall score
            log.info("\n[STEP 7] Calculating overall score...")
            overall_score = self.fit_calculator.calculate_combined_score(
                company_fit, founder_fit
            )
            
            # STEP 8: Generate recommendations
            log.info("\n[STEP 8] Generating recommendations...")
            recommendations = self._generate_recommendations(
                company_fit, founder_fit, company_info, founder_info
            )
            
            # Create response
            response = AnalysisResponse(
                company_fit=company_fit,
                founder_fit=founder_fit,
                overall_score=overall_score,
                company_extracted=CompanyExtracted(**company_info),
                founder_extracted=FounderExtracted(**founder_info),
                analysis={
                    "pdf_pages": pdf_data.get("num_pages"),
                    "word_count": pdf_data.get("word_count"),
                    "nlp_keywords": len(nlp_analysis.get("keywords", [])),
                },
                recommendations=recommendations,
            )
            
            log.info("\n" + "=" * 80)
            log.info("✓ ANALYSIS COMPLETED SUCCESSFULLY")
            log.info("=" * 80)
            log.info(f"Company Fit: {company_fit:.1f}%")
            log.info(f"Founder Fit: {founder_fit:.1f}%")
            log.info(f"Overall Score: {overall_score:.1f}%")
            
            return response
        
        except Exception as e:
            log.error(f"Error in analysis pipeline: {str(e)}", exc_info=True)
            return None
    
    def _extract_pdf(self, pdf_path: str) -> Optional[Dict]:
        """Extract PDF text."""
        try:
            log.info(f"[PDF] Extracting from: {pdf_path}")
            
            extracted = self.pdf_extractor.extract(pdf_path)
            
            if extracted is None:
                log.error("[PDF] Extraction returned None")
                return None
            
            if not extracted.get("full_text"):
                log.error("[PDF] No text extracted")
                return None
            
            log.info(f"[PDF] ✓ Extracted {extracted['num_pages']} pages")
            log.info(f"[PDF] Text length: {len(extracted['full_text'])} characters")
            log.info(f"[PDF] Word count: {extracted.get('word_count', 0)}")
            
            return extracted
        
        except Exception as e:
            log.error(f"[PDF] Extraction error: {str(e)}", exc_info=True)
            return None
    
    def _analyze_text(self, pdf_data: Dict) -> Optional[Dict]:
        """Analyze text with NLP."""
        analysis = self.nlp_pipeline.analyze_text(pdf_data["full_text_cleaned"])
        
        if analysis is None:
            log.error("Failed to analyze text")
            return None
        
        log.info(f"✓ Text analysis completed")
        log.info(f"  Keywords: {len(analysis.get('keywords', []))}")
        log.info(f"  Entities: {len(analysis.get('entities', {}))}")
        
        return analysis
    
    def _generate_recommendations(
        self,
        company_fit: float,
        founder_fit: float,
        company_info: Dict,
        founder_info: Dict
    ) -> list:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Company recommendations
        if company_fit < 40:
            recommendations.append("❌ Improve problem statement and market analysis")
        
        if not company_info.get("market_size", {}).get("tam"):
            recommendations.append("📊 Include specific TAM (Total Addressable Market)")
        
        if not company_info.get("traction", {}).get("users"):
            recommendations.append("📈 Add user/customer traction metrics")
        
        if not company_info.get("traction", {}).get("revenue"):
            recommendations.append("💰 Include revenue or monetization metrics")
        
        # Founder recommendations
        if founder_fit < 40:
            recommendations.append("👥 Strengthen founder backgrounds and experience")
        
        if founder_info.get("count", 0) < 2:
            recommendations.append("👫 Consider adding co-founder for balanced team")
        
        if not founder_info.get("technical_background"):
            recommendations.append("⚙️ Highlight technical expertise in team")
        
        # Combined recommendations
        if company_fit > 80 and founder_fit > 80:
            recommendations.insert(0, "🎯 Strong pitch! Ready for investor pitching")
        
        if company_fit > 70 or founder_fit > 70:
            recommendations.insert(0, "✅ Good fit - Ready for refinement")
        
        return recommendations if recommendations else ["✓ Standard pitch deck"]