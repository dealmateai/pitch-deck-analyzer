"""
Test Script for Pitch Deck Analyzer API
Tests both health endpoint and analysis endpoint
"""

import sys
import tempfile
from pathlib import Path
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from utils.logger import log, setup_logger

setup_logger()

def create_test_pdf() -> str:
    """Create test pitch deck PDF."""
    log.info("Creating test PDF...")
    
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        temp_path = tmp.name
    
    c = canvas.Canvas(temp_path, pagesize=letter)
    width, height = letter
    y = height - 50
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, y, "TechAI Analytics - Pitch Deck")
    y -= 40
    
    # Problem
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "PROBLEM")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Current analytics tools are expensive, complex, and require deep technical knowledge.")
    y -= 30
    
    # Solution
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "SOLUTION")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "We provide an AI-powered analytics platform with natural language interface.")
    y -= 30
    
    # Market
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "MARKET")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "TAM: $50 billion in analytics software. Growing at 15% annually.")
    y -= 30
    
    # Traction
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "TRACTION")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "50,000 users, $500K MRR, 40% monthly growth. Enterprise clients include Fortune 500 companies.")
    y -= 30
    
    # Team
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "TEAM")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Founder: Dr. Sarah Chen (PhD AI from Stanford, ex-Google Research)")
    y -= 15
    c.drawString(50, y, "CTO: John Smith (BS Computer Science from MIT, ex-Meta AI)")
    y -= 30
    
    # Ask
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "ASK")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Seeking $10M Series B to expand enterprise sales and product development.")
    
    c.save()
    
    log.info(f"✓ Test PDF created: {temp_path}")
    return temp_path

def test_health():
    """Test health endpoint."""
    log.info("\n[TEST 1] Testing health endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            log.info(f"✓ Health check passed")
            log.info(f"  Status: {data['status']}")
            log.info(f"  Models loaded: {data['models_loaded']}")
            return True
        else:
            log.error(f"✗ Health check failed: {response.status_code}")
            return False
    
    except Exception as e:
        log.error(f"✗ Error: {str(e)}")
        return False

def test_analyze():
    """Test analyze endpoint."""
    log.info("\n[TEST 2] Testing analyze endpoint...")
    
    try:
        pdf_path = create_test_pdf()
        
        with open(pdf_path, "rb") as f:
            files = {"file": (Path(pdf_path).name, f, "application/pdf")}
            response = requests.post(
                "http://localhost:8000/analyze",
                files=files,
                timeout=120
            )
        
        if response.status_code == 200:
            data = response.json()
            
            log.info(f"✓ Analysis completed")
            log.info(f"\n📊 RESULTS:")
            log.info(f"  Company Fit: {data['company_fit']:.1f}%")
            log.info(f"  Founder Fit: {data['founder_fit']:.1f}%")
            log.info(f"  Overall Score: {data['overall_score']:.1f}%")
            
            log.info(f"\n🏢 Extracted Company:")
            log.info(f"  Name: {data['company_extracted'].get('name', 'N/A')}")
            log.info(f"  Industry: {data['company_extracted'].get('industry', 'N/A')}")
            
            log.info(f"\n👥 Extracted Founders:")
            log.info(f"  Count: {data['founder_extracted'].get('count', 0)}")
            log.info(f"  Experience: {data['founder_extracted'].get('experience_level', 'N/A')}")
            
            if data.get('recommendations'):
                log.info(f"\n💡 Recommendations:")
                for rec in data['recommendations']:
                    log.info(f"  {rec}")
            
            return True
        else:
            log.error(f"✗ Analysis failed: {response.status_code}")
            log.error(f"  Response: {response.text}")
            return False
    
    except Exception as e:
        log.error(f"✗ Error: {str(e)}")
        return False

def main():
    """Run all tests."""
    log.info("=" * 80)
    log.info("PITCH DECK ANALYZER - API TESTS")
    log.info("=" * 80)
    
    results = [
        test_health(),
        test_analyze(),
    ]
    
    log.info("\n" + "=" * 80)
    log.info("TEST SUMMARY")
    log.info("=" * 80)
    
    passed = sum(results)
    total = len(results)
    
    log.info(f"Passed: {passed}/{total} tests")
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())