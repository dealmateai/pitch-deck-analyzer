"""
Fit Calculator - Calculate Company Fit & Founder Fit Scores
Based on extracted details from pitch deck.
"""

import re
from typing import Dict, Tuple
from utils.logger import log

class FitCalculator:
    """Calculate company and founder fit scores."""
    
    def __init__(self):
        """Initialize fit calculator."""
        log.info("✓ FitCalculator initialized")
    
    def calculate_company_fit(self, company_info: Dict, 
                            kaggle_companies: list = None) -> float:
        """
        Calculate Company Fit Score (0-100%).
        
        Factors:
        - Industry clarity (10%)
        - Problem statement quality (20%)
        - Solution clarity (20%)
        - Market size understanding (20%)
        - Traction metrics (30%)
        
        Args:
            company_info: Extracted company information
            kaggle_companies: List of known successful companies (for comparison)
        
        Returns:
            Score 0-100%
        """
        scores = {}
        
        # 1. Industry Clarity (10%)
        industry_score = 10 if company_info.get("industry") and company_info["industry"] != "Other" else 0
        scores["industry"] = industry_score
        
        # 2. Problem Statement Quality (20%)
        problem = company_info.get("problem", "")
        if problem and problem != "Not specified":
            problem_length = len(problem)
            problem_score = min(20, (problem_length / 50) * 20)
            scores["problem"] = problem_score
        else:
            scores["problem"] = 0
        
        # 3. Solution Clarity (20%)
        solution = company_info.get("solution", "")
        if solution and solution != "Not specified":
            solution_length = len(solution)
            solution_score = min(20, (solution_length / 50) * 20)
            scores["solution"] = solution_score
        else:
            scores["solution"] = 0
        
        # 4. Market Size Understanding (20%)
        market = company_info.get("market_size", {})
        market_score = 0
        
        if market.get("tam"):
            market_score += 10  # Has TAM
        if market.get("growth_rate"):
            market_score += 10  # Has growth rate
        
        scores["market"] = min(20, market_score)
        
        # 5. Traction Metrics (30%)
        traction = company_info.get("traction", {})
        traction_score = 0
        
        if traction.get("users"):
            traction_score += 10
        if traction.get("revenue"):
            traction_score += 10
        if traction.get("monthly_growth"):
            traction_score += 10
        
        scores["traction"] = min(30, traction_score)
        
        # Calculate total
        company_fit = sum(scores.values())
        
        log.info(f"Company Fit Breakdown: {scores}")
        log.info(f"Total Company Fit: {company_fit}%")
        
        return min(company_fit, 100)
    
    def calculate_founder_fit(self, founder_info: Dict) -> float:
        """
        Calculate Founder Fit Score (0-100%).
        
        Factors:
        - Number of founders (10%)
        - Experience level (20%)
        - Technical background (20%)
        - Top school education (15%)
        - Previous startup experience (20%)
        - Domain expertise (15%)
        
        Args:
            founder_info: Extracted founder information
        
        Returns:
            Score 0-100%
        """
        scores = {}
        
        # 1. Founder Count (10%)
        founder_count = founder_info.get("count", 0)
        count_score = min(10, founder_count * 5)  # 5 points per founder, max 10
        scores["founder_count"] = count_score
        
        # 2. Experience Level (20%)
        experience_mapping = {
            "Highly Experienced": 20,
            "Moderately Experienced": 15,
            "Some Experience": 10,
            "Early Career": 5,
        }
        experience = founder_info.get("experience_level", "Early Career")
        scores["experience"] = experience_mapping.get(experience, 5)
        
        # 3. Technical Background (20%)
        technical_score = 20 if founder_info.get("technical_background") else 5
        scores["technical"] = technical_score
        
        # 4. Top School Education (15%)
        education = founder_info.get("education", {})
        education_score = 15 if education.get("top_school") else 5
        scores["education"] = education_score
        
        # 5. Previous Startup Experience (20%)
        startup_history = founder_info.get("previous_startups", {})
        startup_score = 0
        
        if startup_history.get("is_serial"):
            startup_score += 15
        if startup_history.get("previous_exits", 0) > 0:
            startup_score += 5
        
        if startup_score == 0:
            startup_score = 5
        
        scores["startup_exp"] = min(20, startup_score)
        
        # 6. Domain Expertise (15%)
        domain = founder_info.get("domain_expertise", "General")
        domain_score = 15 if domain != "General" else 5
        scores["domain"] = domain_score
        
        # Calculate total
        founder_fit = sum(scores.values())
        
        log.info(f"Founder Fit Breakdown: {scores}")
        log.info(f"Total Founder Fit: {founder_fit}%")
        
        return min(founder_fit, 100)
    
    def calculate_combined_score(self, company_fit: float, founder_fit: float) -> float:
        """
        Calculate overall combined score.
        
        Args:
            company_fit: Company fit score
            founder_fit: Founder fit score
        
        Returns:
            Combined score (weighted average)
        """
        # 60% company fit, 40% founder fit
        combined = (company_fit * 0.6) + (founder_fit * 0.4)
        
        log.info(f"Combined Score: {combined:.1f}%")
        
        return min(combined, 100)