"""
Create a test pitch deck PDF for Postman testing
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_test_pitch_deck():
    """Create a realistic test pitch deck PDF."""
    
    pdf_path = "test_pitch_deck.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    y = height - 50
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, y, "TechAI Analytics - Pitch Deck")
    y -= 50
    
    # Company Name
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Company: TechAI Analytics Inc")
    y -= 25
    
    # PROBLEM SECTION
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "PROBLEM")
    y -= 20
    c.setFont("Helvetica", 10)
    problem_text = "Current analytics tools are expensive (>$500/month), require deep technical knowledge, and have poor user experience. Businesses struggle to extract actionable insights from their data."
    c.drawString(50, y, problem_text[:80])
    y -= 15
    c.drawString(50, y, problem_text[80:])
    y -= 30
    
    # SOLUTION SECTION
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "SOLUTION")
    y -= 20
    c.setFont("Helvetica", 10)
    solution_text = "We provide an AI-powered analytics platform with natural language interface. Users simply ask questions in English and get insights instantly. No coding required."
    c.drawString(50, y, solution_text[:80])
    y -= 15
    c.drawString(50, y, solution_text[80:])
    y -= 30
    
    # MARKET SIZE
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "MARKET SIZE")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "TAM: $50 billion in analytics software market")
    y -= 15
    c.drawString(50, y, "Growing at 15% annually (CAGR)")
    y -= 30
    
    # TRACTION
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "TRACTION")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "• 50,000 active users")
    y -= 15
    c.drawString(50, y, "• $500K monthly recurring revenue (MRR)")
    y -= 15
    c.drawString(50, y, "• 40% month-over-month growth")
    y -= 15
    c.drawString(50, y, "• Enterprise customers: Fortune 500 companies")
    y -= 30
    
    # TEAM
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "TEAM")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "CEO: Dr. Sarah Chen")
    y -= 15
    c.drawString(50, y, "  • PhD in AI from Stanford University")
    y -= 15
    c.drawString(50, y, "  • Previously: Senior AI Researcher at Google")
    y -= 15
    c.drawString(50, y, "  • 8 years of experience in machine learning")
    y -= 20
    c.drawString(50, y, "CTO: John Smith")
    y -= 15
    c.drawString(50, y, "  • BS Computer Science from MIT")
    y -= 15
    c.drawString(50, y, "  • Previously: Engineering Lead at Meta AI")
    y -= 15
    c.drawString(50, y, "  • 10 years of backend engineering experience")
    y -= 30
    
    # BUSINESS MODEL
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "BUSINESS MODEL")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "SaaS subscription: Starter ($99/month), Professional ($499/month), Enterprise (custom)")
    y -= 30
    
    # FUNDING ASK
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "FUNDING ASK")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Seeking $10M Series B to:")
    y -= 15
    c.drawString(50, y, "  • Expand enterprise sales team")
    y -= 15
    c.drawString(50, y, "  • Accelerate product development")
    y -= 15
    c.drawString(50, y, "  • Scale marketing and brand awareness")
    
    # Save
    c.save()
    print(f"✓ Test PDF created: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    pdf_path = create_test_pitch_deck()
    print(f"File size: {os.path.getsize(pdf_path)} bytes")
    print(f"Ready for upload in Postman!")